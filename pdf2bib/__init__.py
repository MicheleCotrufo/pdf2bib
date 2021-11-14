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

from .main import pdf2bib
from .bibtex_makers import *
#from .utils_registry import install_right_click, uninstall_right_click


