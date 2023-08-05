# SPDX-License-Identifier: MIT
"""Encode and decode VljuMap."""

import csv as py_csv
import io
import json as py_json
import re
import shlex
import urllib.parse
import warnings

from collections.abc import Callable, Generator, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from fnattr.util import escape
from fnattr.util.error import Error
from fnattr.util.multimap import MultiMap
from fnattr.vlju.types.ean.isbn import is_valid_isbn10, is_valid_isbn13
from fnattr.vljumap import VljuFactory, VljuMap

@dataclass
class DecodeFileResult:
    directory: Path
    stem: str
    suffix: str

EncodeCallable = Callable[[VljuMap, str | None], str]
DecodeCallable = Callable[[VljuMap, str, VljuFactory], VljuMap]
DecodeFileCallable = Callable[[VljuMap, Path, VljuFactory], DecodeFileResult]

class Encoder:
    """Scheme for for encoding and decoding VljuMap."""

    def __init__(self,
                 name: str,
                 encode: EncodeCallable | None,
                 decode: DecodeCallable | None,
                 decode_file: DecodeFileCallable | None = None,
                 desc: str | None = None,
                 description: str | None = None) -> None:
        self.name = name
        self.desc = desc or name
        self.description = description
        self.encode: EncodeCallable = encode or _unimplemented_encode
        self.decode: DecodeCallable = decode or _unimplemented_decode
        if decode_file:
            self.decode_file = decode_file
        else:
            self.decode_file = self._decode_file

    def can_encode(self) -> bool:
        return self.encode != _unimplemented_encode

    def can_decode(self) -> bool:
        return self.decode != _unimplemented_decode

    def _decode_file(self, n: VljuMap, p: Path,
                     f: VljuFactory) -> DecodeFileResult:
        self.decode(n, p.stem, f)
        return DecodeFileResult(p.parent, p.stem, p.suffix)

def _unimplemented_decode(_n: VljuMap, _s: str,
                          _factory: VljuFactory) -> VljuMap:
    raise NotImplementedError

def _unimplemented_encode(_n: VljuMap, _mode: str | None = None) -> str:
    raise NotImplementedError

# Global registry of named Encoders.
encoder: dict[str, Encoder] = {}
decoder: dict[str, Encoder] = {}

def _register_encoder(e: Encoder) -> Encoder:
    if e.can_encode():  # pragma: no branch
        encoder[e.name] = e
    if e.can_decode():
        decoder[e.name] = e
    return e

###############################################################################
#
# V3 Encoder
#
###############################################################################

V3_DESC = 'Default.'

V3_GRAMMAR = """
    v3        → v3seq «‘ ’» v3title «‘ ’» v3attrs
    v3title   → [title [‘ - ’ title]*]
    v3attrs   → [‘[’ v3kv [‘; ’ v3kv]* ‘]’]
    v3kv      → k ‘=’ v
    v3seq     → [digit (alnum | ‘.’)* ‘.’]
    a «j» b   → (a | b | ajb)
"""

V3_DESCRIPTION = """
  Encoder format v3 consists, in order, of optional sequence numbers,
  optional title and subtitles, and optional attributes.

  Sequence numbers begin with a digit and end with a period. Multiple sequence
  numbers are allowed, but they must be adjacent.

  Title and optional subtitles are separated by ‘ - ’ (including the spaces).

  Attributes are surrounded by ‘[ … ]’ and separated by ‘;’. (A space follows
  each semicolon when encoding, but is not required when decoding.) Each
  attribute consists of a key, optionally followed by ‘=’ and a value.

  Characters with special meaning to the encoding, or not allowed in file
  names, are represented using URL-style % encoding.
""" + V3_GRAMMAR

class V3Config(NamedTuple):
    """Properties used by V3 and variants."""

    quote: escape.Escape
    attr_start: str = '['
    attr_end: str = ']'
    attr_join: str = '; '
    attr_kv: str = '='
    title_join: str = ' - '
    seq_start: str = ''
    seq_end: str = '.'
    seq_join: str = '.'

V3_CONFIG = V3Config(
    quote=escape.Escape(
        escape.mkencode_urlish(escape.UNSAFE_ON_UNIX
                               + '[];='), urllib.parse.unquote))

