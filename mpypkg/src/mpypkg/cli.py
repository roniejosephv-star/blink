#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path
from . import __version__
from . import mpypkg


def main():
    argparser = argparse.ArgumentParser(description="Install all files and dependencies of a Micropython project package in a local directory and create a custom manifest.py")
    argparser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    argparser.add_argument("--dry-run", action='store_true', help="do not copy or delete files")
    argparser.add_argument("--clean", action='store_true', help="delete content of build directory before build")
    argparser.add_argument("--build", action='store_true', help="build the project")
    argparser.add_argument("--mfdir", type=str, metavar="${MANIFESTDIR}", help="create manifest.py in ${MANIFESTDIR}")
    argparser.add_argument("--mfbase", type=str, default="PORT", metavar="${ROOT_MANIFEST}", help="PORT: include $(PORT_DIR)/boards/manifest.py, BOARD: include $(BOARD_DIR)/manifest.py (default: PORT)")
    argparser.add_argument("--mfexclude", type=str, action='append', metavar="${EXCLUDE_FILE}", help="${EXCLUDE_FILE} shall not be part of the manifest.py")
    argparser.add_argument("--libdir", type=str, default="lib", metavar="${LIBDIR}", help="sub path for dependencies (default: lib)")
    argparser.add_argument("--pkg", type=str, required=True, metavar="${PKGDIR}", help="url to the project (OS path, http url, micropython-lib name)")
    argparser.add_argument("builddir", type=str, metavar="${BUILDDIR}", help="build directory")
    args = argparser.parse_args()
    if not Path(args.builddir).is_dir():
        try:
            Path(args.builddir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(-1)
    mpy = mpypkg.mpypkg(args.libdir, args.dry_run)
    if args.clean:
        mpy.clean(args.builddir)
    if args.build:
        pkg = args.pkg.split("@")
        version = None
        if len(pkg) > 1:
            version = pkg[1]
        try:
            loglist = mpy.build(args.builddir, pkg[0], version=version)
            print("File List:")
            for f in loglist:
                print(f":{f[0]} ({f[1]})")
        except AssertionError as e:
            print(f"Build aborted: {e}", file=sys.stderr)
            sys.exit(-1)
        if args.mfdir is not None:
            if not Path(args.mfdir).is_dir():
                try:
                    Path(args.mfdir).mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    print(e, file=sys.stderr)
                    sys.exit(-1)
            if args.mfexclude is not None:
                mpy.manifest(args.mfdir, args.builddir, args.mfbase, args.mfexclude)
            else:
                mpy.manifest(args.mfdir, args.builddir, args.mfbase)
        print("Build finished with success.")
    sys.exit(0)


if __name__ == "__main__":
    main()
