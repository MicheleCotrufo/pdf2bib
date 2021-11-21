import logging

# Setup logging
logger = logging.getLogger("pdf2bib")
logger.setLevel(level=logging.INFO)
if not logger.handlers:
    formatter = logging.Formatter("[pdf2bib]: %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
logger.propagate = False

from .config import config
config.ReadParamsINIfile()

config.set('verbose',config.get('verbose')) #This is a quick and dirty way (to improve in the future) to make sure that the verbosity of the pdf2bib and pdf2doi loggers is properly set according
                                            #to the current value of config.get('verbose') (see config.py file for details)
from .main import pdf2bib, pdf2bib_singlefile
from .bibtex_makers import *

