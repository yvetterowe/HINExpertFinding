#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Hao Luo


class DocMeta(object):
    def __init__(
        self,
        doc_id,
        phrases,
        authors,
        venue,
        citations,
        ):
        self.doc_id = doc_id
        self.phrases = phrases  # bag-of-phrases dict
        self.authors = authors  # author id list - index is order
        self.venue = venue  # venue id
        self.citations  = citations # citation id set
