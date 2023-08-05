# SPDX-License-Identifier: MIT
"""Kinds of info: URI."""

# https://tools.ietf.org/html/rfc4452

import fnattr.vlju.types.doi
import fnattr.vlju.types.lccn

# fmt: off
KIND = {
    'ark':                  None,
    'arxiv':                None,
    'bibcode':              None,
    'bnf':                  None,
    'ddbj-embl-genbank':    None,
    'dlf':                  None,
    'doi':                  fnattr.vlju.types.doi.DOI,
    'eu-repo':              None,
    'fedora':               None,
    'hdl':                  fnattr.vlju.types.doi.DOI,
    'inchi':                None,
    'lanl-repo':            None,
    'lc':                   None,
    'lccn':                 fnattr.vlju.types.lccn.LCCN,
    'ncid':                 None,
    'netref':               None,
    'nla':                  None,
    'nyu':                  None,
    'oclcnum':              None,
    'ofi':                  None,
    'pmid':                 None,
    'pronom':               None,
    'refseq':               None,
    'rfa':                  None,
    'rlgid':                None,
    'sici':                 None,
    'sid':                  None,
    'srw':                  None,
    'ugent-repo':           None,
}
# fmt: on

# fmt: off
ORGANIZATION = {
    'ark':          'Archival Resource Keys',
    'arxiv':        'arXiv.org identifiers',
    'bibcode':      'Astrophysics Data System bibcodes',
    'bnf':          'Bibliothèque nationale de France',
    'ddbj-embl-genbank':    'DDBJ/EMBL/GenBank',
    'dlf':          'Digital Library Federation',
    'doi':          'Digital Object Identifiers',
    'eu-repo':      'European Repository Systems',
    'fedora':       'Fedora Digital Objects and Disseminations',
    'hdl':          'Handles',
    'inchi':        'IUPAC International Chemical Identifiers (InChI)',
    'lanl-repo':    'LANL Research Library',
    'lc':           'Library of Congress Identifiers',
    'lccn':         'Library of Congress Control Numbers',
    'ncid':         'NACSIS-CAT Identification Numbers',
    'netref':       'NISO Standard for Network Reference Services',
    'nla':          'National Library of Australia',
    'nyu':          'New York University Digital Objects',
    'oclcnum':      'OCLC Worldcat Control Numbers',
    'ofi':          'Registry Identifiers in the NISO OpenURL Framework',
    'pmid':         'PubMed',
    'pronom':       'PRONOM Unique Identifiers',
    'refseq':       'identifiers for RefSeq reference sequence record',
    'rfa':          'Registry Framework Architecture',
    'rlgid':        'RLG Database Record',
    'sici':         'Serial Item and Contribution',
    'sid':          'Source Identifiers in the NISO OpenURL Framework',
    'srw':          'Search/Retrieve Web Services',
    'ugent-repo':   'University Library Ghent',
}
# fmt: on
