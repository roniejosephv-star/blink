from enum import Enum
from pathlib import Path
import hashlib
import shutil
import urllib.request
import git
import re
import json


class mpypkg:
    """! Libary that helps create reproducible builds based on micropython packages (package.json)

    Install all files and dependencies of a Micropython project package in a local directory.
    """

    class URL_TYPE(Enum):
        """! @private URL types Enum
        """
        PATH = 0
        GITPATH = 1
        MPYLIB = 10
        HTTP = 20
        SHORTURL = 21

    SHORTURL_LIST = [
        ("codeberg", "https://codeberg.org", "api/v1/repos/{user}/{repos}/raw/{filepath}?ref={ref}", "main"),
        ("github", "https://raw.githubusercontent.com", "{user}/{repos}/{ref}/{filepath}", "HEAD"),
        ("gitlab", "https://gitlab.com", "api/v4/projects/{user}%2F{repos}/repository/files/{filepath}/raw?ref={ref}", "main")
    ]

    def __init__(self, libdir="lib", dryrun=False):
        """! Initial settings for build process

        @param libdir  str: sub path for dependencies (default="lib")
        @param dryrun  bool: if True, no file will be copied or deleted
        """
        if libdir.lower() in ["none", "", "/"]:
            self.libdir = None
        else:
            self.libdir = libdir
        self.dryrun = dryrun

    def _abort(self, msg):
        """! @private Stop build process

        @param msg  str: reason for the assertion
        """
        raise AssertionError(msg)

    def _download_file(self, url):
        """! @private Download a file

        @param url  str: download URL
        """
        content = None
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read()
        except Exception as e:
            self._abort(e)
        return content

    def _write_file(self, urltype, src, dest):
        """! @private Write or copy a file to the build dir

        @param urltype  self.URL_TYPE: type of the url
        @param src  str: source file
        @param dest  str: destination path
        """
        print(f"+ Copy {src} -> {dest}")
        if not self.dryrun:
            if urltype == self.URL_TYPE.PATH:
                shutil.copy2(src, dest)
            else:
                fdata = self._download_file(src)
                with open(dest, "w") as f:
                    f.write(fdata.decode('utf-8'))

    def _get_relative_filename(self, pkg_url, fname):
        """! @private Convert an absolute source path in urls section into a relative path

        @param pkg_url  str: package root url
        @param fname  str: source path from section urls
        """
        fname_rel = fname
        if fname.startswith("/"):
            fname_rel = fname.replace(f"{pkg_url}/", "")
        else:
            for shorturl in self.SHORTURL_LIST:
                if fname.startswith(shorturl[0]):
                    search = re.compile(f"^{shorturl[0]}:[^/]+/[^/]+/")
                    fname_rel = search.sub("", fname)
                    break
        if fname_rel != fname:
            print("WARNING: Absolute source url not expected in section 'urls'. Trying to convert in a relative project path.")
            print(f"+ Converted {fname} -> {fname_rel}")
        return fname_rel

    def _copy_file(self, urltype, pkg_url, fname, dest):
        """! @private

        @param urltype  self.URL_TYPE: type of the url
        @param pkg_url  str: package root url
        @param fname  str: source path from section urls
        @param dest  str: destination path

        @retval hashlib.HASH|None: md5 checksum of the copied file, None if no file copied
        """
        fhash = None
        dest_dir = dest.parent
        if not self.dryrun and not dest_dir.exists():
            dest_dir.mkdir(parents=True, exist_ok=True)
        fname = self._get_relative_filename(pkg_url, fname)
        if urltype == self.URL_TYPE.PATH:
            src = Path.joinpath(pkg_url, fname)
            self._write_file(urltype, src, dest)
        elif urltype == self.URL_TYPE.GITPATH:
            pkg_git = pkg_url.split("@")
            try:
                repo = git.Repo(pkg_git[0])
            except git.InvalidGitRepositoryError as e:
                self._abort(f"No Git repository found: {e}")
            try:
                content = repo.git.show(f"{pkg_git[1]}:{fname}")
            except git.GitCommandError as e:
                self._abort(f"Cannot load {fname}: {e}")
            with open(dest, "w") as f:
                f.write(content)
        elif urltype == self.URL_TYPE.MPYLIB:
            src = f"{pkg_url}/{fname}"
            self._write_file(urltype, src, dest)
        elif urltype in [self.URL_TYPE.HTTP, self.URL_TYPE.SHORTURL]:
            # Replacing "/" with "%2F" is especially needed for gitlab, but works also for all others
            src = pkg_url.format(filepath=fname.replace("/", "%2F"))
            self._write_file(urltype, src, dest)
        if not self.dryrun and dest.exists():
            with open(dest, "rb") as f:
                fhash = hashlib.md5()
                while chunk := f.read(8192):
                    fhash.update(chunk)
        return fhash

    def _copy_pkg_urls(self, builddir, urltype, pkg_url, flist, loglist):
        """! @private copy all files from the section "urls" into build directory

        @param builddir  str: build directory
        @param urltype  self.URL_TYPE: type of the url
        @param pkg_url  str: package root url
        @param flist  list: all entries from the "urls" section
        @param loglist  list: list of copied/written files with their md5 checksum

        @retval list  current list of copied/written files with their md5 checksum
        """
        if Path(builddir).exists():
            builddir = Path(builddir)
        for f in flist:
            if f[0].startswith("/"):
                dest = Path.joinpath(builddir, f[0].lstrip("/"))
            else:
                if self.libdir is not None:
                    dest = Path.joinpath(builddir, self.libdir, f[0])
                else:
                    dest = Path.joinpath(builddir, f[0])
            fhash = self._copy_file(urltype, pkg_url, f[1], dest)
            if fhash is not None:
                fstring = str(dest.relative_to(builddir))
                for f in loglist:
                    if f[0] == fstring:
                        if f[1] != fhash.hexdigest():
                            self._abort(f"Same file with different hashes: {fstring}")
                        break
                loglist.append((fstring, fhash.hexdigest()))
        return loglist

    def _copy_pkg_deps(self, builddir, deplist, loglist):
        """! @private install all dependencies "deps" into build directory

        @param builddir  str: build directory
        @param deplist  list: all entries from the "deps" section
        @param loglist  list: list of copied/written files with their md5 checksum
        """
        for d in deplist:
            if isinstance(d, str):
                d = d.split("@")
            pkg = d[0]
            if len(d) > 1:
                version = d[1]
            else:
                version = None
            self._build(builddir, pkg, version, loglist)

    def _test_pkg_is_path(self, package, version):
        """! @private checks if package dir is a path

        @param package  str: package url
        @param version  str: given package version

        @retval self.URL_TYPE|None  PATH if package dir is path, None if not
        @retval str|None  package root url, None if not PATH
        @retval dict|None  package.json content, None if empty
        """
        urltype = None
        pkg_url = None
        pkg_data = None
        if Path(package).exists():
            pkg_url = Path(package)
            if not pkg_url.is_dir():
                pkg_url = pkg_url.parent
            if version is None:
                urltype = self.URL_TYPE.PATH
                pkg = Path.joinpath(pkg_url, "package.json")
                if pkg.exists():
                    print(f'+ Read package {pkg}')
                    with open(pkg) as f:
                        try:
                            pkg_data = json.load(f)
                        except json.decoder.JSONDecodeError as e:
                            self._abort(e)
                else:
                    self._abort(f"{pkg} missing")
            else:
                urltype = self.URL_TYPE.GITPATH
                try:
                    repo = git.Repo(pkg_url)
                except git.InvalidGitRepositoryError as e:
                    self._abort(f"No Git repository found: {e}")
                pkg_url = f"{pkg_url}@{version}"
                try:
                    content = repo.git.show(f"{version}:package.json")
                except git.GitCommandError as e:
                    self._abort(f"Cannot load package.json: {e}")
                try:
                    pkg_data = json.loads(content)
                except json.decoder.JSONDecodeError as e:
                    self._abort(e)
        return urltype, pkg_url, pkg_data

    def _test_pkg_is_http(self, package, version):
        """! @private checks if package is a http(s) url

        @param package  str: package url
        @param version  str: given package version

        @retval self.URL_TYPE|None  HTTP|SORTURL if package url is http(s) url, None if not
        @retval str|None  package root url, None if not HTTP|SORTURL
        @retval dict|None  package.json content, None if empty
        """
        urltype = None
        pkg_url = None
        pkg_data = None
        pkg = package.split(":")
        if pkg[0] in ["http", "https"]:
            urltype = self.URL_TYPE.HTTP
            pkg_url = package.replace("package.json", "{filepath}")
            fcontent = self._download_file(package)
            if fcontent is not None:
                pkg_data = json.loads(fcontent)
        else:
            for shorturl in self.SHORTURL_LIST:
                if shorturl[0] == pkg[0]:
                    urltype = self.URL_TYPE.SHORTURL
                    if version is None:
                        version = shorturl[3]
                    par = pkg[1].split("/")
                    pkg_url = shorturl[1] + "/" + shorturl[2].format(user=par[0], repos=par[1], filepath="{filepath}", ref=version)
                    print(f'+ Download package {pkg_url.format(filepath="package.json")}')
                    fcontent = self._download_file(pkg_url.format(filepath="package.json"))
                    if fcontent is not None:
                        pkg_data = json.loads(fcontent)
                    break
        return urltype, pkg_url, pkg_data

    def _test_pkg_is_mpylib(self, package, version):
        """! @private checks if package is a micropython-lib url

        @param package  str: package url
        @param version  str: given package version

        @retval self.URL_TYPE|None  MPYLIB if package url is micropython-lib url, None if not
        @retval str|None  package root url, None if not MPYLIB
        @retval dict|None  package.json like converted content, None if not possible
        """
        urltype = None
        pkg_url = None
        pkg_data = None
        if version is None:
            version = "latest"
        url = f"https://micropython.org/pi/v2/package/py/{package}/{version}.json"
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read()
        except Exception:
            content = None
        if content is not None:
            urltype = self.URL_TYPE.MPYLIB
            pkg_url = "https://micropython.org/pi/v2/file"
            json_data = json.loads(content)
            print(f'+ Build package from {url}')
            urls = ""
            for url in json_data["hashes"]:
                urls += f'["{url[0]}", "{url[1][:2]}/{url[1]}"],'
            pkg_data = json.loads(f'{{"urls": [{urls.rstrip(",")}], "deps": [], "version": "{json_data["version"]}"}}')
        return urltype, pkg_url, pkg_data

    def _pprint_pkg_data(self, pkg_data):
        """! @private pretty print package.json content

        @param pkg_data  dict: package dictionary

        @retval str formatted dictionary string
        """
        datastring = json.dumps(pkg_data)
        for keyword in pkg_data.keys():
            datastring = datastring.replace(f'"{keyword}"', f'\n    "{keyword}"')
        datastring = datastring[:-1] + "\n  }"
        return datastring

    def _build(self, builddir, package, version=None, loglist=None):
        """! @private copy all files and the dependencies of the package into the build directory

        @param builddir  str: build directory
        @param package  str: package url
        @param version  str: given package version
        @param loglist  list: list of copied/written files with their md5 checksum

        @retval list  current list of copied/written files with their md5 checksum
        """
        if loglist is None:
            loglist = []
        print(f"Install {package} ({version})")
        urltype, pkg_url, pkg_data = self._test_pkg_is_path(package, version)
        if urltype is None:
            urltype, pkg_url, pkg_data = self._test_pkg_is_http(package, version)
        if urltype is None:
            urltype, pkg_url, pkg_data = self._test_pkg_is_mpylib(package, version)
        if pkg_data is not None:
            print(f'# ({urltype.name}) {pkg_url}: {self._pprint_pkg_data(pkg_data)}')
            if "urls" in pkg_data:
                loglist = self._copy_pkg_urls(builddir, urltype, pkg_url, pkg_data["urls"], loglist)
            if "deps" in pkg_data:
                self._copy_pkg_deps(builddir, pkg_data["deps"], loglist)
        else:
            self._abort(f"No package information found for {package} ({version})")
        return loglist

    def build(self, builddir, package, version=None):
        """! start build process

        @param builddir  str: build directory
        @param package  str: package url
        @param version  str: given package version

        @retval list  current list of copied/written files with their md5 checksum
        """
        return self._build(builddir, package, version)

    def clean(self, builddir):
        """! delete all files in the build directory

        @param builddir  str: build directory
        """
        builddir = Path(builddir)
        if not self.dryrun:
            for p in builddir.iterdir():
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()

    def manifest(self, mfdir, builddir, base="PORT", exclude=[]):
        """! delete all files in the build directory

        @param mfdir  str: directory for manifest.py
        @param builddir  str: build directory
        @param base  str:
                     - "PORT": include $(PORT_DIR)/boards/manifest.py
                     - "BOARD": include $(BOARD_DIR)/manifest.py
        @param exclude  list: files in the build directory which shall be not include in the manifest.py
        """
        mffile = Path.joinpath(Path(mfdir), "manifest.py")
        with open(mffile, 'w', encoding="utf-8") as mf:
            if base == "PORT":
                mf.write('include("$(PORT_DIR)/boards/manifest.py")\n')
            elif base == "BOARD":
                mf.write('include("$(BOARD_DIR)/manifest.py")\n')
            else:
                self._abort(f'Invalid argument for base manifest.py: {base}. (Expected: "PORT" or "BOARD")')
            builddir = Path(builddir).resolve()
            libdir = Path.joinpath(builddir, self.libdir)
            for module in builddir.rglob("*"):
                if module.is_file():
                    name = str(module.relative_to(builddir))
                    if name not in exclude:
                        path = builddir
                        if libdir != builddir and module.is_relative_to(libdir):
                            name = str(module.relative_to(libdir))
                            path = libdir
                        mf.write(f'module("{name}", base_path="{path}")\n')
