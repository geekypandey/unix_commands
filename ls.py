import os


def ls(dirname=None, show_hidden=False, reverse=False) -> list:
    """Lists the contents of the directory specified."""
    if dirname is None:
        dirname = "."
    resp = sorted(os.listdir(dirname), reverse=reverse)

    if not show_hidden:
        resp = [f for f in resp if not f.startswith(".")]
    return resp