def v3_encode(n: VljuMap, mode: str | None = None) -> str:
    return _v3_enc(V3_CONFIG, n, mode)

def v3_decode(n: VljuMap, s: str, factory: VljuFactory) -> VljuMap:
    return _v3_dec(V3_CONFIG, n, s, factory)

def v3_decode_file(n: VljuMap, p: Path,
                   factory: VljuFactory) -> DecodeFileResult:
    return _v3_dec_file(V3_CONFIG, n, p, factory)

v3 = _register_encoder(
    Encoder(
        'v3',
        v3_encode,
        v3_decode,
        v3_decode_file,
        desc=V3_DESC,
        description=V3_DESCRIPTION))

def _v3_enc(config: V3Config, n: VljuMap, mode: str | None) -> str:
    m = n.to_strings(mode)

    sequence = config.seq_join.join(m['n'])
    sequence = sequence and f'{config.seq_start}{sequence}{config.seq_end}'
    title_qjoin = config.title_join.translate(
        escape.mktrans_urlish(config.title_join.strip()))
    title = config.title_join.join(
        config.quote.encode(i).replace(config.title_join, title_qjoin)
        for i in m['title'])
    attrs = config.attr_join.join(
        kv_fmt(k, v, config.attr_kv, config.quote)
        for k, v in m.pairs()
        if k not in ('title', 'n'))
    attrs = attrs and f'{config.attr_start}{attrs}{config.attr_end}'
    return join_non_empty(' ', sequence, title, attrs)

def _v3_dec_file(config: V3Config, n: VljuMap, p: Path,
                 factory: VljuFactory) -> DecodeFileResult:
    bad_suffix = (
        config.attr_end in p.suffix
        and p.stem.count(config.attr_start) > p.stem.count(config.attr_end))
    if bad_suffix:
        stem = p.stem + p.suffix
        suffix = ''
    else:
        stem = p.stem
        suffix = p.suffix
    _v3_dec(config, n, stem, factory)
    return DecodeFileResult(p.parent, stem, suffix)

def _v3_dec(config: V3Config, n: VljuMap, s: str,
            factory: VljuFactory) -> VljuMap:
    return n.add_pairs(_v3_dec_iter(config, s), factory)

def _v3_dec_iter(config: V3Config, s: str) -> Iterable[tuple[str, str]]:
    if config.attr_start in s:
        s, _, attr = s.partition(config.attr_start)
    else:
        attr = ''
    if s:
        sequence, title = _v3_dec_seq(config, s)
        for v in sequence:
            yield ('n', v)
        if title:
            for i in title.split(config.title_join):
                yield ('title', escape.winfile.decode(i.strip()))
    if attr:
        for k, v in _v3_dec_attr(config, attr):
            yield (k, v)

def _v3_dec_attr(config: V3Config, s: str) -> Iterable[tuple[str, str]]:
    if s.endswith(config.attr_end):
        s = s[:-1]
    else:
        warnings.warn(f"Expected '{config.attr_end}' after '{s}'", stacklevel=0)
    for kv in s.split(config.attr_join.strip()):
        if config.attr_kv in kv:
            k, v = kv.split(config.attr_kv, 1)
        else:
            k = kv
            v = ''
        k = escape.winfile.decode(k.strip())
        v = escape.winfile.decode(v.strip())
        if not k:
            continue
        yield (k, v)

def _v3_dec_seq(config: V3Config, s: str) -> tuple[Iterable[str], str]:
    # Not currently used by any encoding:
    # if config.seq_start:
    #     if not s.startswith(config.seq_start):
    #         return ([], s)
    #     s = s[len(config.seq_start):]
    if config.seq_end not in s:
        return ([], s)
    seq: list[str] = []
    t = s
    lj = len(config.seq_join)
    while (((i := t.find(config.seq_join)) > 0) and t[: i].isalnum()
           and t[i + lj].isalnum() and t[0].isdigit()):
        seq.append(t[: i])
        t = t[(i + lj):]
    if ((i := t.find(config.seq_end)) > 0 and t[: i].isalnum()
            and t[0].isdigit()):
        seq.append(t[: i])
        t = t[(i + len(config.seq_end)):]
        return (seq, t.strip())
    return ([], s)

