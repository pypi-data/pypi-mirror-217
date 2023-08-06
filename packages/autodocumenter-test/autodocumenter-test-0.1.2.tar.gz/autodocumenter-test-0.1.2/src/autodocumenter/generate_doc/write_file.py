from utils.output import out, err
from .utils.parse_file import (
    check_code_syntax,
)


def write_file(
    file_path,
    tasks,
    verbose=False,
):
    tasks = list(tasks)
    num_function_defs = len([item for item in tasks if item["type"] == "FunctionDef"])
    num_class_defs = len([item for item in tasks if item["type"] == "ClassDef"])
    num_method_defs = len([item for item in tasks if item["type"] == "ClassMethodDef"])

    with open(file_path, "r") as file:
        file_lines = file.readlines()

    file_txt = "".join(file_lines)

    # Save for fallback if the file breaks
    original_file_txt = file_txt

    for data in tasks:
        docstring = '"""\n' + data["response"] + '\n"""\n'
        indentation = "    " + data["col_offset"] * " "
        docstring_lines = docstring.splitlines(keepends=True)
        docstring_lines = [
            indentation + docstring_line for docstring_line in docstring_lines
        ]
        docstring = "".join(docstring_lines)
        hash_placeholder = data["hash_placeholder"]
        file_txt = file_txt.replace(hash_placeholder, docstring)

    syntax_check = check_code_syntax(file_txt)
    # syntax_check = True

    if syntax_check:
        with open(file_path, "w") as f:
            f.write(file_txt)
        if verbose:
            out(
                f"File {file_path} sucessfuly processed! Added docstring for {num_function_defs} functions, {num_class_defs} classes and {num_method_defs} methods."
            )
        return "Success"
    else:
        with open(file_path, "w") as f:
            f.write(original_file_txt)
        err(
            f"File {file_path} unsucessfuly processed! Syntax error ecnountered. Reverting to original content."
        )
        return "Failure"
