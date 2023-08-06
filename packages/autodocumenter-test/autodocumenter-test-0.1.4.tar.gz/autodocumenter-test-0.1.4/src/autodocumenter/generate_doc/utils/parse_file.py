import ast
import re
from collections import namedtuple

from utils.constants import docstring_quotes, end_of_declaration_regex


def check_file_syntax(file_path):
    with open(file_path) as f:
        source = f.read()
    valid = True
    try:
        ast.parse(source)
    except SyntaxError:
        valid = False
        # traceback.print_exc()  # Remove to silence any errros
    return valid


def check_code_syntax(source):
    valid = True
    try:
        ast.parse(source)
    except SyntaxError:
        valid = False
        # traceback.print_exc()  # Remove to silence any errros
    return valid


def get_imports(file_path):
    Import = namedtuple("Import", ["module", "name", "alias"])

    with open(file_path) as file:
        root = ast.parse(file.read(), file_path)

    imports = []
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split(".")
        else:
            continue

        for n in node.names:
            imports.append(Import(module, n.name.split("."), n.asname))

    return imports


def get_node_body(node, fullText):
    node_rep = "\n".join(fullText.splitlines()[node.lineno - 1 : node.end_lineno])
    return node_rep


def get_docstring(node):
    docstring = ast.get_docstring(node, clean=False)
    if docstring is not None:
        return docstring
    else:
        return ""


def get_function_bodies(file_path, use_existing_docstring=False):
    with open(file_path, "r") as file:
        file_txt = file.read()

    node = ast.parse(file_txt)
    function_names = [
        n
        for n in node.body
        if (isinstance(n, ast.FunctionDef) or isinstance(n, ast.AsyncFunctionDef))
    ]

    function_bodies = []
    for function_name in function_names:
        # data - function body, start line, end line, col offset, end col offset
        node_body = get_node_body(function_name, file_txt)
        original_node_body = node_body
        docstring = get_docstring(function_name)

        if docstring and not use_existing_docstring:
            node_body_lines = node_body.splitlines(keepends=True)
            def_end_lines = [
                i
                for i, node_body_line in enumerate(node_body_lines)
                if re.search(end_of_declaration_regex, node_body_line)
            ]
            if len(def_end_lines):
                def_end_line = def_end_lines[0]
                docstring_start_line = [
                    i
                    for i, item in enumerate(node_body_lines)
                    if any(
                        [
                            docstring_quote in item
                            for docstring_quote in docstring_quotes
                        ]
                    )
                ][0]
                num_docstring_lines = len(docstring.splitlines(keepends=True))
                node_body_lines = (
                    node_body_lines[: (def_end_line + 1)]
                    + node_body_lines[(docstring_start_line + num_docstring_lines) :]
                )
                node_body = "".join(node_body_lines)
            else:
                # BAD, IT WILL GIVE BACK THE NODE BODY WITH THE OLD DOCSTRING IN PLACE, EVEN IF REMOVAL WAS REQUIRED
                # ALTHOUGH SHOILD ALMOST NEVER HAPPEN (UP TO THE REGEX)
                pass

        data = {
            "body": node_body,
            "original_body": original_node_body,
            "lineno": function_name.lineno,
            "end_lineno": function_name.end_lineno,
            "col_offset": function_name.col_offset,
            "end_col_offset": function_name.end_col_offset,
            "type": "FunctionDef",
            "docstring": docstring,
        }
        function_bodies.append(data)

    return function_bodies


def get_class_bodies(file_path, use_existing_docstring=False):
    with open(file_path, "r") as file:
        file_txt = file.read()

    node = ast.parse(file_txt)
    class_names = [n for n in node.body if isinstance(n, ast.ClassDef)]

    class_bodies = []
    for class_name in class_names:
        # data - function body, start line, end line, col offset, end col offset
        node_body = get_node_body(class_name, file_txt)
        original_node_body = node_body
        docstring = get_docstring(class_name)

        if docstring and not use_existing_docstring:
            node_body_lines = node_body.splitlines(keepends=True)
            def_end_lines = [
                i
                for i, node_body_line in enumerate(node_body_lines)
                if re.search(end_of_declaration_regex, node_body_line)
            ]
            if len(def_end_lines):
                def_end_line = def_end_lines[0]
                docstring_start_line = [
                    i
                    for i, item in enumerate(node_body_lines)
                    if any(
                        [
                            docstring_quote in item
                            for docstring_quote in docstring_quotes
                        ]
                    )
                ][0]
                num_docstring_lines = len(docstring.splitlines(keepends=True))
                node_body_lines = (
                    node_body_lines[: (def_end_line + 1)]
                    + node_body_lines[(docstring_start_line + num_docstring_lines) :]
                )
                node_body = "".join(node_body_lines)
            else:
                # BAD, IT WILL GIVE BACK THE NODE BODY WITH THE OLD DOCSTRING IN PLACE, EVEN IF REMOVAL WAS REQUIRED
                # ALTHOUGH SHOILD ALMOST NEVER HAPPEN (UP TO THE REGEX)
                pass

        data = {
            "body": node_body,
            "original_body": original_node_body,
            "lineno": class_name.lineno,
            "end_lineno": class_name.end_lineno,
            "col_offset": class_name.col_offset,
            "end_col_offset": class_name.end_col_offset,
            "type": "ClassDef",
            "docstring": docstring,
        }
        class_bodies.append(data)

    return class_bodies


def get_method_bodies(file_path, use_existing_docstring=False):
    with open(file_path, "r") as file:
        file_txt = file.read()

    node = ast.parse(file_txt)
    class_names = [n for n in node.body if isinstance(n, ast.ClassDef)]

    method_bodies = []
    for class_name in class_names:
        method_names = [n for n in class_name.body if isinstance(n, ast.FunctionDef)]
        for method_name in method_names:
            node_body = get_node_body(method_name, file_txt)
            original_node_body = node_body
            docstring = get_docstring(method_name)

            if docstring and not use_existing_docstring:
                node_body_lines = node_body.splitlines(keepends=True)
                def_end_lines = [
                    i
                    for i, node_body_line in enumerate(node_body_lines)
                    if re.search(end_of_declaration_regex, node_body_line)
                ]
                if len(def_end_lines):
                    def_end_line = def_end_lines[0]
                    docstring_start_line = [
                        i
                        for i, item in enumerate(node_body_lines)
                        if any(
                            [
                                docstring_quote in item
                                for docstring_quote in docstring_quotes
                            ]
                        )
                    ][0]
                    num_docstring_lines = len(docstring.splitlines(keepends=True))
                    node_body_lines = (
                        node_body_lines[: (def_end_line + 1)]
                        + node_body_lines[
                            (docstring_start_line + num_docstring_lines) :
                        ]
                    )
                    node_body = "".join(node_body_lines)
                else:
                    # BAD, IT WILL GIVE BACK THE NODE BODY WITH THE OLD DOCSTRING IN PLACE, EVEN IF REMOVAL WAS REQUIRED
                    # ALTHOUGH SHOILD ALMOST NEVER HAPPEN (UP TO THE REGEX)
                    pass

            data = {
                "body": node_body,
                "original_body": original_node_body,
                "lineno": method_name.lineno,
                "end_lineno": method_name.end_lineno,
                "col_offset": method_name.col_offset,
                "end_col_offset": method_name.end_col_offset,
                "type": "ClassMethodDef",
                "docstring": docstring,
            }
            method_bodies.append(data)

    return method_bodies

