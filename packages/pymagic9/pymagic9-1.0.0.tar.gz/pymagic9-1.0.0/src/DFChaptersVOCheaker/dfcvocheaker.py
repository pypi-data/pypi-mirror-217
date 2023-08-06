# noinspection SpellCheckingInspection
"""
dfcvocheaker.py
"""
import os
# noinspection PyCompatibility
import pathlib


# noinspection SpellCheckingInspection
def isinclude(path_1, path_2):
    """
    Compare two directories.

    :param path_1: path of 1st directorie
    :param path_2: path of 2st directorie
    :return: True if `path_1` include in `path_2`, else False.
    """
    path_1, path_2 = os.path.abspath(path_1), os.path.abspath(path_2)
    missing = []

    # noinspection PyShadowingBuiltins
    with pathlib.Path(path_1) as dir:
        for file in dir.iterdir():
            if not os.path.exists(os.path.join(path_2, file.name)):
                missing.append(file)
                continue

            if file.is_dir():
                if not isinclude(os.path.join(path_1, file.name), os.path.join(path_2, file.name)):
                    missing.append(file)
                    continue

        if len(missing):
            return missing, False

        return missing, True