###############################################################################
#
# Windows Encoder
#
# Same as V3 except restricted to Windows file name characters.
#
###############################################################################

WIN_DESC = 'Like v3, but escape Windows forbidden characters.'
WIN_DESCRIPTION = """
  This is the same as v3 encoding format, except that additional characters
  are URL-escaped to comply with Windows file name limitations.
"""

WIN_CONFIG = V3Config(
    quote=escape.Escape(
        escape.mkencode_urlish(escape.UNSAFE_ON_WINDOWS
                               + '[];='), urllib.parse.unquote))

def win_encode(n: VljuMap, mode: str | None = None) -> str:
    return _v3_enc(WIN_CONFIG, n, mode)

def win_decode(n: VljuMap, s: str, factory: VljuFactory) -> VljuMap:
    return _v3_dec(WIN_CONFIG, n, s, factory)

def win_decode_file(n: VljuMap, p: Path,
                    factory: VljuFactory) -> DecodeFileResult:
    return _v3_dec_file(WIN_CONFIG, n, p, factory)

win = _register_encoder(
    Encoder(
        'win',
        win_encode,
        win_decode,
        win_decode_file,
        desc=WIN_DESC,
        description=WIN_DESCRIPTION))

###############################################################################
#
# V2 Encoder
#
# Same as V3 except attributes are surrounded by ‘{}’ instead of ‘[]’
# and joined by ‘;’ with no space.
#
###############################################################################

V2_DESC = 'An obsolete encoder.'

V2_GRAMMAR = """
    v2        → v2seq «‘ ’» v2title «‘ ’» v2attrs
    v2title   → [title [‘ - ’ title]*]
    v2attrs   → [‘{’ v2kv [‘;’ v2kv]* ‘}’]
    v2kv      → k ‘=’ v
    v2seq     → [digit (alnum | ‘.’)* ‘.’]
    a «j» b   → (a | b | ajb)
"""

V2_DESCRIPTION = """
  Encoder format v2 is similar to v3, except that attributes are surrounded
  by ‘{ … }' rather than ‘[ … ]’, and separated by semicolons with no space.

  This is supported only to covert old file names.
""" + V2_GRAMMAR

V2_CONFIG = V3Config(
    quote=escape.Escape(
        escape.mkencode_urlish(escape.UNSAFE_ON_UNIX + '{};='),
        urllib.parse.unquote),
    attr_start='{',
    attr_join=';',
    attr_end='}')

def v2_encode(n: VljuMap, mode: str | None = None) -> str:
    return _v3_enc(V2_CONFIG, n, mode)

def v2_decode(n: VljuMap, s: str, factory: VljuFactory) -> VljuMap:
    return _v3_dec(V2_CONFIG, n, s, factory)

def v2_decode_file(n: VljuMap, p: Path,
                   factory: VljuFactory) -> DecodeFileResult:
    return _v3_dec_file(V2_CONFIG, n, p, factory)

v2 = _register_encoder(
    Encoder(
        'v2',
        v2_encode,
        v2_decode,
        v2_decode_file,
        desc=V2_DESC,
        description=V2_DESCRIPTION))

###############################################################################
#
# V1 Encoder
#
###############################################################################

V1_DESC = 'An obsolete encoder.'

V1_GRAMMAR = """
    v1        → v1author ‘:’ «‘ ’» v1title «‘ ’» v1attrs
    v1author  → [author [‘; ’ author]*]
    v1title   → [title [‘: ’ title]*]
    v1attrs   → [‘[’ v1kv [‘,’ v1kv]* ‘]’]
    v1kv      → k ‘=’ v
    a «j» b   → (a | b | ajb)
"""

V1_DESCRIPTION = """
  Encoder format v1 begins with optional authors, followed by optional
  title and subtitle, followed by optional attributes.

  Authors are separated by ‘; ’ and followed by a ‘:’.

  Titles and subtitles are separated by ‘: ’.

  Attributes are surrounded by ‘[ … ]’ and separated by ‘,’.

  This is supported only to covert old file names; it should not be used
  due to the ambiguity between authors and titles with subtitles.
""" + V1_GRAMMAR

