"""
.. include:: ../../README.md
"""

import importlib.metadata
import logging
import os

from dotenv import load_dotenv
from termcolor import colored

from .benchmarker import Benchmarker  # noqa
from .utils import block_terminal_output

# Fetches the version of the package as defined in pyproject.toml
__version__ = importlib.metadata.version(__package__)


# Block unwanted terminal outputs
block_terminal_output()


# Loads environment variables
load_dotenv()


# Set up logging
fmt = colored("%(asctime)s [%(levelname)s] <%(name)s>\n↳ ", "green") + colored(
    "%(message)s", "yellow"
)
logging.basicConfig(level=logging.INFO, format=fmt)


# Disable parallelisation when tokenizing, as that can lead to errors
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# Enable MPS fallback
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
