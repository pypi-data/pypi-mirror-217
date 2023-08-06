"""Load and validate configuration file."""

import yaml
import os
from yaml.loader import SafeLoader
from schema import Schema, Optional
import shutil
import sys
import logging

log = logging.getLogger(__name__)

CONFIG = ".doc-spell.yml"

schema = Schema(
    {
        "hunspell": {Optional("wordlists"): [str]},
        "rules": [
            {
                "name": str,
                "match": {"types": [str]},
                "ignore": {
                    Optional("linters"): [str],
                    Optional("block-marks"): [str],
                    Optional("custom"): [str],
                },
                Optional("wordlists"): [str],
            }
        ],
    }
)


def conf_get(path):
    if path == CONFIG and not os.path.isfile(path):
        log.warning("Configuration file '%s' does not exists.", path)
        log.warning("Create one with '--init' option")
        conf = {"hunspell": {}, "rules": []}
    else:
        log.info("reading configuration from `%s`", path)
        try:
            conf = yaml.load(open(path, "r"), Loader=SafeLoader)
        except Exception as exp:
            log.error("%s", exp)
            sys.exit(1)
    try:
        conf = schema.validate(conf)
    except Exception as exp:
        log.error("%s", exp)
        sys.exit(1)
    return conf


def conf_init():
    if os.path.exists(CONFIG):
        log.warning("file '%s' exists, won't overwrite", CONFIG)
        sys.exit(1)
    log.info("create '%s'", CONFIG)
    src = os.path.join(os.path.dirname(__file__), CONFIG)
    shutil.copyfile(src, CONFIG)
    sys.exit(0)
