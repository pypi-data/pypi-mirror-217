import ast
import pathlib
import typing
import collections.abc


def add_path_prefix(in_path, code_root, out_path=""):
    if not out_path:
        out_path = in_path

    prefix = f"""
import sys
import pathlib
sys.path.insert(0, "{pathlib.Path(code_root).resolve().as_posix()}")
"""
    with open(in_path, "r") as f:
        data_in = f.read()

    data_out = prefix + "\n" + data_in
    with open(out_path, "w") as f:
        f.write(data_out)


def replace_scalar_assignments(tree, map):
    for i, node in enumerate(tree.body):
        if not isinstance(node, ast.Assign):
            continue

        for nt in node.targets:
            if not isinstance(nt, ast.Name):
                # deal with tuple assignments a, b = 1, 2
                continue
            if nt.id in map:
                # ok we have to replace this
                if not isinstance(node.value, ast.Constant):
                    # warning it is not assigned a constant
                    continue
                # change value for all targets. this will break a=b=2 with a replace of a = 5
                node.value.value = map[nt.id]


def replace_list_assignments(tree, map):
    assert all(
        isinstance(item, collections.abc.Sequence) for item in map.values()
    ), "All assignments need to be lists."

    for i, node in enumerate(tree.body):
        if not isinstance(node, ast.Assign):
            continue

        for nt in node.targets:
            if not isinstance(nt, ast.Name):
                # deal with tuple assignments a, b = 1, 2
                continue
            if nt.id in map:
                # ok we have to replace this
                if not isinstance(node.value, ast.List):
                    # warning it is not assigned a list
                    continue

                # change value for all targets. this will break a=b=2 with a replace of a = 5
                node.value.elts = [ast.Constant(item) for item in map[nt.id]]


def remap_config(in_path, code_root, mapping, out_path=""):
    if not out_path:
        out_path = in_path
    add_path_prefix(in_path, code_root, out_path)
    with open(out_path, "r") as f:
        data = f.read()
    tree = ast.parse(data, mode="exec")
    mapping_scalar = {
        key: value
        for key, value in mapping.items()
        if not isinstance(value, typing.List)
    }
    mapping_list = {
        key: value for key, value in mapping.items() if isinstance(value, typing.List)
    }
    replace_scalar_assignments(tree, mapping_scalar)
    replace_list_assignments(tree, mapping_list)
    data = ast.unparse(tree)
    with open(out_path, "w") as f:
        f.write(data)


def edit_config(in_path, code_root, out_path):
    mapping = {
        "html_theme": "sphinx_rtd_theme",
        "extensions": [
            "sphinx.ext.autodoc",
            "sphinx.ext.doctest",
            "sphinx.ext.autosummary",
        ],
    }
    remap_config(in_path, code_root, mapping, out_path)