V1_CONFIG = V3Config(
    escape.unixfile, attr_start='[', attr_end=']', attr_join=',')

def v1_encode(n: VljuMap, mode: str | None = None) -> str:
    m = n.to_strings(mode)
    r = _v1_enc_author_title(m)
    attrs = ','.join(
        kv_fmt(k, v, '=', escape.unixfile)
        for k, v in m.pairs()
        if k not in ('title', 'a'))
    return spj(r, f'[{attrs}]') if attrs else r

def v1_decode(n: VljuMap, s: str, factory: VljuFactory) -> VljuMap:
    return n.add_pairs(_v1_dec_iter(V1_CONFIG, s), factory)

v1 = _register_encoder(
    Encoder(
        'v1', v1_encode, v1_decode, desc=V1_DESC, description=V1_DESCRIPTION))

def _v1_enc_author_title(m: MultiMap) -> str:
    author = '; '.join(i for i in m['a'])
    r = f'{author}:' if author else ''
    title = ': '.join(i for i in m['title'])
    return spj(r, title)

def _v1_dec_iter(config: V3Config, s: str) -> Iterable[tuple[str, str]]:
    if '[' in s:
        s, a = s.split('[', 1)
    else:
        a = ''
    for k, v in _v1_dec_author_title(s):
        yield (k, v)
    if a:
        for k, v in _v3_dec_attr(config, a):
            yield (k, v)

def _v1_dec_author_title(s: str) -> Generator[tuple[str, str], None, None]:
    if ':' in s:
        author, s = s.split(':', 1)
        for i in author.split(';'):
            yield ('a', escape.winfile.decode(i.strip()))
    for i in s.split(':'):
        if i:
            yield ('title', escape.winfile.decode(i.strip()))

###############################################################################
#
# V0 Encoder
#
###############################################################################

V0_DESC = 'The most obsolete encoder.'

V0_GRAMMAR = """
    v0        → v1author «‘ ’» v1title «‘ ’» (isbn | ‘lccn=’ lccn)
    a «j» b   → (a | b | ajb)
"""

V0_DESCRIPTION = """
  Encoder format v0 is strictly limited in the attributes it can represent.
  This is supported only to convert old file names.
""" + V0_GRAMMAR

def v0_encode(n: VljuMap, mode: str | None = None) -> str:
    m = n.to_strings(mode)
    r = _v1_enc_author_title(m)
    if 'isbn' in m:
        return spj(r, m['isbn'][0])
    if 'lccn' in m:
        return spj(r, f'lccn={m["lccn"][0]}')
    return r

def v0_decode(n: VljuMap, s: str, factory: VljuFactory) -> VljuMap:
    return n.add_pairs(_v0_dec_iter(s), factory)

v0 = _register_encoder(
    Encoder(
        'v0', v0_encode, v0_decode, desc=V0_DESC, description=V0_DESCRIPTION))

V0_RE = re.compile(
    r"""
        (?P<rest>.*)
        \b(?:
            (?P<isbn> (?: [0-9]{13} | [0-9]{9}[0-9xX] ) )
        | lccn=(?P<lccn> \S+ )
        )$
        """, re.VERBOSE)

def _v0_dec_iter(s: str) -> Generator[tuple[str, str], None, None]:
    if m := V0_RE.fullmatch(s):
        s = m.group('rest')
    yield from _v1_dec_author_title(s)
    if m:
        if isbn := m.group('isbn'):
            yield ('isbn', isbn)
        elif lccn := m.group('lccn'):   # pragma: no branch
            yield ('lccn', lccn)
        else:                           # pragma: no cover
            message = f'no isbn or lccn in {s}'
            raise Error(message)

###############################################################################
#
# SFC Encoder
#
###############################################################################

SFC_DESC = "SFC's encoder."

