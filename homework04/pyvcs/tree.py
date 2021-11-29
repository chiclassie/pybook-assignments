#  type: ignore
import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    structure_of_tree = []
    tree_sidings = dict()
    files = []
    extracted_structure = (gitdir.parent / dirname).glob("*")
    filler = 0o40000

    for i in extracted_structure:
        files.append(str(i))

    for entrance in index:
        if entrance.name in files:
            structure_of_tree.append(
                (entrance.mode, str(gitdir.parent / entrance.name), entrance.sha1)
            )
        else:
            directory_name = entrance.name.lstrip(dirname).split("/", 1)[0]
            if not directory_name in tree_sidings:
                tree_sidings[directory_name] = []
            tree_sidings[directory_name].append(entrance)

    for name in tree_sidings:
        if dirname != "":
            structure_of_tree.append(
                (
                    filler,
                    str(gitdir.parent / dirname / name),
                    bytes.fromhex(write_tree(gitdir, tree_sidings[name], dirname + "/" + name)),
                )
            )
        else:
            structure_of_tree.append(
                (
                    filler,
                    str(gitdir.parent / dirname / name),
                    bytes.fromhex(write_tree(gitdir, tree_sidings[name], name)),
                )
            )
    structure_of_tree.sort(key=lambda x: x[1])
    data = b"".join(
        f"{elem[0]:o} {elem[1].split('/')[-1]}".encode() + b"\00" + elem[2]
        for elem in structure_of_tree
    )
    return hash_object(data, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:

    if "GIT_AUTHOR_NAME" in os.environ and "GIT_AUTHOR_EMAIL" in os.environ and author is None:
        author = (
            os.getenv("GIT_AUTHOR_NAME") + " " + f'<{os.getenv("GIT_AUTHOR_EMAIL")}>'
        )  # type:ignore
    if time.timezone > 0:
        timezone_bool = "-"
    else:
        timezone_bool = "+"

    timezone_bool += f"{abs(time.timezone) // 3600:02}{abs(time.timezone) // 60 % 60:02}"
    commited_data = []
    commited_data.append(f"tree {tree}")

    if parent is not None:
        commited_data.append(f"parent {parent}")
    commited_data.append(f"author {author} {int(time.mktime(time.localtime()))} {timezone_bool}")

    commited_data.append(f"committer {author} {int(time.mktime(time.localtime()))} {timezone_bool}")
    commited_data.append(f"\n{message}\n")
    return hash_object("\n".join(commited_data).encode(), "commit", write=True)
