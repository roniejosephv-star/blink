#!/bin/bash
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

checkExitCode() {
    if [ $1 -ne 0 ] ; then
        exit $1
    fi
}

build_app() {
    builddir="${SCRIPTDIR}/build"
    mkdir -p "${builddir}"
    checkExitCode $?
    python3 -m pip install -t "${builddir}" -r "${SCRIPTDIR}/requirements.txt"
    checkExitCode $?
    cp -r "${SCRIPTDIR}/src/mpypkg" "${builddir}"
    checkExitCode $?
    rm -rf "${builddir}"/*.dist-info
    checkExitCode $?
    py3clean "${builddir}"
    checkExitCode $?
    python3 -m zipapp "${builddir}" -o mpypkg-cli -p "/usr/bin/env python3" -m "mpypkg.cli:main"
    checkExitCode $?
}

case $1 in
    --distclean)
        rm -r "${SCRIPTDIR}/build"
        checkExitCode $?
        ;;
    --clean)
        rm -r "${SCRIPTDIR}/build/mpypkg"
        checkExitCode $?
        ;;
esac

build_app

exit 0
