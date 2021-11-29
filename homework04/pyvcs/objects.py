#  type: ignore
import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    roof = fmt + f" " + f"{len(data)}\0"
    sha = hashlib.sha1(roof.encode() + data).hexdigest()
    if write:
        wd = pathlib.Path(".", os.environ["GIT_DIR"], "objects", sha[0:2])
        pathlib.Path(wd).mkdir(parents=True, exist_ok=True)
        filename = sha[2:]
        f = open(pathlib.Path(wd, filename), "wb")
        if isinstance(data, bytes):
            store = roof.encode() + data
        file_c = zlib.compress(roof.encode() + data)
        f.write(file_c)
        f.close()
    return sha


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    wd = pathlib.Path(gitdir, "objects", obj_name[0:2])
    files_list = []
    for (dirpath, dirnames, filenames) in os.walk(wd):
        for i in filenames:
            if obj_name[2:] == i[:3]:
                files_list.append("".join([obj_name[0:2], i]))
    if len(files_list) > 0:
        return files_list
    else:
        raise Exception(f"Not a valid object name {obj_name}")


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    wd = pathlib.Path(gitdir, "objects", obj_name[0:2])
    files_list = []
    for (dirpath, dirnames, filenames) in os.walk(wd):
        for i in filenames:
            if obj_name[2:] == i[:3]:
                files_list.append("".join([obj_name[0:2], i]))
    if len(files_list) > 0:
        return files_list
    else:
        raise Exception(f"Not a valid object name {obj_name}")


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    wdirectory = pathlib.Path(gitdir, "objects", sha[0:2])
    filename = sha[2:]
    f = open(pathlib.Path(wdirectory, filename), "rb")
    count = zlib.decompress(f.read())
    temple = count.split(b" ")
    type_c = temple[0].decode()
    del temple[0]
    temple_joined = b" ".join(temple)
    cont = temple_joined.split(b"\x00", maxsplit=1)[1]

    return type_c, cont


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    ans = []
    while data:
        before_sha_index = data.index(b"\00")
        type_of_mode, name = data[:before_sha_index].decode().split(" ")
        sha = data[before_sha_index + 1 : before_sha_index + 21]
        ans.append((int(type_of_mode), sha.hex(), name))
        data = data[before_sha_index + 21 :]
    return ans


def cat_file(obj_name: str, pretty: bool = True) -> None:
    type_c, cont = read_object(
        obj_name, pathlib.Path(".", os.environ.get("GIT_DIR", default=".git"))
    )
    if pretty and (type_c == "blob" or type_c == "commit"):
        print(cont.decode())
    else:
        tree = read_tree(cont)
        for i in tree:
            if i[0] == 40000:
                obj_type = "tree"
            else:
                obj_type = "blob"
            print(f"{i[0]:06}", obj_type, i[1] + "\t" + i[2])


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    ans_2 = []
    while data:
        before_sha_index = data.index(b"\00")
        mode, name = data[:before_sha_index].decode().split(" ")
        sha = data[before_sha_index + 1 : before_sha_index + 21]
        ans_2.append((int(mode), sha.hex(), name))
        data = data[before_sha_index + 21 :]
    return ans_2


def commit_parse(raw: bytes, start: int = 0, dct=None):
    commit_dict = {"message": []}
    for row in raw.decode().split("\n"):
        if row.startswith(("parent", "committer", "author", "tree")):
            name, value = row.split(" ", maxsplit=1)
            commit_dict[name] = value
        else:
            commit_dict["message"].append(row)

    return commit_dict
