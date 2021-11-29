#  type: ignore
import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    added_content = []
    for path in paths:
        if path.is_file():
            added_content.append(path)
        if path.is_dir():
            add(gitdir, list(path.glob("*")))
    update_index(gitdir, added_content)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    hash = commit_tree(
        gitdir,
        write_tree(gitdir, read_index(gitdir), str(gitdir.parent)),
        message,
        resolve_head(gitdir),
        author,
    )
    with (gitdir / get_ref(gitdir)).open("w") as f:
        f.write(hash)
    return hash


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    for entrance in read_index(gitdir):
        if (gitdir.parent / entrance.name).exists():
            os.remove(entrance.name)
    data_of_commit = commit_parse(read_object(obj_name, gitdir)[1])
    flag_1 = True
    while flag_1:
        tree_data = [(gitdir.parent, read_tree(read_object(data_of_commit["tree"], gitdir)[1]))]
        while len(tree_data) != 0:
            tree_path, tree_content = tree_data.pop()
            for file_data in tree_content:
                fmt, data = read_object(file_data[1], gitdir)
                if fmt == "tree":
                    tree_data.append((tree_path / file_data[2], read_tree(data)))
                    if not (tree_path / file_data[2]).is_dir():
                        (tree_path / file_data[2]).mkdir()
                else:
                    if not (tree_path / file_data[2]).exists():
                        with (tree_path / file_data[2]).open("wb") as f:
                            f.write(data)
                        (tree_path / file_data[2]).chmod(file_data[0])
        if "parent" in data_of_commit:
            data_of_commit = commit_parse((read_object(data_of_commit["parent"], gitdir)[1]))
        else:
            flag_1 = False
    for remove_part in gitdir.parent.glob("*"):
        if remove_part.is_dir() and remove_part != gitdir:
            try:
                os.removedirs(remove_part)
            except OSError:
                continue
