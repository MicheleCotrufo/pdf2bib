import json
import re
import logging
import urllib.parse
from unidecode import unidecode
import bibtexparser

logger = logging.getLogger('pdf2bib')

#The functions parse_bib_from_dxdoiorg and parse_bib_from_exportarxivorg take as input a string or other object, which has been obtained by the library pdf2doi by
#querying the relevant websites. By analyzing this input, they create a dictionary containing valid bibtex infos and return it as output.
#The output dictionaries returned by parse_bib_from_dxdoiorg and parse_bib_from_exportarxivorg must have the same "format", i.e. the same set of required keys
#(additional keys are possible)
#The required keys in the dictionaries are 'title', 'journal', 'volume', 'issue', 'page', 'year', 'month', 'publisher', 'author', 'URL', 'DOI'    

#The dictionaries are then fed to the function make_bibtex(data) which creates a string containing the full bibtex entry

#The functions make_bibtex, parse_bib_from_dxdoiorg and parse_bib_from_exportarxivorg are called directly from the function pdf2bib_singlefile inside main.py, but they
#can also called directly by an user is (s)he knows what (s)he is doing.

def parse_bib_from_dxdoiorg(text, method):
    """
    Given a certain string contained in the input variable text, which was obtained from pdf2doi by quering dx.doi.org, it parses the string and returns a dictionary containing valid bibtex infos.
    The input variable method is a string which specifies the method used by pdf2doi to query dx.doi.org, and it is normally defined in pdf2doi.config.get('method_dxdoiorg')

    Note: the methods "application/x-bibtex" and "text/bibliography; style=bibtex" return strings in the same format
    Note: "text/bibliography; style=bibtex" returns the authors in the format "LastName1, FirstName1 SecondName1.. and LastName2, FirstName2 SecondName2.. and etc."
    Note: the method 'application/citeproc+json' returns data in JSON format

    When the method "application/citeproc+json" is used (which will be the standard method) the dictionary returned by this function contains ALWAYS ONLY the following keys
    'title', 'author', 'journal', 'volume', 'issue', 'page', 'publisher', 'url', 'doi', 'year', 'month'
    all values are strings, except for the value corresponding to the 'author' key, which is instead a list of dictionaries (one dictionary per each author).
    Normally, the format returned by dx.doi.org when using "application/citeproc+json" is author =  [{'given': 'Name1', 'family': 'LastName1'}, {'given': 'Name2', 'family': 'LastName2'}, ... [{'given': 'NameN', 'family': 'LastNameN'}]
    """

    # 
    if method == "application/x-bibtex":
        data = bibtexparser.loads(text)
        metadata = data.entries[0]
        return metadata
    if method == "text/bibliography; style=bibtex":
        data = bibtexparser.loads(text)
        metadata = data.entries[0]
        return metadata
    if method == "application/citeproc+json":        
        try:
            json_dict = json.loads(text)
        except Exception as e:
            print(f'A problem occurred when trying to parse the text: {e}') 
            return None

        #I extract only certain fields from the JSON dict
        fields = ['title', 'volume', 'issue', 'page', 'publisher', 'URL', 'DOI']
        metadata = dict()

        for field in fields:
            try:
                metadata[field.lower()] = json_dict[field] if field in json_dict.keys() else ''
            except:
                metadata[field.lower()] = ''
        try:
            metadata['journal'] = json_dict["container-title"] 
        except:
            metadata['journal'] = ''

        if (metadata['publisher'] == 'arXiv') and (metadata['journal'] == ''):
            metadata['journal'] = 'arXiv'

        try:
            metadata['year'] = json_dict["issued"]['date-parts'][0][0]
        except:
            metadata['year'] = ''
        try:
            metadata['month'] = json_dict["issued"]['date-parts'][0][1]
        except:
            metadata['month'] = ''
        try:
            metadata['author'] = [author for author in json_dict['author']]
        except:
            metadata['author'] = ''
        return metadata
    raise ValueError("The input variable method does not have a valid value")


