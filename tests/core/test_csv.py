# -*- coding: utf-8 -*-

from StringIO import StringIO
import unittest
from hamcrest import assert_that, only_contains, is_

from backdrop.core.parse_csv import parse_csv
from backdrop.core.errors import ParseError


class ParseCsvTestCase(unittest.TestCase):
    def test_parse_csv(self):
        csv_stream = StringIO("a,b\nx,y\nq,w")

        data = parse_csv(csv_stream)

        assert_that(data,
                    only_contains({"a": "x", "b": "y"}, {"a": "q", "b": "w"}))

    def test_parse_empty_csv(self):
        csv_stream = StringIO("")

        data = parse_csv(csv_stream)

        assert_that(data, is_([]))

    def test_parse_utf8_data(self):
        csv = u"a,b\nà,ù"
        csv_stream = StringIO(csv.encode("utf-8"))

        data = parse_csv(csv_stream)

        assert_that(data, only_contains(
            {"a": u"à", "b": u"ù"}
        ))

    def test_error_when_values_for_columns_are_missing(self):
        incoming_data = StringIO("a,b\nx,y\nq")

        self.assertRaises(ParseError, parse_csv, incoming_data)

    def test_error_when_there_are_more_values_than_columns(self):
        incoming_data = StringIO("a,b\nx,y,s,d\nq,w")

        self.assertRaises(ParseError, parse_csv, incoming_data)

    def test_error_when_input_is_not_utf8(self):
        csv = u"a,b\nà,ù"

        csv_stream = StringIO(csv.encode("iso-8859-1"))

        self.assertRaises(ParseError, parse_csv, csv_stream)

    def test_ignore_when_empty_row(self):
        csv = u"a,b\n,\nc,d"
        csv_stream = StringIO(csv.encode("utf-8"))

        data = parse_csv(csv_stream)

        assert_that(data, only_contains(
            {"a": u"c", "b": u"d"}
        ))

    def test_accept_when_some_values_empty(self):
        csv = u"a,b\n,\nc,d\nc,"
        csv_stream = StringIO(csv.encode("utf-8"))

        data = parse_csv(csv_stream)

        assert_that(data, only_contains(
            {"a": u"c", "b": u"d"},
            {"a": u"c", "b": u""}
        ))

    def test_ignore_comments(self):
        csv = u"# top comment\na,b\n# any random comment\nc,d"
        csv_stream = StringIO(csv.encode("utf-8"))

        data = parse_csv(csv_stream)

        assert_that(data, only_contains(
            {"a": u"c", "b": u"d"}
        ))

    def test_ignore_values_in_comments_column(self):
        csv = u"a,comment,b\nc,d,e"
        csv_stream = StringIO(csv.encode("utf-8"))

        data = parse_csv(csv_stream)

        assert_that(data, only_contains(
            {"a": u"c", "b": u"e"}
        ))
