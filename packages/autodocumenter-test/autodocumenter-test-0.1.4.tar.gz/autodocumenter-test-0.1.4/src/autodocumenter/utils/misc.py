import os
import astor


def get_python_files(root):
    result = [
        os.path.join(item[0], item[1]) for item in astor.code_to_ast.find_py_files(root)
    ]
    return result


def remove_extension(path, return_basename=False):
    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    basename = os.path.splitext(basename)[0]

    if return_basename:
        return basename
    else:
        return os.path.join(dirname, basename)


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path
