import argparse
import logging
from os import path, listdir
import pdf2bib.bibtex_makers as bibtex_makers
import pdf2bib.config as config
import pdf2doi as pdf2doi
#import pyperclip (Modules that are commented here are imported later only when needed, to improve start up time)

#We tell pdf2doi to use the same value of save_identifier_metadata specified in the settings of pdf2bib. When pdf2bib is called via command line, 
#the value of save_identifier_metadata (for both pdf2doi and pdf2bib) might get changed
pdf2doi.config.set('save_identifier_metadata',config.get('save_identifier_metadata')) 

def pdf2bib(target):
    ''' 
    This is the main routine of the library. When the library is used as a command-line tool (via the entry-point "pdf2bib") the input arguments
    are collected, validated and sent to this function (see the function main() below). Alternatively, the function can be called from a Python
    script by importing pdf2bib. The output is a dictionary (or a list of dictionaries if multiple files are target) which contains, for each file, 
    all the info returned by the library pdf2doi, plus additional bibtex raw data and bibtex entry.

        Example:
        import pdf2bib
        path = r"Path\to\folder"
        result = pdf2bib.pdf2bib(path)
        print(result[0]['metadata']             # Dictionary containing bibtex data
        print(result[0]['bibtex']               # A string containing a valid bibtex entry

    Parameters
    ----------
    target : string
        Relative or absolute path of a .pdf file or a directory containing pdf files

    Returns
    -------
    results, dictionary or list of dictionaries (or None if an error occured)
        The output is a single dictionary if target is a file, or a list of dictionaries if target is a directory, 
        each element of the list describing one file. Each dictionary has the following keys
        
        result['identifier']        = DOI or other identifier (or None if nothing is found)
        result['identifier_type']   = String specifying the type of identifier (e.g. 'doi' or 'arxiv')
        result['validation_info']   = Additional info on the paper. If config.get('webvalidation') = True, then result['validation_info']
                                      will typically contain raw bibtex data for this paper. Otherwise it will just contain True 
        result['path']              = Path of the pdf file
        result['method']            = Method used to find the identifier
        result['metadata']          = Dictionary containing bibtex info
        result['bibtex']            = A string containing a valid bibtex entry

    ''' 

    # Setup logging
    logger = logging.getLogger("pdf2bib")

    # Make sure the path is a string in case a Pathlib object is provided
    target = str(target)

    #Check if path is valid
    if not(path.exists(target)):
        logger.error(f"{target} is not a valid path to a file or a directory.")
        return None
      
    #Check if target is a directory
    #If yes, we look for all the .pdf files inside it, and for each of them
    #we call again this function
    if  path.isdir(target):
        logger.info(f"Looking for pdf files in the folder {target}...")
        pdf_files = [f for f in listdir(target) if (f.lower()).endswith('.pdf')]
        numb_files = len(pdf_files)
        
        if numb_files == 0:
            logger.error("No pdf files found in this folder.")
            return None
        
        logger.info(f"Found {numb_files} pdf files.")
        if not(target.endswith(config.get('separator'))): #Make sure the path ends with "\" or "/" (according to the OS)
            target = target + config.get('separator')
            
        papers = [] #For each pdf file in the target folder we will store a dictionary inside this list
        for f in pdf_files:
            logger.info("................") 
            file = target + f
            #For each file we call again this function, but now the input argument target is set to the path of the file
            result = pdf2bib(target=file)
            #logger.info(result['identifier'])
            papers.append(result)

        logger.info("................") 

        return papers
    
    #If target is not a directory, we check that if it is an existing file and that it ends with .pdf
    else:
        filename = target
        if not path.exists(filename):
            logger.error(f"'{filename}' is not a valid file.")
            return None   
        if not (filename.lower()).endswith('.pdf'):
            logger.error("The file must have .pdf extension.")
            return None

        result = pdf2bib_singlefile(filename)

        return result 

