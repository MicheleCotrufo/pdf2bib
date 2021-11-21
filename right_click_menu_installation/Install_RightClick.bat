set path_pdf2bib=D:\Dropbox (Personal)\PythonScripts\env2\Scripts

REG ADD "HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\pdf2bib" /f
REG ADD "HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\pdf2bib" /v "MUIVerb" /t REG_SZ /d "pdf2bib" /f
REG ADD "HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\pdf2bib" /v "subcommands" /t REG_SZ /d "" /f
REG ADD "HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\pdf2bib\shell" /f

REG ADD "HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\pdf2bib\shell\pdf2bib_copybibtex" /t REG_SZ /d "Retrieve and copy bibtex entry of this file..." /f
REG ADD "HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\pdf2bib\shell\pdf2bib_copybibtex\command" /t REG_SZ /d "%path_pdf2bib%\pdf2bib.exe \"%%1\" -clip -v" /f

REG ADD "HKEY_CLASSES_ROOT\Directory\shell\pdf2bib" /f
REG ADD "HKEY_CLASSES_ROOT\Directory\shell\pdf2bib" /v "MUIVerb" /t REG_SZ /d "pdf2bib" /f
REG ADD "HKEY_CLASSES_ROOT\Directory\shell\pdf2bib" /v "subcommands" /t REG_SZ /d "" /f
REG ADD "HKEY_CLASSES_ROOT\Directory\shell\pdf2bib\shell" /f

REG ADD "HKEY_CLASSES_ROOT\Directory\shell\pdf2bib\shell\pdf2bib_copybibtex" /t REG_SZ /d "Retrieve and copy bibtex entries of all pdf files in this folder..." /f
REG ADD "HKEY_CLASSES_ROOT\Directory\shell\pdf2bib\shell\pdf2bib_copybibtex\command" /t REG_SZ /d "%path_pdf2bib%\pdf2bib.exe \"%%1\" -clip -v" /f