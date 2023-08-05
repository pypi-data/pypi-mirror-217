# SPDX-License-Identifier: MIT
"""Kinds of URN. Not implemented."""

from fnattr.vlju import Vlju

KIND: dict[str, type[Vlju] | None] = {}

ORGANIZATION: dict[str, str] = {}

# https://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml

# 3gpp                https://www.iana.org/go/rfc5279
# 3gpp2               https://www.iana.org/go/rfc8464
# adid                https://www.iana.org/go/rfc8107
# alert               https://www.iana.org/go/rfc7462
# bbf                 https://www.iana.org/go/rfc8057
# broadband-forum-org https://www.iana.org/go/rfc8057
# cablelabs           https://www.iana.org/go/rfc6289
# ccsds               https://www.iana.org/go/rfc7738
# cgi                 https://www.iana.org/go/rfc5138
# clei                https://www.iana.org/go/rfc4152
# ddi                 https://www.iana.org/go/draft-urn-ddi-00
# dev                 https://www.iana.org/go/rfc9039
# dgiwg               https://www.iana.org/go/rfc6288
# dslforum-org        https://www.iana.org/go/rfc8057
# dvb                 https://www.iana.org/go/rfc7354
# ebu                 https://www.iana.org/go/rfc5174
# eidr                https://www.iana.org/go/rfc7972
# epc                 https://www.iana.org/go/rfc5134
# epcglobal           https://www.iana.org/go/rfc5134
# etsi                https://www.iana.org/go/rfc8515
# eurosystem          https://www.iana.org/go/rfc7207
# example             https://www.iana.org/go/rfc6963
# fdc                 https://www.iana.org/go/rfc4198
# fipa                https://www.iana.org/go/rfc3616
# geant               https://www.iana.org/go/rfc4926
# globus              https://www.iana.org/go/rfc7853
# gsma                https://www.iana.org/go/rfc7254
# hbbtv               https://www.iana.org/go/rfc7528
# ieee                https://www.iana.org/go/rfc8069
# ietf                https://www.iana.org/go/rfc2648
# iptc                https://www.iana.org/go/rfc3937
# isan                https://www.iana.org/go/rfc4246
# isbn                https://www.isbn-international.org
# iso                 https://www.iana.org/go/rfc5141
# issn                http://www.issn.org
# itu                 https://www.itu.int/
# ivis                https://www.iana.org/go/rfc4617
# liberty             https://www.iana.org/go/rfc3622
# mace                https://www.iana.org/go/rfc3613
# mef                 https://www.iana.org/go/rfc7818
# mpeg                https://www.iana.org/go/rfc3614
# mrn                 http://www.iala-aism.org
# nato                https://www.iana.org/go/rfc7467
# nbn                 https://www.iana.org/go/rfc8458
# nena                https://www.iana.org/go/rfc6061
# newsml              https://www.iana.org/go/rfc3085
# nfc                 https://www.iana.org/go/rfc4729
# nzl                 https://www.iana.org/go/rfc4350
# oasis               https://www.iana.org/go/rfc3121
# ogc                 https://www.iana.org/go/rfc5165
# ogf                 https://www.iana.org/go/rfc6453
# oid                 https://www.iana.org/go/rfc3061
# oipf                https://www.iana.org/go/rfc6893
# oma                 https://www.iana.org/go/rfc4358
# onf                 https://www.opennetworking.org/
# pin                 https://www.iana.org/go/rfc3043
# publicid            https://www.iana.org/go/rfc3151
# reso                http://www.iana.org/assignments/urn-formal/reso
# s1000d              https://www.iana.org/go/rfc4688
# schac               https://www.iana.org/go/rfc6338
# service             https://www.iana.org/go/rfc5031
# smpte               https://www.iana.org/go/rfc5119
# swift               https://www.iana.org/go/rfc3615
# tva                 https://www.iana.org/go/rfc4195
# uci                 https://www.iana.org/go/rfc4179
# ucode               http://www.rfc-editor.org/errata_search.php?eid=3189
# uuid                https://www.iana.org/go/rfc4122
# web3d               https://www.iana.org/go/rfc3541
# xmlorg              https://www.iana.org/go/rfc3120
# xmpp                https://www.iana.org/go/rfc4854
