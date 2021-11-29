#  type: ignore
import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    if os.getenv("GIT_DIR") is None:
        os.environ["GIT_DIR"] = ".git"

    wdirectory = pathlib.Path(workdir, os.environ["GIT_DIR"])

    if str(wdirectory).count(".git") > 1:
        wdirectory = pathlib.Path(str(wdirectory).split(".git")[0] + ".git")

    if os.path.isdir(wdirectory) != True:
        raise Exception("Not a git repository")

    return wdirectory


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    # os.environ["GIT_DIR"] =".git"
    if os.path.isdir(workdir) != True:
        raise Exception(f"{workdir} is not a directory")
    # PUT YOUR CODE HERE
    if os.getenv("GIT_DIR") is None:
        os.environ["GIT_DIR"] = ".git"

    wdirectory = pathlib.Path(workdir, os.environ["GIT_DIR"])
    pathlib.Path(wdirectory).mkdir(parents=True, exist_ok=True)
    pathlib.Path(wdirectory, "refs", "heads").mkdir(parents=True, exist_ok=True)
    pathlib.Path(wdirectory, "refs", "tags").mkdir(parents=True, exist_ok=True)
    pathlib.Path(wdirectory, "objects").mkdir(parents=True, exist_ok=True)

    file_for_note = open(pathlib.Path(wdirectory, "HEAD"), "w")
    file_for_note.write("ref: refs/heads/master\n")
    file_for_note.close()

    file_for_note = open(pathlib.Path(wdirectory, "config"), "w")
    file_for_note.write(
        "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
    )
    file_for_note.close()

    file_for_note = open(pathlib.Path(wdirectory, "description"), "w")
    file_for_note.write("Unnamed pyvcs repository.\n")
    file_for_note.close()
    return pathlib.Path(os.environ["GIT_DIR"])
