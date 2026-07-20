#!/bin/env python
# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: Handler for the =bx:dblock:global:run-result-stdout= dblock.

Runs the shell command given in the =:command= argument and replaces the
dblock body with the command's stdout, followed by a trailing newline.
If the command fails the block body is replaced with an error comment.
#+end_org """

import pathlib
import subprocess
import typing

from bisos.pyDblock import updateDblock

_SIGNATURE = 'bx:dblock:global:run-result-stdout'


def _handler(
        filePath: pathlib.Path,
        targetDir: pathlib.Path,
        args: typing.Dict[str, str],
) -> str:
    command = args.get('command', '')
    if not command:
        return '# bx:dblock:global:run-result-stdout: no :command argument\n'

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=str(targetDir),
        )
        output = result.stdout
        if not output.endswith('\n'):
            output += '\n'
        return output
    except Exception as exc:
        return f'# bx:dblock:global:run-result-stdout error: {exc}\n'


updateDblock.registerHandler(_SIGNATURE, _handler)