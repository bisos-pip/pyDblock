#!/bin/bash -i
#

# Safety check: must run from a directory named "test"
# from a non-test directory by mistake.
if [[ "$(basename "$PWD")" != "test" ]]; then
    echo "ERROR: verify.sh must be run from a directory named 'test'." >&2
    echo "  Current PWD: $PWD" >&2
    exit 1
fi

lpDo ../bin/py-dblock.cs
lpDo ../bin/py-dblock.cs -i updateDblocks  ./dblock_AI-WorkPlan.org
lpDo ../bin/py-dblock.cs -i updateDblocks  ./dblock_hosts

