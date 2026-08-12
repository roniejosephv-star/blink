# mpypkg

Tool that helps create reproducible builds based on micropython packages (package.json)

With `mpypkg`, all files and dependencies of a Micropython project package are stored in a local directory.

The content of this directory can then be cloned/copied to the target using `mpremote cp`.
```bash
$ mpremote cp -r ${path/to/build/directory}/* :
```

In addition, a custom `manifest.py` can be generated with which the project files can be integrated ("frozen") into the board firmware.
```bash
$ cd ${path/to/clone/of/micropython}/ports/${PORT}
$ make BOARD=${BOARD} FROZEN_MANIFEST=${path/to/custom/manifest}/manifest.py
```

Supported package sources:
* local paths and Git repositories
* http(s) URLs
* micropython-lib index

## How to use it for your project

Create a `package.json` with a "urls" and a "deps" lists in your project directory.

```
{
  "urls": [
  ],
  "deps": [
  ]
}
```

The "urls" list contains all your project files and their location on the target.
If the path for the target starts with "/", the file is copied to the build root directory.
Otherwise, it is copied to the ${LIBDIR} (default: /lib) directory.

Example:
```
  "urls": [
    ["/myproject.py", "src/myproject.py"],
    ["/main.py", "src/main.py"],
    ["/etc/config.py", "config.py"]
  ],
```

Add all the project dependencies to the "deps" list.

Example:
```
  "deps": [
    ["/path/to/my/other/project", "1.0.0"],
    ["bundle-networking", "0.2.0"],
    ["codeberg:yvo/micropython-ahtx", "v0.0.1"]
  ]
```

Then run `mpypkg-cli`:
```bash
$ cd ${path/to/your/project}
$ mpypkg-cli --clean --build --mfdir build --pkg . build/py
```
The `build/py` directory will then contain all the necessary target files for your project.

Now you can copy the content of the `build/py` directory to the target using mpremote:
```bash
$ mpremote cp -r build/py/* :
```

If you want to include the project files into the board firmware, you can do this with the also generated custom `manifest.py`:
```bash
$ cd ${path/to/clone/of/micropython}/ports/${PORT}
$ make BOARD=${BOARD} FROZEN_MANIFEST=${path/to/your/project}/build/manifest.py
```


## Usage details

```
usage: mpypkg-cli [-h] [--version] [--dry-run] [--clean] [--build] [--mfdir ${MANIFESTDIR}] [--mfbase ${ROOT_MANIFEST}]
                  [--mfexclude ${EXCLUDE_FILE}] [--libdir ${LIBDIR}] --pkg ${PKGDIR}
                  ${BUILDDIR}

positional arguments:
  ${BUILDDIR}                   build directory

options:
  -h, --help                    show this help message and exit
  --version                     show program's version number and exit
  --dry-run                     do not copy or delete files
  --clean                       delete content of build directory before build
  --build                       build the project
  --mfdir ${MANIFESTDIR}        create manifest.py in ${MANIFESTDIR}
  --mfbase ${ROOT_MANIFEST}     PORT: include $(PORT_DIR)/boards/manifest.py, 
                                BOARD: include $(BOARD_DIR)/manifest.py
                                (default: PORT)
  --mfexclude ${EXCLUDE_FILE}   ${EXCLUDE_FILE} shall not be part of the manifest.py
  --libdir ${LIBDIR}            sub path for dependencies (default: lib)
  --pkg ${PKGDIR}               url to the project (OS path, http url, micropython-lib name)
```

Copying the content of `${BUILDDIR}` to the target can be done with mpremote:
```bash
$ mpremote cp -r "${BUILDDIR}"/* :
```

With the created custom `manifest.py` the project files can be integrated ("frozen") into the board firmware:
```bash
$ cd ${path/to/clone/of/micropython}/ports/${PORT}
$ make BOARD=${BOARD} FROZEN_MANIFEST=${path/to/MANIFESTDIR}/manifest.py
```

### Supported URL formats

#### Local Paths and Git Repositories

Absolute and relative paths are supported. 
If a reference (branch/tag/commit) is added, a .git directory is expected in the path.

**Examples:**
* /path/to/package
* path/to/package
* ../path/to/package@1.0.0

#### HTTP URLs

For some hosting platforms are shortcuts available.

The shortcuts have the following format:<br>
{platform}:{user}/{repos}\@{branch/tag/commit}

The following platforms are supported:
* codeberg
* github
* gitlab

**Examples:**
* codeberg:yvo/micropython-ahtx\@v0.0.1

Full HTTP URLs are also supported.

For example the full HTTP URL for a codeberg repository would look like this:<br>
https: //codeberg.org/api/v1/repos/{user}/{repos}/raw/package.json?ref={branch/tag/commit}

**Examples:**
* https://codeberg.org/api/v1/repos/yvo/micropython-ahtx/raw/package.json?ref=v0.0.1


#### micropython-lib

A package from the micropython-lib is referenced with its name.

**Examples:**
* bundle-networking\@latest
* ds18x20@0.1.0
* dht


## Build

### CLI

To build the CLI `mpypkg-cli`, run the build script `build.sh`:
```bash
$ build.sh
```

### API

`mpypkg` can be also used as a libary.

API documentation can be generated with doxygen:
```bash
$ docs/mkdoc.sh
```
The API documentation is generated in the `docs/html` directory.


## Links

- [MicroPython](https://www.micropython.org)


## License

GPL version 3.0 or any later version.
