"""
Code documentation spell checker.

`doc-spell` extracts documentation and comments from a code and sends them to
spell checker.

It features
 * support for programming languages: python, shell, makefile and more
 * support for configuration files: YAML, INI, TOML
 * private dictionaries, either as separate file or inline comments.
 * reports in gcc format 'file:line:column'

It does not work with markup (html, markdown or xml).

Please see `https://github.com/aanatoly/doc-spell` for details.

EPILOG:
Example:
Spell check python project, having python code, makefile and yaml
```
doc-spell src/*.py Makefile *.yml

```

"""


import pydevkit.log.config  # noqa: F401
from pydevkit.log import prettify
from pydevkit.argparse import ArgumentParser
from .cspell import spell_checker, UnsupportedFileError, SpellingError
from . import __version__
from .conf import conf_get, conf_init, CONFIG
import sys
import logging

log = logging.getLogger(__name__)


def get_args():
    p = ArgumentParser(help=__doc__, version=__version__)
    p.add_argument("-c", help="configuration file", dest="config", default=CONFIG)
    p.add_argument(
        "--init", help="create sample configuration file", action="store_true"
    )
    p.add_argument("files", help="files to check", nargs="*")

    return p.parse_known_args()


def main():
    args, unknown_args = get_args()
    if unknown_args:
        log.warning("Unknown arguments: %s", unknown_args)
        sys.exit(1)

    if args.init:
        conf_init()

    conf = conf_get(args.config)
    log.debug("config: %s", prettify(conf))
    rc = 0
    for f in args.files:
        try:
            spell_checker(f, conf)
            log.info("%s: spelling is ok", f)
        except UnsupportedFileError as exp:
            log.warning("%s: %s", exp.path, exp)
        except SpellingError as exp:
            log.error("%s: %s", exp.path, exp)
            rc = 1
        except Exception as exp:
            log.error("%s", exp)
            rc = 1
    return rc


if __name__ == "__main__":
    main()
