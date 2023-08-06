import os
import shutil
import argparse

from utils.output import echo
from .utils.edit_config import edit_config
from .utils.edit_index import edit_index
from .utils.edit_user_guide import edit_user_guide
from .utils.edit_reference import edit_reference


def parse_args():
    parser = argparse.ArgumentParser(description="Generate documentation for a project")
    parser.add_argument("-p", "--project-name", help="Project name.", required=True)
    parser.add_argument("-a", "--author-name", help="Author name.", required=True)
    parser.add_argument(
        "-c", "--code-root", help="Code root directory path.", required=True
    )
    parser.add_argument(
        "-d", "--doc-root", help="Documentation root directory path.", required=True
    )
    parser.add_argument(
        "-i",
        "--ignore-list",
        help="Names of top-level modules to ignore.",
        nargs="+",
        default=[],
    )
    args = parser.parse_args()
    return args


def compile_doc(
    project_name, author_name, code_root, doc_root, ignore_list, verbose=False
):
    if os.path.exists(doc_root):
        shutil.rmtree(doc_root)
        os.makedirs(doc_root)

    # current_directory = os.curdir
    os.system(
        f"sphinx-quickstart -q -p '{project_name}' -a '{author_name}' '{doc_root}'"
    )

    config_path = os.path.join(doc_root, "conf.py")
    edit_config(config_path, code_root, config_path)
    index_path = os.path.join(doc_root, "index.rst")
    edit_index(project_name, index_path)

    os.makedirs(os.path.join(doc_root, "user_guide"))
    os.makedirs(os.path.join(doc_root, "reference"))

    edit_user_guide(os.path.join(doc_root, "user_guide", "index.rst"))
    edit_reference(
        os.path.join(doc_root, "reference", "index.rst"), code_root, ignore_list
    )

    templates_dir = os.path.join(doc_root, "_templates", "autosummary")
    os.makedirs(templates_dir)
    shutil.copy(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates/base.rst"),
        templates_dir,
    )
    shutil.copy(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates/class.rst"),
        templates_dir,
    )
    shutil.copy(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "templates/module.rst"
        ),
        templates_dir,
    )

    # os.chdir(f"{doc_root}")
    os.system(f"make -s html -C {doc_root}")
    os.system(f"open {doc_root}/_build/html/index.html")


def main():
    args = parse_args()
    project_name = args.project_name
    author_name = args.author_name
    code_root = args.code_root
    doc_root = args.doc_root
    ignore_list = args.ignore_list

    compile_doc(project_name, author_name, code_root, doc_root, ignore_list)


if __name__ == "__main__":
    main()
