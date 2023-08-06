"""
Retrieves human text from the code and pipes it via spell checker.

First, formatter collects all comments and doc strings. After that, it strips
tech text, and sends the rest to spell checker.

The tech text in comments could be:
 * code snippets
 * variable references, function names
 * technical comments, like `noqa`, `pylint`

"""

from pygments import highlight
from pygments.lexers import (
    get_lexer_by_name,
    guess_lexer_for_filename,
)
import subprocess as sp
import re
import sys
import os
import tempfile
from identify import identify
import logging
from pydevkit.log import prettify
from .formatters import CodeFormatter


log = logging.getLogger(__name__)


# {{{ hunspell invocation
class SpellingError(Exception):
    def __init__(self, path, errors):
        self.path = path
        self.message = "%d spellng errors" % errors

    def __str__(self):
        return self.message


def hunspell_run(path, code, dict_fname):
    p = sp.Popen(
        ["hunspell", "-a", "-p", dict_fname],
        universal_newlines=True,
        stdin=sp.PIPE,
        stdout=sp.PIPE,
    )

    # read one-line header
    p.stdout.readline()

    errors = 0
    for no, line in enumerate(code.splitlines()):
        if line == "" or line.isspace():
            continue
        log.debug("line %d '%s'", no, line)
        for wm in re.finditer("\\b\\w+\\b", line):
            log.debug(">> %s", wm.group(0))
            # feed a line with one word
            p.stdin.write(wm.group(0) + "\n")
            p.stdin.flush()
            # read an answer for a word
            txt = p.stdout.readline().strip()
            # read an answer for a line
            p.stdout.readline()
            log.debug("<< '%s'", txt)
            if txt == "*":
                continue
            errors += 1
            msg = "%s:%s:%s: %s" % (path, no + 1, wm.start(0), txt)
            print(msg, file=sys.stderr)
    return errors


def hunspell(code, path, conf, spell_dict):
    """
    Pipe code to `hunspell` and print errors in gcc format `file:line:column`.

    `spell_dict` is a personal dictionary. Is is loaded for the single run and
    not saved to disk.
    """
    tconf = conf["hunspell"]
    # add personal word list
    dict_fp, dict_fname = tempfile.mkstemp(prefix="doc-spell-dict-")
    dict_fp = open(dict_fname, "w")

    def add_word_list(name, words):
        log.debug("add dictionary '%s'", name)
        for word in words:
            w = word.strip()
            if not w:
                continue
            log.debug("add word '%s'", w)
            dict_fp.write(w + "\n")

    add_word_list("inline", spell_dict)
    word_lists = tconf.get("wordlists", [])
    for wl in word_lists:
        try:
            words = open(wl, "r").readlines()
        except Exception as exp:
            log.error("%s", exp)
            continue
        add_word_list(wl, words)
    dict_fp.close()

    # save code for debugging
    code_fp, code_fname = tempfile.mkstemp(prefix="doc-spell-code-")
    code_fp = open(code_fname, "w")
    code_fp.write(code)
    code_fp.close()

    errors = hunspell_run(path, code, dict_fname)
    if log.getEffectiveLevel() != logging.DEBUG:
        os.unlink(dict_fname)
        os.unlink(code_fname)
    else:
        log.debug("remove tmp code: %s", code_fname)
        log.debug("remove tmp dict: %s", dict_fname)
    if errors:
        raise SpellingError(path, errors)


# }}} noqa ERA001


class UnsupportedFileError(Exception):
    def __init__(self, path, msg):
        self.path = path
        self.message = "unsupported file type: " + msg

    def __str__(self):
        return self.message


# weights of lexer aliases, to find best match
aliases = {
    "text": -1,
    "shell": 1,
    "bash": 2,
    "c": 1,
    "c++": 2,
}


def get_lexer(path, *, debug=False):
    tags = identify.tags_from_path(path)
    if "symlink" in tags:
        path = os.path.realpath(path)
        log.debug("redirect to '%s'", path)
        tags = identify.tags_from_path(path)

    accept = {"file", "text"}
    rc = accept - tags
    if len(rc):
        raise UnsupportedFileError(path, "not a text file")

    if "plain-text" in tags:
        return get_lexer_by_name("text", stripall=False)

    tags = tags - accept
    tags = tags - {"executable", "non-executable"}
    tags = sorted(tags, key=lambda x: aliases.get(x, 0), reverse=True)
    log.debug("get lexer from identify tags %s", tags)
    rc = None
    for tag in tags:
        try:
            lexer = get_lexer_by_name(tag, stripall=False)
        except Exception:
            lexer = None
        log.debug("lexer for '%s': %s", tag, lexer)
        if rc is None:
            rc = lexer
        if not debug:
            break
    if rc:
        return rc

    log.debug("get lexer from guess_lexer_for_filename")
    buf = open(path, "r").read(1024)
    try:
        return guess_lexer_for_filename(path, buf)
    except Exception:
        return None


doc_types = {
    "text",
    "html",
    "markdown",
    "xml",
    "qml",
    "rst",
    "xhtml",
    "pug",
    "jade",
    "scaml",
    "xslt",
}


def get_formatter(conf, tags):
    stags = set(tags)
    rc = stags - doc_types
    if len(stags) != len(rc):
        return None

    def rule_get_value(rule, name, keys):
        try:
            for key in keys:
                rule = rule.get(key)
        except Exception:
            rule = None
        log.debug("rule '%s', path %s, value %s", name, keys, rule)
        return rule

    def rule_match(r, name, stags):
        rtypes = rule_get_value(r, name, ["match", "types"])
        if rtypes is None:
            return False
        if "*" in rtypes:
            log.debug("rule '%s', match by type '*'", name)
            return True
        rc = stags.intersection(set(rtypes))
        if len(rc):
            log.debug("rule '%s', match by type %s", name, rc)
            return True
        return False

    kwargs = {}
    ignore_keys = ["block-marks", "custom", "linters"]
    for no, rule in enumerate(conf["rules"]):
        name = "%d %s" % (no, rule.get("name", "noname"))
        if not rule_match(rule, name, stags):
            continue
        ignore = rule_get_value(rule, name, ["ignore"])
        if ignore is None:
            continue
        for k, v in ignore.items():
            if k in ignore_keys and v and isinstance(v, list):
                kwargs[k] = kwargs.get(k, []) + v
    log.debug("kwargs %s", prettify(kwargs))
    return CodeFormatter(kwargs)


def spell_checker(path, conf):
    """
    Obtain human text from the code and pipe it via hunspell.

    In case of spelling errors, raises an exception.
    """
    log.info("%s: starting", path)
    lexer = get_lexer(path, debug=True)
    log.debug("lexer: %s, aliases %s", lexer, lexer.aliases if lexer else None)
    if not lexer:
        raise UnsupportedFileError(path, "no lexer found")
    tags = [t.split("+")[0] for t in lexer.aliases]
    tags = list(set(tags))
    log.info("%s: associated types: %s", path, lexer.aliases)
    formatter = get_formatter(conf, tags)
    if not formatter:
        raise UnsupportedFileError(path, "no formatter found")
    code = open(path, "r").read()
    code = highlight(code, lexer, formatter)
    hunspell(code, path, conf, formatter.spell_dict)
