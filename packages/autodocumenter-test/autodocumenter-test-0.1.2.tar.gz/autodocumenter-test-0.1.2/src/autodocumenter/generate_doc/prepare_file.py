import os
import re
import yaml
import time
import asyncio

from utils.hashing import get_hash
from utils.output import out, err
from utils.constants import docstring_quotes, end_of_declaration_regex
from .utils.parse_file import (
    get_class_bodies,
    get_function_bodies,
    get_method_bodies,
    check_code_syntax,
)
from .utils.token_counting import num_tokens_from_messages


def prepare_file(
    file_path,
    overwrite_existing_docstrings=False,
    use_existing_docstrings=False,
    document_class_defs=False,
    token_cap=2500,
    verbose=False,
):
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/utils/config.yaml", "r") as file:
        config = yaml.load(file, Loader=yaml.CLoader)
    system_prompt_class = config["SYSTEM_PROMPT_CLASS"]
    user_prompt_class = config["USER_PROMPT_CLASS"]
    system_prompt_function = config["SYSTEM_PROMPT_FUNCTION"]
    user_prompt_function = config["USER_PROMPT_FUNCTION"]
    system_prompt = {
        "ClassDef": system_prompt_class,
        "FunctionDef": system_prompt_function,
        "ClassMethodDef": system_prompt_function,
    }
    user_prompt = {
        "ClassDef": user_prompt_class,
        "FunctionDef": user_prompt_function,
        "ClassMethodDef": user_prompt_function,
    }

    function_defs = get_function_bodies(file_path, use_existing_docstrings)
    num_function_defs = len(function_defs)
    if document_class_defs:
        class_defs = get_class_bodies(file_path, use_existing_docstrings)
        num_class_defs = len(class_defs)
    else:
        class_defs = []
        num_class_defs = 0
    method_defs = get_method_bodies(file_path, use_existing_docstrings)
    num_method_defs = len(method_defs)
    all_defs = function_defs + class_defs + method_defs
    all_defs = sorted(all_defs, key=lambda x: x["lineno"])

    # Unless overwriting existing docstrings, only include undocumented ones
    all_defs = [
        item
        for item in all_defs
        if (
            (not item["docstring"])
            or (item["docstring"] and overwrite_existing_docstrings)
        )
    ]

    to_document_defs = []
    for data in all_defs:
        include = True
        if data["docstring"] and not overwrite_existing_docstrings:
            include = False
        if include:
            to_document_defs.append(data)

    if verbose:
        out(
            f"In file {file_path}, creating hashes for {len(function_defs)} functions, {len(class_defs)} classes and {len(method_defs)} methods..."
        )

    with open(file_path, "r") as file:
        file_lines = file.readlines()

    # Save for fallback if the file breaks
    original_file_txt = "".join(file_lines)

    global_offset = 0
    tasks = []
    for data in all_defs:
        original_body_lines = data["original_body"].splitlines(keepends=True)
        def_end_lines = [
            i
            for i, original_body_line in enumerate(original_body_lines)
            if re.search(end_of_declaration_regex, original_body_line)
        ]
        if len(def_end_lines):
            def_end_line = def_end_lines[0]
            # Decide based on docstring if we need to remove it and reduce local offset
            if data["docstring"]:
                docstring_start_line = [
                    i
                    for i, item in enumerate(original_body_lines)
                    if any(
                        [
                            docstring_quote in item
                            for docstring_quote in docstring_quotes
                        ]
                    )
                ][0]
                num_removed_lines = (
                    len(data["docstring"].splitlines(keepends=True))
                    + docstring_start_line
                    - def_end_line
                    - 1
                )
            else:
                num_removed_lines = 0

            hash = get_hash(file_path, " ", data["lineno"])
            hash = '"""\n' + hash + '\n"""\n'
            hash_lines = hash.splitlines(keepends=True)
            indentation = "    " + data["col_offset"] * " "
            hash_lines = [indentation + hash_line for hash_line in hash_lines]
            hash_placeholder = "".join(hash_lines)
            messages = [
                {"role": "system", "content": system_prompt[data["type"]]},
                {
                    "role": "user",
                    "content": user_prompt[data["type"]].replace("<<code>>", data["body"]),
                },
            ]
            num_tokens = num_tokens_from_messages(messages)

            if num_tokens < token_cap:
                tasks.append(
                    {
                        "file_path": file_path,
                        "lineno": data["lineno"],
                        "col_offset": data["col_offset"],
                        "hash_placeholder": hash_placeholder,
                        "type": data["type"],
                        "body": data["body"],
                        "existing_docstring": data["docstring"],
                        "messages": messages,
                        "num_tokens": num_tokens
                    }
                )
                num_hash_lines = len(hash_lines)
                total_lineno = data["lineno"] + def_end_line + global_offset
                file_lines = (
                    file_lines[:(total_lineno)]
                    + hash_lines
                    + file_lines[(total_lineno + num_removed_lines) :]
                )
                global_offset = global_offset + num_hash_lines - num_removed_lines
        else:
            # BAD, IT WILL SKIP THIS DEFINITION AS HEADING WAS NOT DETECTED PROPERLY
            # ALTHOUGH SHOILD ALMOST NEVER HAPPEN (UP TO THE REGEX)
            pass

    file_txt = "".join(file_lines)

    syntax_check = check_code_syntax(file_txt)

    if syntax_check:
        with open(file_path, "w") as f:
            f.write(file_txt)
        if verbose:
            out(
                f"File {file_path} sucessfuly processed! Generated placeholders for docstrings to {num_function_defs} functions, {num_class_defs} classes and {num_method_defs} methods."
            )
        return ("Success", tasks)
    else:
        with open(file_path, "w") as f:
            f.write(original_file_txt)
        err(
            f"File {file_path} unsucessfuly processed! Syntax error ecnountered. Reverting to original content."
        )
        return ("Failure", [])


if __name__ == "__main__":
    file_path = "examples/processing_documented.py"
    time1 = time.time()
    asyncio.run(prepare_file(file_path))
    time2 = time.time()
    print(time2 - time1)
