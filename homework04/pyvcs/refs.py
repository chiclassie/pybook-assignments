#  type: ignore
import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    with (gitdir / ref).open("w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    with (gitdir / ref).open("w") as f:
        f.write(name)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD" and not is_detached(gitdir):
        return ref_resolve(gitdir, get_ref(gitdir))
    with (gitdir / refname).open() as f:
        return f.read().strip()


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    artificial_ref = get_ref(gitdir)
    if (gitdir / artificial_ref).exists():
        return ref_resolve(gitdir, artificial_ref)
    else:
        return None


def is_detached(gitdir: pathlib.Path) -> bool:
    try:
        get_ref(gitdir)
        return False
    except IndexError:
        return True


def get_ref(gitdir: pathlib.Path) -> str:
    with (gitdir / "HEAD").open() as file:
        ref = file.read().strip().split()[1]
        return ref