def parse_bib_from_exportarxivorg(items):
    """
    Given a certain dictionary contained in the input variable items (which was obtained from pdf2doi by quering export.arxiv.org)
    it returns a dictionary containing valid bibtex infos

    the dictionary returned by this functions contains ALWAYS ONLY the following keys
    'title', 'author', 'ejournal', 'eprint', 'published', 'url', 'doi','arxiv_doi', 'year', 'month', 'day', 'ENTRYTYPE'

    all values are strings, except for the value corresponding to the 'author' key, which is either a string in the format "Name1 Lastname1 and Name2 Lastname2 and ... "
    #or a list of dictionaries in the format  [{'given': 'Name1', 'family': 'LastName1'}, {'given': 'Name2', 'family': 'LastName2'}, ... [{'given': 'NameN', 'family': 'LastNameN'}]
    """
    #Extract data from the dictionary items
    data_to_extract = ['title','link','published','arxiv_doi']
    data =[items[key] if key in items.keys() else None for key in data_to_extract]

    #Create the dictionary data_dict which will be passed to the function make_bibtex
    data_dict = dict(zip(data_to_extract,data))

    #add additionaly values
    if isinstance(data_dict['arxiv_doi'],str):
        data_dict['eprint'] ="arXiv:" + data_dict['arxiv_doi']
    data_dict['ejournal'] ="arXiv" 
    data_dict['ENTRYTYPE'] = 'article'
    #rename some of the keys in order to match the bibtex standards
    data_dict['url'] = data_dict.pop('link')
    data_dict['doi'] = data_dict.pop('arxiv_doi')       
    #parse the published data to get the year, month and day
    if data_dict['published']:
        regexDate = re.search(r'(\d{4}\-\d{2}\-\d{2})',data_dict['published'],re.I)
        if regexDate:
            date_list =  (regexDate.group(1)).split("-")
            year = date_list[0] if len(date_list)>0 else '0000'
            month = date_list[1] if len(date_list)>1 else '00'
            day = date_list[2] if len(date_list)>2 else '00'
    else:
        year,month,day = '0000', '00', '00'
    data_dict['year'] = year
    data_dict['month'] = month
    data_dict['day'] = day

    if 'authors' in items:
        authors = items['authors'] #The entry 'authors' should always be a list of dictionaries, with one dictionary for each author
    elif 'author' in items:
        authors = items['author'] #The entry 'author' is normally a string containing only one author (normally the corresponding author)
    else:
        authors = ''

    #The typical format returned by export.arxiv.org for the authors is a list 
    #in the format [{'name': 'Name1 LastName1'}, {'name': 'Name2 LastName2'}, ... [{'name': 'NameN LastNameN'}], 
    #If authors is indeed a list in this format, we reshape it in the format [{'given': 'Name1', 'family': 'LastName1'}, {'given': 'Name2', 'family': 'LastName2'}, ... [{'given': 'NameN', 'family': 'LastNameN'}]
    if authors and isinstance(authors,list):
        authorsnames_list = [ {'given' : " ".join(author['name'].split(" ")[0:-1]), 'family': author['name'].split(" ")[-1]} for author in authors]
        data_dict['author'] = authorsnames_list
    elif authors and isinstance(authors,str):
        data_dict['author'] = authors

    return data_dict


def make_bibtex(metadata):
    #Based on the metadata contained in the input dictionary metadata, it creates a valid bibtex entry
    #The ID of the bibtex entry has the format [lastname_firstauthor][year][first_word_title] all in lower case
    #If the tag url is present, any possible ascii code (e.g. %2f) is decoded
    #Note: the code below assumes that the field for the authors is either a string in the format "Name1 Lastname1 and Name2 Lastname2 and ... "
    #or a list of dictionaries in the format  [{'given': 'Name1', 'family': 'LastName1'}, {'given': 'Name2', 'family': 'LastName2'}, ... [{'given': 'NameN', 'family': 'LastNameN'}]
    
    data = metadata.copy()

    if 'author' in data.keys():
        authors = data['author']
    else:
        authors = ''

    if not(type(authors) in (str, list)):
        raise TypeError('The value corresponding to the key ''author'' must be either a string or a list of strings')
    
    #Generate the ID by looking for last name of first author, year of publicaton, and first word of title
    try:
        if authors and isinstance(authors,list):
            firstauthor = authors[0]
            lastname_firstauthor = (firstauthor['family'].strip()).split(' ')[0]
        elif authors and isinstance(authors,str): 
            lastname_firstauthor = authors.split(" and ")[0].split(" ")[-1] #We assume that the word before the first occurence of and is the last name of first author
        else: 
            lastname_firstauthor = ''
    except:
        lastname_firstauthor =''
    year = data['year'] if 'year' in data.keys() else ''
    try:
        first_word_title =  data['title'].split(' ')[0] if 'title' in data.keys()  else ''
    except:
        first_word_title =''
    id = lastname_firstauthor + str(year) + first_word_title
    id = id.lower()
    id = remove_latex_codes(id)
    id = unidecode(id) #This makes sure that the id of the bibtex entry is only made out of ascii characters (i.e. no accents, tildes, etc.)
    id = re.sub(
        "-|,|:|'|\\n", "", id
    ) # Make sure to remove any possible hyphen, comma, colon, single quote, and newline.
    if id == '':
        id = 'NoValidID'

    #Sanitize the URL
    if 'url' in data.keys():
        data['url'] = urllib.parse.unquote(data['url'])

    if not 'ENTRYTYPE' in data.keys():
        data['ENTRYTYPE'] = 'article'

    if  isinstance(authors,list):
        #if authors is defined as a list, it will have the format [{'given': 'Name1', 'family': 'LastName1'}, {'given': 'Name2', 'family': 'LastName2'}, ... [{'given': 'NameN', 'family': 'LastNameN'}]
        #We convert it into a string Name1 Lastname1 and Name2 Lastname2 and ... "
        authors_string = " and ".join([ a.get('given', '') +  " " + a.get('family', '')  for a in authors if (('family' in a) or ('given' in a))])
        data['author'] = authors_string
    elif isinstance(authors,str):
        #if instead authors is a string, then it is already in the right format
        data['author'] = authors

    #Create the bibtex entry as a string 
    metadata_not_to_use = ['ENTRYTYPE','ID'] #These are temporary metadata, not useful for bibtex
    text = ["@"+data['ENTRYTYPE']+"{" + id]
    for key, value in data.items():
        if value and not (key in metadata_not_to_use):
            text.append("\t%s = {%s}" % (key, value))
    bibtex_entry = (",\n").join(text) + "\n" + "}"
    return bibtex_entry


def remove_latex_codes(text):
    #It replaces any latex special code (e.g. {\`{u}}) by the "closest" unicode character (e.g. u). This is useful when
    #certain strings which might contain latex codes need to be used in contexts where only unicode characters are accepted
    
    #This regex looks for any substring that matches the pattern "{\string1{string2}}" where string1 can be anything,
    #and it replaces the whole substring by string2
    text_sanitized = re.sub(r"{\\[^\{]+{([\w]+)}}", r"\1",text)
    return text_sanitized
