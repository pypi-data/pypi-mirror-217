import os
import sys
import argparse
from typing import Callable

from vomit import to_unicode, to_utf8, walker


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='python -m vomit')

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('-e', '--encode', action='store_true', help='indicate the file should be encoded')
    action_group.add_argument('-d', '--decode', action='store_true', help='indicate the file should be decoded')

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('-f', '--file', type=str, help='the file to encode or decode, defaults to stdin')
    input_group.add_argument('-s', '--source', type=str, help='the directory to encode or decode .py files recursively')

    parser.add_argument(
        '-i', '--ignore', type=str,
        help='comma separated values of files and directories to skip when using --source'
    )

    parser.add_argument(
        '-t', '--ext', type=str,
        help='comma separated values of extensions to include along ".py" when using --source'
    )

    return parser


def _output(code: str, dest: str | None):
    if not dest:
        print(code)
        return

    with open(dest, 'w') as f:
        f.write(code)


def _input(action: Callable[[str], str], src: str | None) -> str:
    if not src:
        code = ''.join(line for line in sys.stdin)
        return action(code)

    with open(src, 'r') as f:
        code = f.read()
        return action(code)


def _pipe(action: Callable[[str], str], source: str | None):
    code = _input(action, source)
    _output(code, source)


def _validate_input(source: str, msg: str, check: Callable[[str], bool]):
    if not os.path.exists(source):
        print(f'{msg} "{source}" not found')
        os._exit(1)

    if not check(source):
        print(f'"{source}" not a {msg}')
        os._exit(1)


if __name__ == '__main__':
    args = _parser().parse_args()
    action = to_unicode if args.encode else to_utf8

    if args.source:
        _validate_input(args.source, 'directory', os.path.isdir)
        for file in walker(args.source, args.ignore, args.ext):
            _pipe(action, file)
        os._exit(0)

    if args.file:
        _validate_input(args.file, 'file', os.path.isfile)
        _pipe(action, args.file)
        os._exit(0)

    _pipe(action, None)
