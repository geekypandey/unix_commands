import os


def ls(dirname=None) -> list:
    """Lists the contents of the directory specified."""
    if dirname is None:
        dirname = "."
    return sorted(os.listdir(dirname))
