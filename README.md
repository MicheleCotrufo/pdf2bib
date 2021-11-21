# pdf2bib

pdf2bib is a Python library to automatically extract bibliographic information from the .pdf file of a publication 
(or from a folder containing several .pdf files), and generate BibTeX entries. The pdf file can be either a paper published in a scientific journal (i.e. with
a DOI associated to it), or an arxiv preprint.
It uses the library [pdf2doi](https://github.com/MicheleCotrufo/pdf2doi) to first find a valid identifier of the publication (i.e. either a DOI or an arxiv ID),
and then uses this identifier to query public archives (e.g. http://dx.doi.org) to obtain bibliographic data.

pdf2bib can be used either from [command line](#command-line-usage), or inside your [python script](#usage-inside-a-python-script) or, only for Windows, directly from the [right-click context menu](#installing-the-shortcuts-in-the-right-click-context-menu-of-windows) of a pdf file or a folder.


## Installation

Use the package manager pip to install pdf2bib.

```bash
pip install pdf2bib==1.0rc2
```

Under Windows, it is also possible to add [shortcuts to the right-click context menu](#installing-the-shortcuts-in-the-right-click-context-menu-of-windows).

<!--
<img src="docs/ContextMenu_pdf.gif" width="500" />

[![Downloads](https://pepy.tech/badge/pdf2doi)](https://pepy.tech/project/pdf2doi?versions=0.4&versions=0.5&versions=0.6)[![Downloads](https://pepy.tech/badge/pdf2doi/month)](https://pepy.tech/project/pdf2doi?versions=0.4&versions=0.5&versions=0.6)
[![Pip Package](https://img.shields.io/pypi/v/pdf2doi?logo=PyPI)](https://pypi.org/project/pdf2doi)
-->
## Table of Contents
 - [Installation](#installation)
 - [Description](#description)
 - [Usage](#usage)
    * [Command line usage](#command-line-usage)
        + [Manually associate the correct identifier to a file from command line](#manually-associate-the-correct-identifier-to-a-file-from-command-line)
    * [Usage inside a python script](#usage-inside-a-python-script)
 - [Installing the shortcuts in the right-click context menu of Windows](#installing-the-shortcuts-in-the-right-click-context-menu-of-windows)
  -[Contributing](#contributing)
 - [License](#license)
 - [Acknowledgment](#acknowledgment)
 - [Donating](#donating)


## Description

The online validation of an identifier relies on performing queries to different online archives 
(e.g., http://dx.doi.org for DOIs and http://export.arxiv.org for arxiv IDs). Using data obtained from these queries, a bibtex entry can be automatically created.
By using the optional argument ```-b filename```, a list of bibtex entries for all the pdf files in the targeted folder is stored in a text file within the same folder. 
For example, if target is the folder [examples](/examples), the command
```
$ pdf2doi ".\examples" -b "bibtex.txt"
```
creates the file [bibtex.txt](/examples/bibtex.txt) inside the same folder. 

[TO DO]


## Usage

pdf2bib can be used either as a [stand-alone application](#command-line-usage) invoked from the command line, or by [importing it in your python project](#usage-inside-a-python-script) or, only for Windows, 
directly from the [right-click context menu](#installing-the-shortcuts-in-the-right-click-context-menu-of-windows) of a pdf file or a folder.

### Command line usage
```pdf2bib``` can be invoked directly from the command line, without having to open a python console.
The simplest command-line invokation is

```
$ pdf2doi 'path/to/target'
```
where ```target``` is either a valid pdf file or a directory containing pdf files. Adding the optional command '-v' increases the output verbosity,
documenting all steps.
For example, when targeting the folder [examples](/examples) we get the following output

```
pdf2bib examples -v
[pdf2bib]: Looking for pdf files in the folder examples...
[pdf2bib]: Found 4 pdf files.
[pdf2bib]: ................
[pdf2bib]: Trying to extract data to generate the BibTeX entry for the file: examples\1-s2.0-0021999186900938-main.pdf
[pdf2bib]: Calling pdf2doi...
[pdf2doi]: Method #1: Looking for a valid identifier in the document infos...
[pdf2doi]: Validating the possible DOI 10.1016/0021-9991(86)90093-8 via a query to dx.doi.org...
[pdf2doi]: The DOI 10.1016/0021-9991(86)90093-8 is validated by dx.doi.org.
[pdf2doi]: A valid DOI was found in the document info labelled '/identifier'.
[pdf2bib]: pdf2doi found a valid identifier for this paper. Trying to parse the data obtained by pdf2doi into valid BibTeX data..
[pdf2bib]: A valid BibTeX entry was generated.
[pdf2bib]: ................
[pdf2bib]: Trying to extract data to generate the BibTeX entry for the file: examples\chaumet_JAP_07.pdf
[pdf2bib]: Calling pdf2doi...
[pdf2doi]: Method #1: Looking for a valid identifier in the document infos...
[pdf2doi]: Validating the possible DOI 10.1063/1.2409490 via a query to dx.doi.org...
[pdf2doi]: The DOI 10.1063/1.2409490 is validated by dx.doi.org.
[pdf2doi]: A valid DOI was found in the document info labelled '/identifier'.
[pdf2bib]: pdf2doi found a valid identifier for this paper. Trying to parse the data obtained by pdf2doi into valid BibTeX data..
[pdf2bib]: A valid BibTeX entry was generated.
[pdf2bib]: ................
[pdf2bib]: Trying to extract data to generate the BibTeX entry for the file: examples\PhysRevLett.116.061102.pdf
[pdf2bib]: Calling pdf2doi...
[pdf2doi]: Method #1: Looking for a valid identifier in the document infos...
[pdf2doi]: Validating the possible DOI 10.1103/PhysRevLett.116.061102 via a query to dx.doi.org...
[pdf2doi]: The DOI 10.1103/PhysRevLett.116.061102 is validated by dx.doi.org.
[pdf2doi]: A valid DOI was found in the document info labelled '/identifier'.
[pdf2bib]: pdf2doi found a valid identifier for this paper. Trying to parse the data obtained by pdf2doi into valid BibTeX data..
[pdf2bib]: A valid BibTeX entry was generated.
[pdf2bib]: ................
[pdf2bib]: Trying to extract data to generate the BibTeX entry for the file: examples\s41586-019-1666-5.pdf
[pdf2bib]: Calling pdf2doi...
[pdf2doi]: Method #1: Looking for a valid identifier in the document infos...
[pdf2doi]: Validating the possible DOI 10.1038/s41586-019-1666-5 via a query to dx.doi.org...
[pdf2doi]: The DOI 10.1038/s41586-019-1666-5 is validated by dx.doi.org.
[pdf2doi]: A valid DOI was found in the document info labelled '/doi'.
[pdf2bib]: pdf2doi found a valid identifier for this paper. Trying to parse the data obtained by pdf2doi into valid BibTeX data..
[pdf2bib]: A valid BibTeX entry was generated.
[pdf2bib]: ................
@article{jordan1986an,
        title = {An efficient numerical evaluation of the Green's function for the Helmholtz operator on periodic structures},
        volume = {63},
        issue = {1},
        page = {222-235},
        publisher = {Elsevier BV},
        url = {http://dx.doi.org/10.1016/0021-9991(86)90093-8},
        doi = {10.1016/0021-9991(86)90093-8},
        journal = {Journal of Computational Physics},
        year = {1986},
        month = {3},
        author = {Kirk E Jordan and Gerard R Richter and Ping Sheng}
}
@article{chaumet2007coupled,
        title = {Coupled dipole method to compute optical torque: Application to a micropropeller},
        volume = {101},
        issue = {2},
        page = {023106},
        publisher = {AIP Publishing},
        url = {http://dx.doi.org/10.1063/1.2409490},
        doi = {10.1063/1.2409490},
        journal = {Journal of Applied Physics},
        year = {2007},
        month = {1},
        author = {Patrick C. Chaumet and C. Billaudeau}
}
@article{2016observation,
        title = {Observation of Gravitational Waves from a Binary Black Hole Merger},
        volume = {116},
        issue = {6},
        publisher = {American Physical Society (APS)},
        url = {http://dx.doi.org/10.1103/PhysRevLett.116.061102},
        doi = {10.1103/physrevlett.116.061102},
        journal = {Physical Review Letters},
        year = {2016},
        month = {2}
}
@article{arute2019quantum,
        title = {Quantum supremacy using a programmable superconducting processor},
        volume = {574},
        issue = {7779},
        page = {505-510},
        publisher = {Springer Science and Business Media LLC},
        url = {http://dx.doi.org/10.1038/s41586-019-1666-5},
        doi = {10.1038/s41586-019-1666-5},
        journal = {Nature},
        year = {2019},
        month = {10},
        author = {Frank Arute and Kunal Arya and Ryan Babbush and Dave Bacon and Joseph C. Bardin and Rami Barends and Rupak Biswas and Sergio Boixo and Fernando G. S. L. Brandao and David A. Buell and Brian Burkett and Yu Chen and Zijun Chen and Ben Chiaro and Roberto Collins and William Courtney and Andrew Dunsworth and Edward Farhi and Brooks Foxen and Austin Fowler and Craig Gidney and Marissa Giustina and Rob Graff and Keith Guerin and Steve Habegger and Matthew P. Harrigan and Michael J. Hartmann and Alan Ho and Markus Hoffmann and Trent Huang and Travis S. Humble and Sergei V. Isakov and Evan Jeffrey and Zhang Jiang and Dvir Kafri and Kostyantyn Kechedzhi and Julian Kelly and Paul V. Klimov and Sergey Knysh and Alexander Korotkov and Fedor Kostritsa and David Landhuis and Mike Lindmark and Erik Lucero and Dmitry Lyakh and Salvatore Mandrà and Jarrod R. McClean and Matthew McEwen and Anthony Megrant and Xiao Mi and Kristel Michielsen and Masoud Mohseni and Josh Mutus and Ofer Naaman and Matthew Neeley and Charles Neill and Murphy Yuezhen Niu and Eric Ostby and Andre Petukhov and John C. Platt and Chris Quintana and Eleanor G. Rieffel and Pedram Roushan and Nicholas C. Rubin and Daniel Sank and Kevin J. Satzinger and Vadim Smelyanskiy and Kevin J. Sung and Matthew D. Trevithick and Amit Vainsencher and Benjamin Villalonga and Theodore White and Z. Jamie Yao and Ping Yeh and Adam Zalcman and Hartmut Neven and John M. Martinis}
}
```
Every line which begins with '[pdf2doi]' or '[pdf2bib]' is omitted when the optional command '-v' is absent. It is also possible to store all bibtex entries into
a text file, or into the system clipboard, by using the optional arguments ```-s FILENAME_BIBTEX``` and ```-clip```

```
$ pdf2bib examples -s bibtex.txt -clip
All available bibtex entries have been stored in the file bibtex.txt
All available bibtex entries have been stored in the system clipboard
```

A list of all optional arguments can be generated by ```pdf2bib --h```
```
$ pdf2bib --h
usage: pdf2bib [-h] [-v] [-s FILENAME_BIBTEX] [-clip] [-install--right--click] [-uninstall--right--click]
               [path [path ...]]

Generate BibTeX entries of scientific publications starting from the pdf files. It requires an internet connection.

positional arguments:
  path                  Relative path of the target pdf file or of the targe folder.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase verbosity. By default (i.e. when not using -v), only the text of the found bibtex
                        entries will be printed as output.
  -s FILENAME_BIBTEX, --make_bibtex_file FILENAME_BIBTEX
                        Create a text file inside the target directory, with name given by FILENAME_BIBTEX, containing
                        the bibtex entry of each pdf file in the target folder (if any is found).
  -clip, --save_bibtex_clipboard
                        Store all found bibtex entries into the clipboard.
  -install--right--click
                        Add a shortcut to pdf2bib in the right-click context menu of Windows. This allows you to copy
                        the bibtex entry of a pdf file (or all pdf files in a folder) into the clipboard by just right
                        clicking on it! NOTE: this feature is only available on Windows.
  -uninstall--right--click
                        Uninstall the right-click context menu functionalities. NOTE: this feature is only available
                        on Windows.
```

#### Manually associate the correct identifier to a file from command line
Occasionally, the BibTeX generation process will fail (or give wrong results) if the library ```pdf2doi``` (which ```pdf2bib``` relies on to find a valid publication identifier)
fails to  retrieve a DOI/identifier (or maybe it retrives the uncorrect one). This problem can be fixed
by looking for the DOI/identifier manually and add it to the pdf metadata, by using ```pdf2doi``` as described [here](https://github.com/MicheleCotrufo/pdf2doi#manually-associate-the-correct-identifier-to-a-file-from-command-line).
In this way, any future use of ```pdf2bib``` on this file will always retrieve the correct BibTeX infos. 

### Usage inside a python script
```pdf2doi``` can also be used as a library within a python script. The function ```pdf2doi.pdf2doi``` is the main point of entry. It looks for the identifier of a pdf file by applying all the available methods. 
The first input argument must be a valid path (either absolute or relative) to a pdf file or to a folder containing pdf files. 
Setting the optional argument ```verbose=True``` will increase the output verbosity, documenting all steps performed by the library. Using as a test the folder [examples](/examples), 

```python
>>> from pdf2doi import pdf2doi
>>> results = pdf2doi('.\examples',verbose=False)
```

The output of the function ```pdf2doi``` is a list of dictionaries (or just a single dictionary if a single file was targeted). Each dictionary has the following keys

```
result['identifier'] = DOI or other identifier (or None if nothing is found)
result['identifier_type'] = string specifying the type of identifier (e.g. 'doi' or 'arxiv')
result['validation_info'] = Additional info on the paper. If online validation of identifier is set to True (as default), then result['validation_info']
                            will contain a bibtex entry for this paper. Otherwise it will just contain True.
result['bibtex_data'] = dictionary containing all available bibtex info of this publication. E.g., result['bibtex_info']['author'], result['bibtex_info']['title'], etc.
result['path'] = path of the pdf file
result['method'] = method used to find the identifier
```
For example, the DOIs/identifiers of each file can be printed by
```
>>> for result in results:
>>>     print(result['identifier'])
10.1016/0021-9991(86)90093-8
10.1063/1.2409490
10.1103/PhysRevLett.116.061102
10.1038/s41586-019-1666-5
```
Additional optional arguments can be passed to the function ```pdf2doi.pdf2doi``` to control its behaviour, for example to specify if
web-based methods (either to find an identifier and/or to validate it) should not be used.

```python
def pdf2doi(target, verbose=False, websearch=True, webvalidation=True,
            save_identifier_metadata = config.save_identifier_metadata,
            numb_results_google_search = config.numb_results_google_search,
            filename_identifiers = False, filename_bibtex = False,
            store_bibtex_clipboard = False, store_identifier_clipboard = False):
    '''
    Parameters
    ----------
    target : string
        Relative or absolute path of a .pdf file or a directory containing pdf files
    verbose : boolean, optional
        Increases the output verbosity. The default is False.
    websearch : boolean, optional
        If set false, any method to find an identifier which requires a web search is disabled. The default is True.
    webvalidation : boolean, optional
        If set false, validation of identifiers via internet queries (e.g. to dx.doi.org or export.arxiv.org) is disabled. 
        The default is True.
    save_identifier_metadata : boolean, optional
        If set True, when a valid identifier is found with any method different than the metadata lookup, the identifier
        is also written in the file metadata with key "/identifier" (this will speed up future lookup of thi same file). 
        If set False, this does not happen. The default is True.
    numb_results_google_search : integer, optional
        It sets how many results are considered when performing a google search. The default is config.numb_results_google_search.
    filename_identifiers : string or boolean, optional
        If set equal to a string, all identifiers found in the directory specified by target are saved into a text file 
        inside the same directory and with a name specified by filename_identifiers. 
        The default is False.  It is ignored if the input parameter target is a file.
    filename_bibtex : string or boolean, optional
        If set equal to a string, all bibtex entries obtained in the validation process for all pdf files found in the 
        directory specified by target are saved into a file inside the same directory and with a name specified by filename_bibtex. 
        The default is False. It is ignored if the input parameter target is a file.
    store_bibtex_clipboard : boolean, optional
        If set true, the bibtex entries of all pdf files (or a for a single pdf file if target is a file) are
        stored in the system clipboard. The default is False. 
    store_identifier_clipboard : boolean, optional
        If set true, the identifier of all pdf files (or a for a single pdf file if target is a file) are
        stored in the system clipboard. The default is False. 
        If both store_bibtex_clipboard and store_identifier_clipboard are set to true, the bibtex entries have 
        priority.
    '''
```

By default, everytime that a valid DOI/identifier is found, it is stored in the metadata of the pdf file. In this way, subsequent lookups of the same folder/file will be much faster.
This behaviour can be removed (e.g. if the user does not want or cannot edit the files) by setting the optional argument  ```save_identifier_metadata = False```

#### Generate list of bibtex entries
Similarly to the [command line](#generate-list-of-bibtex-entries-from-command-line) approach, the function ```pdf2doi.pdf2doi``` can be used
to generate bibtex entries and save them on file. By setting the input argument ```filename_bibtex``` equal to a 
valid filename, the bibtex entries of all files in the target directory will be saved in a file within the same directory. For example,

```python
>>> from pdf2doi import pdf2doi
>>> results = pdf2doi('.\examples', filename_bibtex='bibtex.txt')
```
creates the file [bibtex.txt](/examples/bibtex.txt) in the 'examples' folder. 

#### Manually associate the correct identifier to a file
Similarly to what described [above](#manually-associate-the-correct-identifier-to-a-file-from-command-line), it is possible to associate a (manually found) 
identifier to a pdf file also from within python, by using the function ```pdf2doi.add_found_identifier_to_metadata```:

```python
>>> import pdf2doi
>>> pdf2doi.add_found_identifier_to_metadata(path_to_pdf_file, identifier)
```
this creates a new metadata in the pdf file with label '/identifier' and containing the string ```identifier```.  

## Installing the shortcuts in the right-click context menu of Windows
This functionality is only available on Windows (and so far it has been tested only on Windows 10). It adds additional commands to the context menu of Windows
which appears when right-clicking on a pdf file or on a folder.

<img src="docs/ContextMenu_pdf.png" width="550" /><img src="docs/ContextMenu_folder.png" width="550" />

The different menu commands allow to copy the paper(s) identifier(s) or bibtex entry(ies) into the system clipboard, or also to manually
set the identifier of a pdf file (see also [here](#manually-associate-the-correct-identifier-to-a-file-from-command-line)).

<img src="docs/ContextMenu_pdf.gif" width="500" />

To install this functionality, first install ```pdf2doi``` via pip (as described above), then open a command prompt **with administrator rights** and execute
```
$ pdf2doi  -install--right--click
```
To remove it, simply run (again from a terminal with administrator rights)
```
$ pdf2doi  -uninstall--right--click
```
If it is not possible to run this command from a terminal with administrator rights, the batch files
[here](/right_click_menu_installation) can be alternatively used (see readme.MD file in the same folder for instructions), although it is still required to have 
admnistrator rights.

NOTE: when multiple pdf files are selected, and the right-click context menu commands are used, ```pdf2doi``` will be called separately for each file, and thus
only the info of the last file will be stored in the clipboard. In order to copy the info of multiple files it is necessary to save them in a folder and right-click on the folder.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgment
I am thankful to my friend and colleague Yarden Mazor for leading the beta-testing efforts for this project.

## Donating
If you find this library useful (or amazing!), please consider making donations on my behalf to organizations that advocate for and promote free dissemination of science, such as

[Arxiv](https://arxiv.org/about/donate)

[Sci-Hub](https://sci-hub.se/donate)

[Wikipedia](https://donate.wikimedia.org/)

## License
[MIT](https://choosealicense.com/licenses/mit/)