def pdf2bib_singlefile(filename):
    '''
    Extract bibtex data from the pdf file specified by filename. This function does not check wheter filename is a valid path to a pdf file.

    Parameters
    ----------
    filename : string
        absolute path of a single .pdf file

    Returns
    -------
    result : dictionary
        The output is a single dictionary describing the data obtained for this file.
        The dictionary has the following keys
        result['identifier']        = DOI or other identifier (or None if nothing is found)
        result['identifier_type']   = String specifying the type of identifier (e.g. 'doi' or 'arxiv')
        result['validation_info']   = Additional info on the paper. If config.get('webvalidation') = True, then result['validation_info']
                                      will typically contain raw bibtex data for this paper. Otherwise it will just contain True 
        result['path']              = Path of the pdf file
        result['method']            = Method used by pdf2doi to find the identifier
        result['metadata']          = Dictionary containing bibtex info
        result['bibtex']            = A string containing a valid bibtex entry
    ''' 
    # Setup logging
    logger = logging.getLogger("pdf2bib")
    logger.info(f"Trying to extract data to generate the BibTeX entry for the file: {filename}")  
    logger.info(f"Calling pdf2doi...") 
    result = pdf2doi.pdf2doi(filename)
    if result['identifier'] == None:
        logger.error("It was not possible to find a valid identifier for this file.")
        result['metadata'] = None
        result['bibtex'] = None
        return result
    if not (isinstance(result['validation_info'],str) or isinstance(result['validation_info'],dict)):
        result['metadata'] = None
        result['bibtex'] = None
        logger.error("The validation_info returned by pdf2doi is not a string or valid dictionary. It is not possible to extract BibTeX data.")
        return result

    logger.info(f"pdf2doi found a valid identifier for this paper.") 
  
    if result["identifier_type"] == "arxiv ID":
        logger.info(f"Parsing the info returned by export.arxiv.org...")
        metadata = bibtex_makers.parse_bib_from_exportarxivorg(
            result["validation_info"]
        )
    elif result["identifier_type"] == "arxiv DOI":
        if "arxiv_doi" not in result["validation_info"]:
            result["validation_info"]["arxiv_doi"] = result["identifier"]
        logger.info(f"Parsing the info returned by export.arxiv.org...")
        metadata = bibtex_makers.parse_bib_from_exportarxivorg(
            result["validation_info"]
        )
    elif result['identifier_type'] == 'DOI':
        logger.info(f"Parsing the info returned by dx.doi.org...")
        metadata = bibtex_makers.parse_bib_from_dxdoiorg(result['validation_info'], method=pdf2doi.config.get('method_dxdoiorg'))

    if metadata: #if retrieval of bibtex data was succesful, we add the fields to the result dictionary
        result['metadata'] = metadata
        result['bibtex'] = bibtex_makers.make_bibtex(metadata)
        logger.info(f"A valid BibTeX entry was generated.") 
    else:
        result['metadata'] = None
        result['bibtex'] = None
        logger.error("Some error occurred when parsing the raw BibTeX data.")
    
    return result
    


def save_bibtex_entries(filename_bibtex, results, clipboard = False):
    ''' Write all bibtex entries contained in the input list 'results' into a text file with a path specified by filename_bibtex 
        (if filename_bibtex is a valid string) and/or into the clipboard (if clipboard = True).
        the input variable results is a list of dictionaries, and the element results[i]['bibtex'] contains the bibtex entry.
    
    Parameters
    ----------
    filename_bibtex : string
        Absolute path of the target file. If equal to '' or False, nothing is stored on file.
    results : list of dictionaries
        Each element of the list 'results' describes a .pdf file, and contains the pdf identifier, bibtex entry and other infos.
    clipboard : boolean, optional
        If set to True, the bibtex entries are stored in the clipboard. Default is False.

    Returns
    -------
    None.
    '''
    logger = logging.getLogger("pdf2bib")

    if isinstance(filename_bibtex,str) or clipboard:
        text = ''
        for result in results:
            if isinstance(result['bibtex'],str):
                text = text + result['bibtex'] + "\n\n"

    #If filename_bibtex is a valid string, we create the full path of the file where bibtex entries will be saved
    if isinstance(filename_bibtex,str):
        path_filename_bibtex = path.dirname(results[0]['path']) + config.get('separator') + filename_bibtex
        try:
            with open(path_filename_bibtex, "w", encoding="utf-8") as text_file:
                text_file.write(text) 
                print(f'All available bibtex entries have been stored in the file {filename_bibtex}')
        except Exception as e:
            print(e)
            print(f'A problem occurred when trying to write into the file {filename_bibtex}')
    if clipboard:
        import pyperclip
        try:
            pyperclip.copy(text)
            print(f'All available bibtex entries have been stored in the system clipboard')
        except Exception as e:
            print(e)
            print(f'A problem occurred when trying to write into the system clipboard')

    
