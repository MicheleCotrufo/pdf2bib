# pdf2bib

```pdf2bib``` is a Python library/command-line tool to extract bibliographic information from the .pdf file of a publication 
(or from a folder containing several .pdf files), and automatically generate BibTeX entries. The pdf file can be either a paper published in a scientific journal (i.e. with
a DOI associated to it), or an [arXiv](https://arxiv.org/about/donate) preprint. The bibliographic information is retrieved by querying public archives, thus **an internet connection is required**.

```pdf2bib``` can be used either from [command line](#command-line-usage), or inside your [python script](#usage-inside-a-python-script) or, only for Windows, directly from the [right-click context menu](#installing-the-shortcuts-in-the-right-click-context-menu-of-windows) of a pdf file or a folder.

[![Downloads](https://pepy.tech/badge/pdf2bib)](https://pepy.tech/project/pdf2bib?versions=1.0.2&versions=1.1&versions=1.2)[![Downloads](https://pepy.tech/badge/pdf2bib/month)](https://pepy.tech/project/pdf2bib?versions=1.0.2&versions=1.1&versions=1.2)
[![Pip Package](https://img.shields.io/pypi/v/pdf2bib?logo=PyPI)](https://pypi.org/project/pdf2bib?versions=1.2)

## Warning
```pdf2bib``` uses ```pdf2doi``` to find the DOI of a paper. Versions of ```pdf2doi``` prior to the **1.6** are affected by a very annoying bug. By default, after finding the DOI of a pdf paper, ```pdf2doi``` will store the DOI into the metadata of the pdf file. Due to a bug, the size of the pdf file doubles everytime that a metadata was added. This bug has been fixed in all versions of ```pdf2doi``` >= 1.6. 

If you have pdf files that have been affected by this bug, you can use ```pdf2doi``` to fix it. After updating ```pdf2doi``` to a version > 1.6, run ```pdf2doi path/to/folder/containing/pdf/files -id ''```. This will restore the pdf files to their original size.

Thanks Ole Steuernagel for pointing out this issue.


## Latest stable version
The latest stable version of ```pdf2bib``` is the **1.2**. See [here](https://github.com/MicheleCotrufo/pdf2bib/releases) for the full change log.

### [v1.2] - 2024-06-18

#### Main changes
- Added the CLI option ```-nostore```, which allows the user to opt out of the default behaviour of ```pdf2doi``` regarding storing the found identifier into the pdf metadata. When ```-nostore``` is added to the CLI invokation of ```pdf2bib```, the pdf files will not be modified by ```pdf2doi```.

#### Added
- Make sure entry id can not contain commas https://github.com/MicheleCotrufo/pdf2bib/pull/8.
- Make sure that the input variable target is converted to a string before processing, and Fix trailing colon for some PDF files https://github.com/MicheleCotrufo/pdf2bib/pull/16.


## Installation

Use the package manager pip to install pdf2bib.

```bash
pip install pdf2bib==1.2
```

Under Windows, it is also possible to add [shortcuts to the right-click context menu](#installing-the-shortcuts-in-the-right-click-context-menu-of-windows).



## Table of Contents
 - [Installation](#installation)
 - [Description](#description)
 - [Usage](#usage)
    * [Command line usage](#command-line-usage)
        + [Creating a bib file from a folder](#creating-a-bib-file-from-a-folder)
        + [Manually associate the correct identifier to a file from command line](#manually-associate-the-correct-identifier-to-a-file-from-command-line)
    * [Usage inside a python script](#usage-inside-a-python-script)
        + [Manually associate the correct identifier to a file](#manually-associate-the-correct-identifier-to-a-file)
 - [Installing the shortcuts in the right-click context menu of Windows](#installing-the-shortcuts-in-the-right-click-context-menu-of-windows)
  -[Contributing](#contributing)
 - [License](#license)
 - [Acknowledgment](#acknowledgment)
 - [Donating](#donating)


## Description
```pdf2bib``` relies on the library [pdf2doi](https://github.com/MicheleCotrufo/pdf2doi), which can automatically find a valid identifier of a scientific publication (i.e. either a DOI or an arxiv ID)
starting from a .pdf file. ```pdf2doi``` will query public archives (e.g., http://dx.doi.org for DOIs and http://export.arxiv.org for arxiv IDs) in order to validate any identifier found. The validation process returns raw BibTeX data (see also [here](https://github.com/MicheleCotrufo/pdf2doi#usage-inside-a-python-script)), which is then used by
```pdf2bib``` to generate a valid BibTeX entry in the format
```
@article{[LastNameFirstAuthor][PublicationYear][FirstWordTitle],
        title = ...,
        volume = ...,
        issue = ...,
        page = ...,
        publisher = ...,
        url = ...,
        doi = ...,
        journal = ...,
        year = ...,
        month = ...,
        author = ...
}
```
In the current version the format of the BibTeX entry is not customizable by the user (unless you want to change the code - have fun :D),
but this functionality will be implemented in future realeses.

## Usage

```pdf2bib``` can be used either as a [stand-alone application](#command-line-usage) invoked from the command line, or by [importing it in your python project](#usage-inside-a-python-script) or, only for Windows, 
directly from the [right-click context menu](#installing-the-shortcuts-in-the-right-click-context-menu-of-windows) of a pdf file or a folder.

### Command line usage
```pdf2bib``` can be invoked directly from the command line, without having to open a python console.
The simplest command-line invokation is

```bash
pdf2bib 'path/to/target'
```
where ```target``` is either a valid pdf file or a directory containing pdf files. Adding the optional command '-v' increases the output verbosity,
documenting all steps.
For example, when targeting the folder [examples](/examples) we get the following output

```bash
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

```bash
pdf2bib examples -s bibtex.txt -clip
All available bibtex entries have been stored in the file bibtex.txt
All available bibtex entries have been stored in the system clipboard
```

A list of all optional arguments can be generated by ```pdf2bib --h```
```bash
pdf2bib --h
usage: pdf2bib [-h] [-v] [-nostore] [-s FILENAME_BIBTEX] [-clip] [-install--right--click] [-uninstall--right--click]
               [path ...]

Generate BibTeX entries of scientific publications starting from the pdf files. It requires an internet connection.

positional arguments:
  path                  Relative path of the target pdf file or of the targe folder.

options:
  -h, --help            show this help message and exit
  -v, --verbose         Increase verbosity. By default (i.e. when not using -v), only the text of the found bibtex
                        entries will be printed as output.
  -nostore, --no_store_identifier_metadata
                        pdf2bib uses the library pdf2doi to find the DOI/identifier of a publication. By default,
                        anytime an identifier is found, pdf2doi also adds it to the metadata of the pdf file (if not
                        present yet). By using this additional option, the identifier is not stored in the file
                        metadata.
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

#### Creating a bib file from a folder
```pdf2bib``` can be used to quickly generate a .bib file containining the BibTeX entries of all pdf files in a target folder, via the command

```bash
pdf2bib 'path\\to\\target\\folder' -s bibtex.bib
```
The generated .bib file can be imported into other software, such as [Zotero](https://www.zotero.org), to generate bibliograpies for, e.g. Microsoft Word.


#### Manually associate the correct identifier to a file from command line
Occasionally, the BibTeX generation process will fail (or give wrong results) if the library ```pdf2doi``` (which ```pdf2bib``` relies on to find a valid publication identifier)
fails to  retrieve a DOI/identifier (or maybe it retrives the uncorrect one). This problem can be fixed
by looking for the DOI/identifier manually and add it to the pdf metadata, by using ```pdf2doi``` as described [here](https://github.com/MicheleCotrufo/pdf2doi#manually-associate-the-correct-identifier-to-a-file-from-command-line).
In this way, any future use of ```pdf2bib``` on this file will always retrieve the correct BibTeX infos. 

### Usage inside a python script
```pdf2bib``` can also be used as a library within a python script. The function ```pdf2bib.pdf2bib``` is the main point of entry. 
The first input argument must be a valid path (either absolute or relative) to a pdf file or to a folder containing pdf files. 
The same settings available in the command line operation (see above), are now available via the methods ```set``` and ```get``` of the object ```pdf2bib.config```
For example, we can scan the folder [examples](/examples) with reduced output verbosity, 

```python
>>> import pdf2bib
>>> pdf2bib.config.set('verbose',False)
>>> path = r'.\examples'
>>> result = pdf2bib.pdf2bib(path)
>>> print(result[0]['metadata'])
>>> print('\n')
>>> print(result[0]['bibtex'])
{'title': "An efficient numerical evaluation of the Green's function for the Helmholtz operator on periodic structures", 'volume': '63', 'issue': '1', 'page': '222-235', 'publisher': 'Elsevier BV', 'url': 'http://dx.doi.org/10.1016/0021-9991(86)90093-8', 'doi': '10.1016/0021-9991(86)90093-8', 'journal': 'Journal of Computational Physics', 'year': 1986, 'month': 3, 'author': 'Kirk E Jordan and Gerard R Richter and Ping Sheng', 'ENTRYTYPE': 'article'}


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
```

The output of the function ```pdf2bib.pdf2bib``` is a list of dictionaries (or just a single dictionary if a single file was targeted). 
Each dictionary has the following keys

```
result['identifier']        = DOI or other identifier (or None if nothing is found)
result['identifier_type']   = string specifying the type of identifier (e.g. 'doi' or 'arxiv')
result['path']              = path of the pdf file
result['method']            = method used by pdf2doi to find the identifier
result['validation_info']   = Raw BibTeX data.
result['metadata']          = Dictionary containing bibtex info
result['bibtex']            = A string containing a valid bibtex entry
```

The element ```result['metadata']``` is a dictionary containing the most typical bibtex infos. 
The specific keys contained in this dictionary, and their format, will depend on several factors, such as (1) if the paper was associated to a DOI or to an arxiv ID, 
(2) which method was used by ```pdf2doi``` to validate the paper identifier, and (3) which data is available for this paper in the relevant archive. 
When the paper is associate to a DOI, the ```result['metadata']``` dictionary will always contain at least the keys  ```'title', 'author', 'journal', 'volume', 'issue', 'page', 'publisher', 'url', 'doi', 'year', 'month'```, althought some of them might be empty. When the paper is associated to an arxiv ID, the ```result['metadata']``` dictionary will always contain the keys ```'title', 'author', 'ejournal', 'eprint', 'published', 'url', 'doi','arxiv_doi', 'year', 'month', 'day', 'ENTRYTYPE'```

#### Manually associate the correct identifier to a file
Similarly to what described [above](#manually-associate-the-correct-identifier-to-a-file-from-command-line), it is possible to associate a (manually found) 
identifier to a pdf file also from within python, by using the function ```pdf2doi.add_found_identifier_to_metadata```:

```python
>>> import pdf2doi
>>> pdf2doi.add_found_identifier_to_metadata(path_to_pdf_file, identifier)
``` 

## Installing the shortcuts in the right-click context menu of Windows
This functionality is only available on Windows (and so far it has been tested only on Windows 10). It adds additional commands to the context menu of Windows
which appears when right-clicking on a pdf file or on a folder.

<!--<img src="docs/ContextMenu_pdf.png" width="550" /><img src="docs/ContextMenu_folder.png" width="550" />-->

The  menu commands allow to copy BibTeX entry of a pdf file (or all pdf files contained in a folder) into the system clipboard.

<!--<img src="docs/ContextMenu_pdf.gif" width="500" />-->

To install this functionality, first install ```pdf2bib``` via pip (as described above), then open a command prompt **with administrator rights** and run
```
$ pdf2bib  -install--right--click
```
To remove it, simply run (again from a terminal with administrator rights)
```
$ pdf2bib  -uninstall--right--click
```
If it is not possible to run this command from a terminal with administrator rights, the batch files
[here](/right_click_menu_installation) can be alternatively used (see readme.MD file in the same folder for instructions), although it is still required to have 
admnistrator rights.

NOTE: when multiple pdf files are selected, and the right-click context menu commands are used, ```pdf2bib``` will be called separately for each file, and thus
only the BibTeX entry of the last file will be stored in the clipboard. In order to copy the info of multiple files it is necessary to save them in a folder and right-click on the folder.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgment
I am thankful to my friend and colleague Yarden Mazor for leading the beta-testing efforts for this project.

## Donating
If you find this library useful (or amazing!), please consider making donations on my behalf to organizations that advocate for and promote free dissemination of science, such as

[arXiv](https://arxiv.org/about/donate)

[Sci-Hub](https://sci-hub.se/donate)

[Wikipedia](https://donate.wikimedia.org/)

## License
[MIT](https://choosealicense.com/licenses/mit/)
