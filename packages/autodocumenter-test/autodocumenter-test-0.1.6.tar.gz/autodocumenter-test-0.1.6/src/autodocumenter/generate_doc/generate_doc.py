import asyncio
import os
import pathlib
import argparse
from itertools import groupby
from operator import itemgetter

import openai
import aiometer
from aiomisc import asyncbackoff
from alive_progress import alive_bar
from utils.output import out, err
from utils.misc import get_python_files
from .utils.generate_response import generate_response_async
from .prepare_file import prepare_file
from .write_file import write_file


def parse_args():
    parser = argparse.ArgumentParser(description="Generate documentation for a project")
    parser.add_argument(
        "-c", "--code-root", help="Code root directory path.", required=True
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


def timeout_decorator_factory(timeout):
    def timeout_decorator(func):
        return asyncbackoff(attempt_timeout=timeout, deadline=timeout, max_tries=1)(func)

    def dummy_decorator(func):
        return func

    if timeout > 0:
        return timeout_decorator
    else:
        return dummy_decorator


async def add_response_to_task(
    task,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.01,
    timeout: int = -1,
    rate_limit: bool = False,
    request_limit: int = 500,
    token_limit: int = 50000,
    stop=None,  # can be set to ["#", "\"\"\""]
):
    try:
        response = await timeout_decorator_factory(timeout)(
            generate_response_async
        )(
            task["messages"],
            model,
            temperature,
            timeout,
            rate_limit,
            request_limit,
            token_limit,
            stop,
        )
    except asyncio.exceptions.TimeoutError as e:
        err(e)
        if task["existing_docstring"]:
            response = task["existing_docstring"]
        else:
            response = (
                "Docstring generation timed out, no existing docstring to revert to!"
            )
        err(
            f"Timeout occurred on {task['file_path']}, line {task['lineno']} due to {e},\
            (with {len(task['body'].splitlines(keepends=True))} lines and {task['num_tokens']} tokens),\
            reverting to original docstring if available, or leaving timeout notification."
        )
    except openai.error.OpenAIError as e:
        if task["existing_docstring"]:
            response = task["existing_docstring"]
        else:
            response = (
                "Docstring generation timed out, no existing docstring to revert to!"
            )
        err(
            f"OpenAI service unavailable on {task['file_path']}, line {task['lineno']} due to {e},\
            (with {len(task['body'].splitlines(keepends=True))} lines and {task['num_tokens']} tokens),\
            reverting to original docstring if available, or leaving timeout notification."
        )
    task["response"] = response
    return task


async def generate_documentation(
    code_root,
    ignore_list,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.01,
    max_concurrent: int = 60,
    max_per_second: int = 4,
    timeout: int = 120,
    rate_limit: bool = False,
    request_limit: int = 500,
    token_limit: int = 50000,
    overwrite_existing_docstrings: bool = False,
    use_existing_docstrings: bool = False,
    document_class_defs: bool = False,
    token_cap: int = 2500,
    verbose: bool = False,
):
    files = get_python_files(code_root)
    # We do not document top-level files
    files_toplevel = [
        pathlib.Path(os.path.relpath(file, code_root)).parts[0] for file in files
    ]
    files = [
        file
        for i, file in enumerate(files)
        if (
            os.path.isdir(os.path.join(code_root, files_toplevel[i]))
            and files_toplevel[i] not in ignore_list
        )
    ]

    prepare_file_partial = lambda x: prepare_file(
        x,
        overwrite_existing_docstrings=overwrite_existing_docstrings,
        use_existing_docstrings=use_existing_docstrings,
        document_class_defs=document_class_defs,
        token_cap=token_cap,
        verbose=verbose,
    )
    add_response_to_task_partial = lambda x: add_response_to_task(
        x,
        model=model,
        temperature=temperature,
        timeout=timeout,
        rate_limit=rate_limit,
        request_limit=request_limit,
        token_limit=token_limit,
    )

    all_tasks = []
    for file in files:
        indicator, tasks = prepare_file_partial(file)
        if indicator:
            all_tasks.extend(tasks)

    out(f"Added docstring placeholders to {len(all_tasks)} docstrings...")

    completed_tasks = []
    with alive_bar(len(all_tasks), disable=(not verbose)) as bar:
        async with aiometer.amap(
            add_response_to_task_partial,
            all_tasks,
            max_at_once=max_concurrent,  # Limit maximum number of concurrently running tasks.
            max_per_second=max_per_second,  # Limit request rate to not overload the server.
        ) as results:
            async for result in results:
                completed_tasks.append(result)
                if verbose:
                    bar()

    out(f"Generated {len(all_tasks)} docstrings, writing docstrings to files...")

    completed_tasks = sorted(completed_tasks, key=itemgetter("file_path"))
    for file_path, tasks in groupby(completed_tasks, key=itemgetter("file_path")):
        write_file(file_path, tasks, verbose=verbose)


def generate_doc(
    code_root,
    ignore_list,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.01,
    max_concurrent: int = 60,
    max_per_second: int = 4,
    timeout: int = 120,
    rate_limit: bool = False,
    request_limit: int = 500,
    token_limit: int = 50000,
    overwrite_existing_docstrings: bool = False,
    use_existing_docstrings: bool = False,
    document_class_defs: bool = False,
    token_cap: int = 2500,
    verbose: bool = False,
):
    asyncio.run(
        generate_documentation(
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
    )


def main():
    args = parse_args()
    code_root = args.code_root
    ignore_list = args.ignore_list
    overwrite_existing_docstrings = False
    use_existing_docstrings = False

    generate_doc(
        code_root,
        ignore_list,
        overwrite_existing_docstrings=overwrite_existing_docstrings,
        use_existing_docstrings=use_existing_docstrings,
        verbose=True,
    )


if __name__ == "__main__":
    main()
