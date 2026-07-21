#!/bin/bash -i
#

# Safety check: must run from a directory named "test"
# from a non-tests directory by mistake.
if [[ "$(basename "$PWD")" != "tests" ]]; then
    echo "ERROR: verify.sh must be run from a directory named 'tests'." >&2
    echo "  Current PWD: $PWD" >&2
    exit 1
fi

lpDo ../bin/py-dblock.cs
# lpDo ../bin/py-dblock.cs -i updateDblocks  ./dblock_AI-WorkPlan.org
# lpDo ../bin/py-dblock.cs -i updateDblocks  ./dblock_hosts

function dblock_fileParticulars {
    # lpDo cp ./dblock_AI-WorkPlan.blank ./dblock_AI-WorkPlan.eldb
    # lpDo bx-dblock -i dblockUpdateFiles ./dblock_AI-WorkPlan.eldb  
    lpDo cp ./dblock_AI-WorkPlan.blank ./dblock_AI-WorkPlan.pydb
    lpDo py-dblock.cs -i updateDblocks ./dblock_AI-WorkPlan.pydb
    lpDo diff ./dblock_AI-WorkPlan.eldb ./dblock_AI-WorkPlan.pydb
}

lpDo dblock_fileParticulars

function dblock_subProcStdout {
    lpDo cp ./dblock_hosts.blank ./dblock_hosts.pydb
    lpDo py-dblock.cs -i updateDblocks ./dblock_hosts.pydb
    lpDo diff ./dblock_hosts.eldb ./dblock_hosts.pydb
}

lpDo dblock_subProcStdout
