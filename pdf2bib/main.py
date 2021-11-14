import argparse
import logging
from os import path, listdir
import pdf2bib.bibtex_makers as bibtex_makers
import pdf2bib.config as config
import pdf2doi
#import pyperclip Modules that are commented here are imported later only when needed, to improve start up time

def pdf2bib(target):
    ''' This is the main routine of the library. When the library is used as a command-line tool (via the entry-point "pdf2bib") 
    ''' 

    # Setup logging
    if config.get('verbose'): loglevel = logging.INFO
    else: loglevel = logging.CRITICAL

    logger = logging.getLogger("pdf2bib")
    logger.setLevel(level=loglevel)

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
    
    #If target is not a directory, we check that it is an existing file and that it ends with .pdf
    else:
        filename = target
        if not path.exists(filename):
            logger.error(f"'{filename}' is not a valid file.")
            return None   
        if not (filename.lower()).endswith('.pdf'):
            logger.error("The file must have .pdf extension.")
            return None
        logger.info(f"Trying to extract data to generate the BibTeX entry for the file: {filename}")  
        logger.info(f"Calling pdf2doi...") 
        result = pdf2doi.pdf2doi_singlefile(filename)
        if result['identifier'] == None:
            logger.error("It was not possible to find a valid identifier for this file.")
        if not isinstance(result['validation_info'],str):
            logger.error("The validation_info returned by pdf2doi is not a string. It is not possible to extract BibTeX data.")
        logger.info(f"Trying to parse the data obtained by pdf2doi into valid BibTeX data..") 
        metadata = pdf2bib_singlefile(result)
        if metadata:
            result['metadata'] = metadata
            result['bibtex'] = bibtex_makers.make_bibtex(metadata)
            logger.info(f"A valid BibTeX entry was generated:") 
            logger.info(result['bibtex'])
            return result 
        else:
            logger.error("Some error occurred when parsing the raw BibTeX data.")

def pdf2bib_singlefile(result):
    '''
    Parameters
    ----------
    result : dictionary
        dictionary obtained via pdf2doi
    Returns
    -------
    ''' 
    
    if result['identifier_type'] == 'DOI':
        metadata = bibtex_makers.parse_bib_from_dxdoiorg(result['validation_info'], method=pdf2doi.config.get('method_dxdoiorg'))
    if result['identifier_type'] == 'arxiv ID':
        metadata = bibtex_makers.parse_bib_from_exportarxivorg(result['validation_info'])
    
    return metadata



def save_bibtex_entries(filename_bibtex, results, clipboard = False):
    ''' Write all bibtex entries contained in the input list 'results' into a text file with a path specified by filename_bibtex 
        (if filename_bibtex is a valid string) and/or into the clipboard (if clipboard = True).
    
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
                logger.info(f'All available bibtex entries have been stored in the file {filename_bibtex}')
        except Exception as e:
            logger.error(e)
            logger.error(f'A problem occurred when trying to write into the file {filename_bibtex}')
    if clipboard:
        import pyperclip
        try:
            pyperclip.copy(text)
            logger.info(f'All available bibtex entries have been stored in the system clipboard')
        except Exception as e:
            logger.error(e)
            logger.error(f'A problem occurred when trying to write into the system clipboard')

    
def main():
    parser = argparse.ArgumentParser( 
            description = "Generate BibTeX entries of scientific publications starting from the pdf files. It requires an internet connection.",
            epilog = "")

    parser.add_argument("path",
                        help = "Relative path of the target pdf file or of the targe folder.",
                        metavar = "path",
                        nargs = '*')
    parser.add_argument("-nv",
                        "--no_verbose",
                        help="Decrease verbosity.",
                        action="store_true")
    parser.add_argument("-s",
                        "--make_bibtex_file",
                        dest="filename_bibtex",
                        help="Create a text file inside the target directory, with name given by FILENAME_BIBTEX, containing the bibtex entry of each pdf file in the target folder (if any is found).",
                        action="store")
    parser.add_argument("-bclip",
                        "--save_bibtex_clipboard",
                        action="store_true",
                        help="Store all found bibtex entries into the clipboard.")
    parser.add_argument("-install--right--click",
                        dest="install_right_click",
                        action="store_true",
                        help="Add a shortcut to pdf2bib in the right-click context menu of Windows. You can copy the bibtex entry of a pdf file (or all pdf files in a folder) into the clipboard by just right clicking on it! NOTE: this feature is only available on Windows.")
    parser.add_argument("-uninstall--right--click",
                        dest="uninstall_right_click",
                        action="store_true",
                        help="Uninstall the right-click context menu functionalities. NOTE: this feature is only available on Windows.")

    args = parser.parse_args()

    # Setup logging
    if not(args.no_verbose): loglevel = logging.INFO
    else: loglevel = logging.CRITICAL

    logger = logging.getLogger("pdf2bib")
    logger.setLevel(level=loglevel)

    #If the command -install--right--click was specified, it sets the right keys in the system registry
    if args.install_right_click:
        import pdf2bib.utils_registry as utils_registry
        utils_registry.install_right_click()
        return
    if args.uninstall_right_click:
        import pdf2bib.utils_registry as utils_registry
        utils_registry.uninstall_right_click()
        return
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

    config.set('verbose',not(args.no_verbose))
 
    results = pdf2bib(target=target)

    if not results:
        return
    if not isinstance(results,list):
        results = [results]
    print('The following files were analyzed:')
    for result in results:
        if result['identifier']:
            print('{:<15s} {:<40s} {:<10s}\n'.format(result['identifier_type'], result['identifier'],result['path']) ) 
        else:
            print('{:<15s} {:<40s} {:<10s}\n'.format('n.a.', 'n.a.',result['path']) ) 

    # We call the function save_bibtex_entries. If args.filename_bibtex is a valid string, it will save all found identifiers in a text file with that name.
    # If args.save_doi_clipboard is true, it will copy all identifiers into the clipboard
    save_bibtex_entries(args.filename_bibtex, results, args.save_bibtex_clipboard)  

    return

if __name__ == '__main__':
    main()