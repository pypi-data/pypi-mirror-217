"""
Retrieves human text from the code and pipes it via spell checker.

First, formatter collects all comments and doc strings. After that, it strips
tech text, and sends the rest to spell checker.

The tech text in comments could be:
 * code snippets
 * variable references, function names
 * technical comments, like `noqa`, `pylint`

"""

from pygments.token import Token
from pygments.formatter import Formatter
import re
import logging

log = logging.getLogger(__name__)


def tr(txt):
    rc = ""
    for c in txt:
        if c.isspace():
            rc += c
        else:
            rc += " "
    return rc


def repl(matchobj):
    txt = matchobj.group(0)
    return tr(txt)


class CodeFormatter(Formatter):
    """
    Retrieve human text from the code.

    The flow:
     1. collect all comments and doc strings
     2. strip tech text
         * fenced block - multi-line text between 3 back ticks, similar to
           `<pre>` tag
         * in-line code - text between back ticks, similar to `<code>`
         * special comment - e.g. `noqa`, `pylint`
         * custom regex - lines matching user-defined regex
    """

    # comment directive consists from 3 parts: header, command and value.
    # for example: `docspell: accept foo,bar`
    comment_prefix = "docspell"
    command_accept_len = 2

    def __init__(self, kwargs):
        log.debug("%s init", self.__class__.__name__)
        Formatter.__init__(self)
        self.linters = {"docspell": self.tr_linter_docspell}
        for e in kwargs.get("linters", []):
            self.linters[e] = lambda x: x
        self.block_marks = kwargs.get("block-marks", [])
        self.custom = kwargs.get("custom", [])
        self.spell_dict = []

    def format(self, tokensource, outfile):  # noqa: A003
        txt = self.tr_code(tokensource)
        txt = self.tr_md_code_block(txt)
        txt = self.tr_md_code(txt)
        txt = self.tr_custom(txt)
        outfile.write(txt)

    def tr_code(self, tokensource):
        tokens = []
        for ttype, value in tokensource:
            if log.getEffectiveLevel() == logging.DEBUG:
                log.debug(
                    "token: type %s, value '%s'", ttype, value.replace("\n", "\\n")
                )
            if (
                ttype == Token.Comment
                or ttype == Token.Comment.Single
                or ttype == Token.Comment.Multiline
            ):
                log.debug("token: accept")
                nv = self.tr_comment_hdr(value)
                nv = self.tr_linter(nv)
                if ttype == Token.Comment.Multiline:
                    nv = self.tr_comment_block_marks(nv)
            elif ttype == Token.Literal.String.Doc:
                log.debug("token: accept")
                nv = value
            else:
                nv = tr(value)
            tokens.append(nv)
        return "".join(tokens)

    def tr_comment_hdr(self, txt):
        """
        Replace a header of a single line comment with spaces.

        If header starts with non-word character (`#`, ';', `"`, `//`, `--`)
        replace until first space or word character.

        If header starts with word character (`REM') replace until first space
        character.
        """

        def break_after_word(c):
            return not c.isalpha()

        def break_after_punct(c):
            return c.isspace() or c.isalnum()

        if txt[0].isalpha():
            brk = break_after_word
        else:
            brk = break_after_punct
        rc = ""
        for i, c in enumerate(txt + " "):  # noqa: B007
            if brk(c):
                break
            rc += " "

        rc += txt[i:]
        return rc

    def tr_custom(self, txt):
        for reg in self.custom:
            log.debug("tr_custom: '%s'", reg)
            txt = re.sub(reg, repl, txt)
        return txt

    def tr_comment_block_marks(self, txt):
        if not self.block_marks:
            return txt
        line_reg = [re.escape(i) for i in self.block_marks]
        reg = "(?m)^[ \\t]*(?P<marker>" + "|".join(line_reg) + ")"
        log.debug("tr_comment_block_marks: reg '%s'", reg)
        return re.sub(reg, repl, txt)

    def tr_linter(self, txt):
        """Remove linter comments, `noqa`, `pylint`, `eslint`."""

        def _dispatch(matchobj):
            txt = matchobj.group(0)
            name = matchobj.group("name")
            args = matchobj.group("args")
            log.debug("matchobj: cmd '%s', args '%s'", name, args)
            self.linters[name](args)
            return tr(txt)

        line_reg = [re.escape(i) for i in self.linters.keys()]
        reg = "\\s*\\b(?P<name>" + "|".join(line_reg) + ")\\b:?\\s*(?P<args>.*)?$"
        return re.sub(reg, _dispatch, txt)

    def tr_linter_docspell(self, txt):
        log.debug("tr_linter_docspell: args %s", txt)
        txt = txt.split()
        log.debug("internal command: %s", txt)
        if len(txt) == self.command_accept_len and txt[0] == "accept":
            log.debug("accept words '%s'", txt[1])
            self.spell_dict += txt[1].split(",")

    def tr_md_code(self, txt):
        reg = "(?P<open>`+)[^`\\n]+?(?P=open)"
        return re.sub(reg, repl, txt)

    def tr_md_code_block(self, txt):
        reg_indent = "(?P<indent>^[ \\t]*)"
        reg = "(?m)" + reg_indent + "(?P<open>`{3,})[ \\t]*$\\n"
        reg += "((?P=indent).*$\\n)*?"
        reg += "(?P=indent)(?P=open)[ \\t]*$"
        return re.sub(reg, repl, txt)
