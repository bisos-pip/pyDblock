#!/bin/env python
# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: Handler for the =b:ai:file/particulars= dblock.

Registers itself with =updateDblock= under the signature =b:ai:file/particulars=.
This dblock takes no parameters; the handler derives all content from the file
path, the target directory, and the =AI-Activity.org= symlink present there.
#+end_org """

import pathlib
import typing

from bisos.pyDblock import updateDblock

_SIGNATURE = 'b:ai:file/particulars'

_COMPANION_CANDIDATES = [
    'AI-AGENTS.org',
    'AI-WORKFLOW.org',
    'AI-Activity.org',
    'AI-DevStatus.org',
    'README.org',
]


def _handler(
        filePath: pathlib.Path,
        targetDir: pathlib.Path,
        args: typing.Dict[str, str],
) -> str:
    activityLink = targetDir / 'AI-Activity.org'
    if activityLink.is_symlink():
        activity = activityLink.resolve().parent.name
    else:
        activity = ''

    companionDocs = [f for f in _COMPANION_CANDIDATES if (targetDir / f).exists()]

    lines = ['* AI Working Context\n']
    lines.append(f'  Working Directory: {targetDir}\n')
    lines.append(f'  File: {filePath.resolve()}\n')
    if activity:
        lines.append(f'  Activity: {activity}\n')
    if companionDocs:
        lines.append(f"  Companion Docs: {', '.join(companionDocs)}\n")
    return ''.join(lines)


updateDblock.registerHandler(_SIGNATURE, _handler)
