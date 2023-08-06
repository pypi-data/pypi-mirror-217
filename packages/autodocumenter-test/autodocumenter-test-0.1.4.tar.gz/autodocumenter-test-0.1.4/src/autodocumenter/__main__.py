import shutil
import argparse
from utils.misc import uniquify
from utils.output import out
from generate_doc import generate_doc
from compile_doc import compile_doc


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
    parser.add_argument(
        "-v", "--verbose", help="Verbosity.", action="store_true", default=False
    )
    parser.add_argument(
        "-e",
        "--edit-code",
        help="Whether to add docstrings to the code (if not tmp dir is used).",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-o",
        "--overwrite-existing-docstrings",
        help="Whether to overwrite existing docstrings.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-u",
        "--use-existing-docstrings",
        help="Whether to use existing docstrings when generating response.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-cd",
        "--document-class-defs",
        help="Whether to document class defs, often not necessary due to the ability to document individual methods and the __init__.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--model",
        help="Which model to use to generate documentation",
        type=str,
        default="gpt-3.5-turbo",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.01,
        help="Temperature for the language model.",
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=20,
        help="Maximum number of concurrent API requests.",
    )
    parser.add_argument(
        "--max-per-second",
        type=int,
        default=4,
        help="Maximum number of API requests made per second.",
    )
    parser.add_argument("--timeout", type=int, default=-1, help="Timeout API call.")
    parser.add_argument(
        "-rl",
        "--rate-limit",
        help="Whether to use rate limiting.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--request-limit",
        type=int,
        default=3000,
        help="Request limit for the rate limiter.",
    )
    parser.add_argument(
        "--token-limit",
        type=int,
        default=80000,
        help="Token limit for the rate limiter.",
    )
    parser.add_argument(
        "-tc",
        "--token-cap",
        type=int,
        default=2500,
        help="Cap to the number of tokens for which the request will be processed.",
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    project_name = args.project_name
    author_name = args.author_name
    code_root = args.code_root
    doc_root = args.doc_root
    ignore_list = args.ignore_list

    model = args.model
    temperature = args.temperature

    max_concurrent = args.max_concurrent
    max_per_second = args.max_per_second

    timeout = args.timeout
    rate_limit = args.rate_limit
    request_limit = args.request_limit
    token_limit = args.token_limit

    overwrite_existing_docstrings = args.overwrite_existing_docstrings
    use_existing_docstrings = args.use_existing_docstrings
    document_class_defs = args.document_class_defs
    edit_code = args.edit_code
    token_cap = args.token_cap
    verbose = args.verbose

    using_tmp = False if edit_code else True

    if using_tmp:
        tmp_code_root = uniquify("./tmp")
        if verbose:
            out(f"Copying the code source to a temporary directory at {tmp_code_root}")
        shutil.copytree(code_root, tmp_code_root)
        code_root = tmp_code_root
        using_tmp = True

    generate_doc(
        code_root,
        ignore_list,
        model,
        temperature,
        max_concurrent,
        max_per_second,
        timeout,
        rate_limit,
        request_limit,
        token_limit,
        overwrite_existing_docstrings,
        use_existing_docstrings,
        document_class_defs,
        token_cap,
        verbose,
    )
    compile_doc(project_name, author_name, code_root, doc_root, ignore_list, verbose)

    if using_tmp:
        out(f"Deleting the temporary directory {tmp_code_root}")
        shutil.rmtree(tmp_code_root)


if __name__ == "__main__":
    main()
