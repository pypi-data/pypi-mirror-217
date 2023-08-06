from compileall import compile_file
from pathlib import Path
from typing import Optional, Tuple

import click


def compile_command(path: Path, recursive: bool = False, in_place: bool = False, create_empty_init: bool = False, exclude_patterns: Tuple[str] = tuple()):
    if (create_empty_init and not path.is_dir()):
        raise ValueError(
            '--create-empty-init flag can only be used when path supplied is a directory.')

    path = Path(path)
    _clear_pycache_dir(path, missing_ok=True)
    compileall(path, recursive, exclude_patterns=exclude_patterns)

    if (in_place):
        replace_py_with_pyc(path, recursive, exclude_patterns=exclude_patterns)

    if (create_empty_init):
        _create_init_file(dir=path)


def compileall(path: Path, is_recursive: bool, exclude_patterns: Tuple[str]):
    """
    Simple wrapper around python compileall package to compile .py to .pyc files.

    Note that created .pyc files are under the __pycache__ directory.
    """
    assert (path.exists())
    if (path.is_dir()):
        if (not is_recursive):
            for file in path.glob('*.py'):
                compileall(file, is_recursive=is_recursive,
                           exclude_patterns=exclude_patterns)
            return

        for file in path.iterdir():
            compileall(file, is_recursive=is_recursive,
                       exclude_patterns=exclude_patterns)

    elif (path.is_file() and path.suffix == '.py'):
        for pattern in exclude_patterns:
            if (path.match(pattern)):
                click.echo(f'Skipping file \'{path}\'')
                return
        click.echo(f'Compiling file \'{path}\'')
        compile_file(path)


def replace_py_with_pyc(path: Path, is_recursive: bool, exclude_patterns: Tuple[str]):
    """Replace .py with .pyc files """
    assert (path.exists())

    if (path.is_dir()):
        _replace_py_with_pyc_dir(
            path, is_recursive, exclude_patterns=exclude_patterns)
    elif (path.is_file()):
        assert (path.suffix == '.py')
        _replace_py_with_pyc_file(path, exclude_patterns=exclude_patterns)

    _clear_pycache_dir(path, missing_ok=True)


def _replace_py_with_pyc_dir(path: Path, is_recursive: bool, exclude_patterns: Tuple[str]):
    for child in path.iterdir():
        if (child.is_dir() and is_recursive):
            _replace_py_with_pyc_dir(
                child, is_recursive, exclude_patterns=exclude_patterns)
            continue

        if (child.is_file() and child.suffix == '.py'):
            _replace_py_with_pyc_file(child, exclude_patterns=exclude_patterns)
            continue


def _replace_py_with_pyc_file(python_file_path: Path, exclude_patterns: Tuple[str]):
    """Replace a .py file with its corresponding .pyc file in the __pycache__ directory."""
    assert (python_file_path.is_file() and python_file_path.suffix == '.py')
    for pattern in exclude_patterns:
        if python_file_path.match(pattern):
            return

    compiled_file = _get_pycache_pyc_from_py(python_file_path)
    if (compiled_file is None):
        raise FileNotFoundError(
            f'.pyc file does not exist for the file {python_file_path.as_posix()}')
    python_file_path.unlink()
    compiled_file.rename(python_file_path.with_suffix('.pyc'))


def _get_pycache_pyc_from_py(python_file_path: Path) -> Optional[Path]:
    """For a given .py file, get its corresponding .pyc file path in the __pycache__ directory."""
    assert (python_file_path.is_file() and python_file_path.suffix == '.py')
    pycache_dir = python_file_path.parent / '__pycache__'
    query = list(pycache_dir.glob(python_file_path.stem + '.cpython-*.pyc'))
    if (len(query) == 0):
        return None
    assert (len(query) == 1)
    compiled_file = query[0]

    return compiled_file


def _create_init_file(dir: Path) -> Path:
    """For a given directory, create an empty __init__.py file and return the resulting file as a Path object."""
    assert dir.is_dir()
    file = (dir / '__init__.py')
    file.touch()
    return file


def _clear_pycache_dir(path: Path, missing_ok: bool) -> None:
    """Given a directory or file, delete the __pycache__ folder."""
    if (path.is_file()):
        path = path.parent

    rmtree(path / '__pycache__', missing_ok=missing_ok)


# UTILITY

def rmtree(root: Path, missing_ok: bool):
    if (missing_ok and not root.exists()):
        return
    for p in root.iterdir():
        if p.is_dir():
            rmtree(p, missing_ok=missing_ok)
        else:
            p.unlink(missing_ok=True)

    root.rmdir()
