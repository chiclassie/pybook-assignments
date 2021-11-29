#  type: ignore
import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        cut = self.ino & 0xFFFFFFFF
        head = struct.pack(
            "!LLLLLLLLLL20sH",
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            cut,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
        )
        name = self.name.encode()
        n = 0
        pack = head + name + b"\x00" * n
        while len(pack) % 8 != 0:
            n += 1
            pack = head + name + b"\x00" * n
        return pack

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        roof = data[:62]
        unpack = struct.unpack("!LLLLLLLLLL20sH", roof)
        named = data[62 : len(data)].decode().rstrip("\x00")
        result = GitIndexEntry(
            ctime_s=unpack[0],
            ctime_n=unpack[1],
            mtime_s=unpack[2],
            mtime_n=unpack[3],
            dev=unpack[4],
            ino=unpack[5],
            mode=unpack[6],
            uid=unpack[7],
            gid=unpack[8],
            size=unpack[9],
            sha1=unpack[10],
            flags=unpack[11],
            name=named,
        )
        return result


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    result = []
    if os.path.exists(gitdir / "index"):
        with open(gitdir / "index", "rb") as f:
            data = f.read()
        entry_count = struct.unpack("!L", data[8:12])[0]
        start_pos = 12
        for i in range(entry_count):
            end_pos = start_pos + 62 + data[start_pos + 62 :].find(b"\x00")
            entry = data[start_pos:end_pos]
            result.append(GitIndexEntry.unpack(entry))
            start_pos = end_pos + (8 - ((62 + len(result[i].name)) % 8))
    return result


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    result = struct.pack("!4sLL", b"DIRC", 2, len(entries))
    for entry in entries:
        result += entry.pack()
    result += bytes.fromhex(hashlib.sha1(result).hexdigest())
    with open(gitdir / "index", "wb") as f:
        f.write(result)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    if details:
        indexes = read_index(gitdir)
        result = []
        string = ""
        for index in indexes:
            string += str(oct(index.mode)[2:]) + " "
            string += str(bytes.hex(index.sha1)) + " "
            string += "0\t"
            string += index.name
            result.append(string)
            string = ""
        print("\n".join(result))
    else:
        file_names = [index.name for index in read_index(gitdir)]
        print("\n".join(file_names))


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    entrances = read_index(gitdir)
    for path in paths:
        with path.open("rb") as f:
            data = f.read()
        stat = os.stat(path)
        entrances.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=0,
                mtime_s=int(stat.st_mtime),
                mtime_n=0,
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(hash_object(data, "blob", write=True)),
                flags=7,
                name=str(path),
            )
        )
    if write:
        write_index(gitdir, sorted(entrances, key=lambda x: x.name))
