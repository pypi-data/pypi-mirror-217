import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from .compile_doc import compile_doc

from .utils.edit_config import edit_config
from .utils.edit_index import edit_index
from .utils.edit_reference import edit_reference
from .utils.edit_user_guide import edit_user_guide