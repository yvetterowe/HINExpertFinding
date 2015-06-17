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
        ):
        self.doc_id = doc_id
        self.phrases = phrases  # phrase count dict
        self.authors = authors  # author id list
        self.venue = venue  # venue id
