#!/bin/bash
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

STARTDIR=$(pwd)
cd ${SCRIPTDIR}
VERSION=$(grep __version__ ../src/mpypkg/__init__.py)
VERSION="${VERSION#*\"}"
VERSION="${VERSION%%\"*}"
( cat Doxyfile ; echo "PROJECT_NAME = mpypkg" ; echo "PROJECT_NUMBER = ${VERSION}" ) | doxygen -
if [ ! -L html/docs ] || [ ! -e html/docs ]; then
    ln -rs -t html ../docs
fi
cd ${STARTDIR}
exit 0
