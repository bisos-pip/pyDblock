#!/bin/env python
# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: General-purpose py-dblock dispatch engine.

Mimics org-mode's dblock model in pure Python:
- Handlers register under a signature string.
- =expandAll= scans a file for all =####+BEGIN: <signature> [args]= / =####+END:= blocks,
  parses the signature and keyword args from the BEGIN line, looks up the registered
  handler, and calls it with (filePath, targetDir, parsedArgs).
- Each handler is responsible for returning the replacement body text.
#+end_org """

import pathlib
import re
import typing

# ---------------------------------------------------------------------------
# Handler registry
# ---------------------------------------------------------------------------

# Maps signature string → callable(filePath, targetDir, args) -> str
_REGISTRY: typing.Dict[
    str,
    typing.Callable[[pathlib.Path, pathlib.Path, typing.Dict[str, str]], str]
] = {}


def registerHandler(
        signature: str,
        handler: typing.Callable[[pathlib.Path, pathlib.Path, typing.Dict[str, str]], str],
) -> None:
    _REGISTRY[signature] = handler


# ---------------------------------------------------------------------------
# BEGIN-line parser
# ---------------------------------------------------------------------------

# Matches the full dblock: BEGIN line (kept), body (replaced), END marker (kept).
_DBLOCK_RE = re.compile(
    r'(#{4}\+BEGIN:[ \t]+(\S+)([ \t][^\n]*)?\n)(.*?)(#{4}\+END:)',
    re.DOTALL,
)

# Matches :key value pairs; value is either a quoted string or a bare token.
_ARG_RE = re.compile(r':(\S+)\s+("(?:[^"\\]|\\.)*"|\S+)')


def _parseArgs(argsStr: typing.Optional[str]) -> typing.Dict[str, str]:
    if not argsStr:
        return {}
    result: typing.Dict[str, str] = {}
    for key, val in _ARG_RE.findall(argsStr):
        # Strip surrounding quotes if present, then decode org-mode backslash escapes
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
            val = val.replace('\\\\', '\\')
        result[key] = val
    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def expandAll(
        filePath: pathlib.Path,
) -> None:
    """Expand all registered dblocks in filePath in a single pass."""
    targetDir = filePath.parent
    text = filePath.read_text()

    def _replace(m: re.Match) -> str:  # type: ignore[type-arg]
        beginLine: str = m.group(1)
        signature: str = m.group(2)
        argsStr: typing.Optional[str] = m.group(3)
        endMarker: str = m.group(5)

        handler = _REGISTRY.get(signature)
        if handler is None:
            return m.group(0)  # no handler registered — leave block untouched

        args = _parseArgs(argsStr)
        body = handler(filePath, targetDir, args)
        return beginLine + body + endMarker

    new_text = _DBLOCK_RE.sub(_replace, text)
    filePath.write_text(new_text)