def main():
    '''
    This is the main function which is called when pdf2dbib is called from the command line. It parses all the input parameters and then 
    (1) Calls the function pdf2bib, obtaining a list of dictionaries as output
    (2) Prints a summary of papers analyzed (if verbose is set to True), and then a list of the bibtex entries generated
    (3) Calls the function save_bibtex_entries to (optionally) save the bibtex entries on file and/or copy them into the clipboard
    '''
    parser = argparse.ArgumentParser( 
            description = "Generate BibTeX entries of scientific publications starting from the pdf files. It requires an internet connection.",
            epilog = "")

    parser.add_argument("path",
                        help = "Relative path of the target pdf file or of the targe folder.",
                        metavar = "path",
                        nargs = '*')
    parser.add_argument("-v",
                        "--verbose",
                        help="Increase verbosity. By default (i.e. when not using -v), only the text of the found bibtex entries will be printed as output.",
                        action="store_true")
    parser.add_argument("-nostore",
                    "--no_store_identifier_metadata",
                    help="pdf2bib uses the library pdf2doi to find the DOI/identifier of a publication. By default, anytime an identifier is found, pdf2doi also adds it to the metadata of the pdf file (if not present yet). By using this additional option, the identifier is not stored in the file metadata.",
                    action="store_true")
    parser.add_argument("-s",
                        "--make_bibtex_file",
                        dest="filename_bibtex",
                        help="Create a text file inside the target directory, with name given by FILENAME_BIBTEX, containing the bibtex entry of each pdf file in the target folder (if any is found).",
                        action="store")
    parser.add_argument("-clip",
                        "--save_bibtex_clipboard",
                        action="store_true",
                        help="Store all found bibtex entries into the clipboard.")
    parser.add_argument("-install--right--click",
                        dest="install_right_click",
                        action="store_true",
                        help="Add a shortcut to pdf2bib in the right-click context menu of Windows. This allows you to copy the bibtex\
                                entry of a pdf file (or all pdf files in a folder) into the clipboard by just right clicking\
                                on it! NOTE: this feature is only available on Windows.")
    parser.add_argument("-uninstall--right--click",
                        dest="uninstall_right_click",
                        action="store_true",
                        help="Uninstall the right-click context menu functionalities. NOTE: this feature is only available on Windows.")

    args = parser.parse_args()

    # Setup logging
    config.set('verbose',args.verbose) #store the desired verbose level in the global config of pdf2bib. This will also automatically update the pdf2bib and pdf2doi logger level.
    logger = logging.getLogger("pdf2bib")

    #If the command -install--right--click was specified, it sets the right keys in the system registry
    if args.install_right_click:
        config.set('verbose',True)
        import pdf2bib.utils_registry as utils_registry
        utils_registry.install_right_click()
        return
    if args.uninstall_right_click:
        config.set('verbose',True)
        import pdf2bib.utils_registry as utils_registry
        utils_registry.uninstall_right_click()
        return

    ## The following block of code (until ##END) is required to make sure that 'path' is a required parameter, except for the case when
    ## -install--right--click or -uninstall--right--click are used
    if isinstance(args.path,list):
        if len(args.path)>0:
            target = args.path[0]
        else:
            target = ""
    else:
        target = args.path

    if target == "":
        print("pdf2bib: error: the following arguments are required: path. Type \'pdf2bib --h\' for a list of commands.")
        return
    ## END
    
    config.set('save_identifier_metadata', not (args.no_store_identifier_metadata))
    pdf2doi.config.set('save_identifier_metadata',config.get('save_identifier_metadata')) 

    str_savebibtex = f"All bibtex entries found in {target} will be stored in the file {args.filename_bibtex }.\n" if args.filename_bibtex else ''
    str_copybibtex = f"All bibtex entries found in will be copied into the system clipboard.\n" if  args.save_bibtex_clipboard else ''
    if str_savebibtex or str_copybibtex:
        print(f"{str_savebibtex} {str_copybibtex}")
    if(args.verbose==False):
        print(f"(All intermediate output will be suppressed. To see additional outuput, use the command -v)")
    results = pdf2bib(target=target)
    

    if not results:
        return
    if not isinstance(results,list):
        results = [results]
    #logger.info('The following files were analyzed:')
    #for result in results:
    #    if result['identifier']:
    #        logger.info('{:<15s} {:<40s} {:<10s}\n'.format(result['identifier_type'], result['identifier'],result['path']) ) 
    #    else:
    #        logger.info('{:<15s} {:<40s} {:<10s}\n'.format('n.a.', 'n.a.',result['path']) ) 
    if not(args.filename_bibtex or args.save_bibtex_clipboard): #If the user wants to save the bibtex entries on file or on the clipboard, we dont show them in the command prompt
        for result in results:
            if result['identifier']:
                print(result['bibtex']) 

    # We call the function save_bibtex_entries. If args.filename_bibtex is a valid string, it will save all found identifiers in a text file with that name.
    # If args.save_doi_clipboard is true, it will copy all identifiers into the clipboard
    save_bibtex_entries(args.filename_bibtex, results, args.save_bibtex_clipboard)  

    return

if __name__ == '__main__':
    main()