SFC_GRAMMAR = """
    sfc       → sfctitle [‘ by ’ sfcauthor] [«‘ ’» (isbn | date | sfced)]*
    sfctitle  → [title [‘ - ’ title]*]
    sfcauthor → author [‘, ’ author]*
    sfced     → edition (‘st’ | ‘nd’ | ‘rd’ | ‘th’) ‘ edition’
    a «j» b   → (a | b | ajb)
"""

SFC_DESCRIPTION = """
  Encoder format sfc consists of a title and optional subtitles, optional
  authors, and optional specific attributes: ISBN, year, and edition.

  Title and optional subtitles are separated by ‘ - ’ (including the spaces).

  Authors are preceded by ‘ by ’ and separated by commas.

  An ISBN may follow. A four-digit year may follow. An edition, consisting
  of a number, a number suffix, and the word ‘edition’, may follow.
""" + SFC_GRAMMAR

def sfc_encode(n: VljuMap, mode: str | None = None) -> str:
    m = n.to_strings(mode)
    title = ' - '.join(i for i in m['title'])
    author = ', '.join(i for i in m['a'])
    if author:
        author = f'by {author}'
    isbn = m['isbn'][0] if 'isbn' in m else ''
    if 'edition' in m:
        e = int(m['edition'][0])
        edition = f'{e}{nth(e)} edition'
    else:
        edition = ''
    date = m['date'][0] if 'date' in m else ''
    return join_non_empty(' ', title, author, isbn, edition, date)

def sfc_decode(n: VljuMap, s: str, factory: VljuFactory) -> VljuMap:
    return n.add_pairs(_sfc_dec_iter(s), factory)

sfc = _register_encoder(
    Encoder(
        'sfc',
        sfc_encode,
        sfc_decode,
        desc=SFC_DESC,
        description=SFC_DESCRIPTION))

SFC_TAIL_RE = re.compile(
    r"""
        (?P<prefix> .*)
        (?:
            (?P<date> [12]\d\d\d ) |
            (?: (?P<edition> \d+ ) \w*\s+edition )
        )$
        """, re.X)

def _sfc_dec_iter(s: str) -> Generator[tuple[str, str], None, None]:
    while True:
        if m := SFC_TAIL_RE.fullmatch(s):
            for k in ('date', 'edition'):
                if v := m.group(k):
                    yield (k, v)
            s = m.group('prefix').strip()
        elif is_valid_isbn10(s[-10 :]):
            yield ('isbn', s[-10 :])
            s = s[:-10].strip()
        elif is_valid_isbn13(s[-13 :]):
            yield ('isbn', s[-13 :])
            s = s[:-13].strip()
        else:
            break
    if (by := s.rfind(' by ')) > 0:
        authors = s[by + 4 :]
    elif s.startswith('by '):
        authors = s[3 :]
        by = 0
    else:
        authors = None
    if authors:
        s = s[: by].strip()
        a = list(map(str.strip, authors.split(',')))
        while a:
            if len(a) > 1 and ' ' not in a[0] and ' ' not in a[1]:
                yield ('a', f'{a[0]}, {a[1]}')
                a = a[2 :]
            else:
                yield ('a', a[0])
                a = a[1 :]
    if s:
        for i in s.split(' - ', 1):
            yield ('title', escape.winfile.decode(i.strip()))

###############################################################################
#
# JSON
#
###############################################################################

JSON_DESC = 'Javascript Object Notation'

JSON_DESCRIPTION = """
  Attributes are encoded in JSON, as an object where each key contains a list
  of values.
"""

def json_encode(n: VljuMap, mode: str | None = None) -> str:
    return py_json.dumps(dict(n.get_lists(mode)))

def json_decode(n: VljuMap, s: str, factory: VljuFactory) -> VljuMap:
    return n.add_pairs(_json_dec_iter(s), factory)

def _json_dec_iter(s: str) -> Generator[tuple[str, str], None, None]:
    for k, vl in py_json.loads(s).items():
        if isinstance(vl, list):
            for v in vl:
                yield (k, str(v))
        else:
            yield (k, str(vl))

json = _register_encoder(
    Encoder(
        'json',
        json_encode,
        json_decode,
        desc=JSON_DESC,
        description=JSON_DESCRIPTION))

###############################################################################
#
# Shell
#
###############################################################################

SHELL_DESC = 'Shell arrays'

