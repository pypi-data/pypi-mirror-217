import os
from utils.constants import ignore_list_global


def edit_reference(file_path, code_root, ignore_list=[]):
    content = f"""
Code Reference
==============

.. autosummary::
   :toctree: _autosummary
   :recursive:

"""
    # Add top-level directories that are not in the ignore list or
    for item in os.listdir(code_root):
        if item not in ignore_list and item not in ignore_list_global:
            if os.path.isdir(os.path.join(code_root, item)):
                content += "   " + item + "\n"

    with open(file_path, "w") as f:
        f.write(content)

