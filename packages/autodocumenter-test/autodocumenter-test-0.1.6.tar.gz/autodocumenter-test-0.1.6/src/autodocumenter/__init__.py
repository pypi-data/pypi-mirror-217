import os
import sys

__version__ = "0.1.6"

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from .generate_doc import generate_doc
from .compile_doc import compile_doc