SHELL_DESCRIPTION = """
  Attributes are encoded as shell arrays (ksh, bash).
  Decoding is not implemented.
"""

def shell_encode(n: VljuMap, mode: str | None = None) -> str:
    r = []
    for k, vlist in n.get_lists(mode):
        v = ' '.join(shlex.quote(v) for v in vlist if v is not None)
        r.append(f'{k}=({v})')
    return '\n'.join(r)

sh = _register_encoder(
    Encoder(
        'sh',
        shell_encode,
        _unimplemented_decode,
        desc=SHELL_DESC,
        description=SHELL_DESCRIPTION))

###############################################################################
#
# value
#
###############################################################################

VALUE_DESC = 'Bare values'

VALUE_DESCRIPTION = """
  Attributes are presented as raw strings, one per line.
  Since keys are not represented, decoding is not possible.
"""

def value_encode(n: VljuMap, mode: str | None = None) -> str:
    return '\n'.join((f'{v or k}' for k, v in n.get_pairs(mode)))

value = _register_encoder(
    Encoder(
        'value',
        value_encode,
        _unimplemented_decode,
        desc=VALUE_DESC,
        description=VALUE_DESCRIPTION))

###############################################################################
#
# key/value
#
###############################################################################

KEYVALUE_DESC = 'Key:Value pairs'

KEYVALUE_DESCRIPTION = """
  Attributes are presented as a key, followed by ‘: ’, follow by a value.
  Each attribute (including multiple attributes for the same key) appears
  on its own line.
"""

def keyvalue_encode(n: VljuMap, mode: str | None = None) -> str:
    return '\n'.join((f'{k}: {v}' for k, v in n.get_pairs(mode)))

def keyvalue_decode(n: VljuMap, s: str, factory: VljuFactory) -> VljuMap:
    return n.add_pairs(_keyvalue_dec_iter(s), factory)

def _keyvalue_dec_iter(s: str) -> Generator[tuple[str, str], None, None]:
    for kv in s.split('\n'):
        if kv:
            k, v = kv.split(':', 1)
            yield (k.strip(), v.strip())

keyvalue = _register_encoder(
    Encoder(
        'keyvalue',
        keyvalue_encode,
        keyvalue_decode,
        desc=KEYVALUE_DESC,
        description=KEYVALUE_DESCRIPTION))

###############################################################################
#
# csv
#
###############################################################################

CSV_DESC = 'Comma-separated values'

CSV_DESCRIPTION = """
  Attributes are presented as a CSV table of two columns, the first being
  the key and the second the associated value.
"""

def csv_encode(n: VljuMap, mode: str | None = None) -> str:
    return _csv_enc(n, mode, dialect='unix')

def csv_decode(n: VljuMap, s: str, factory: VljuFactory) -> VljuMap:
    return n.add_pairs(_csv_dec_iter(s, dialect='unix'), factory)

csv = _register_encoder(
    Encoder(
        'csv',
        csv_encode,
        csv_decode,
        desc=CSV_DESC,
        description=CSV_DESCRIPTION))

def _csv_enc(n: VljuMap, mode: str | None, **kwargs) -> str:
    with io.StringIO() as f:
        w = py_csv.writer(f, **kwargs)
        for kv in n.get_pairs(mode):
            w.writerow(kv)
        return f.getvalue()

def _csv_dec_iter(s: str, **kwargs) -> Generator[tuple[str, str], None, None]:
    for row in py_csv.reader(s.split('\n'), **kwargs):
        if row:
            k, v = row
            yield (k, v)

###############################################################################
#
# Utility functions
#
###############################################################################

def kv_fmt(k: str, v: str | None, sep: str, e: escape.Escape) -> str:
    if v:
        return f'{k}{sep}{e.encode(v)}'
    return k

def join_non_empty(sep: str, *args: str) -> str:
    """Join non-empty args with the given separator."""
    return sep.join(filter(bool, args))

def spj(s: str, t: str) -> str:
    return join_non_empty(' ', s, t)

def nth(n: int | str) -> str:
    """Return English suffix for ordinal numbers."""
    n = int(n)
    return ('th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th')[n % 10]
