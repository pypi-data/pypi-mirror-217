import time
import pytest
import re
import os

from memotools import Tag
import mypy.api


def test_readme_code():
    readme_file = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    with open(readme_file) as f:
        text = f.read()
    m = re.search('```(.+?)```', text, flags=re.DOTALL)
    assert m
    code = m.group(1)
    assert code.startswith('python')
    code = code[6:].strip()
    exec(code, globals(), globals())


def test_types():
    files = []
    for dirpath, dirnames, filenames in os.walk(
        os.path.join(os.path.dirname(__file__), '..', 'memotools'),
    ):
        for filename in filenames:
            if filename.endswith('.py'):
                files.append(os.path.join(dirpath, filename))
    stdout, stderr, _ = mypy.api.run(['--strict'] + files)
    if 'Success: no issues found' not in stdout:
        print("MyPy stdout:\n", stdout)
        print("MyPy stderr:\n", stderr)
        raise AssertionError("MyPy found type errors")


if __name__ == "__main__":
    test_readme_code()
    test_types()
