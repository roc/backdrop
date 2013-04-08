from unittest import TestCase
import datetime
from hamcrest import assert_that, is_, contains
from backdrop.core.timeseries import week_start, week_end, timeseries, WEEK
from tests.support.test_helpers import d, d_tz


class TestTimeseries(TestCase):
    def test_returns_a_full_timeseries(self):
        ts = timeseries(start=d_tz(2013, 4, 1),
                        end=d_tz(2013, 4, 15),
                        period=WEEK,
                        data=[],
                        default={"value": 0})

        assert_that(ts, contains(
            {"_start_at": d_tz(2013, 4, 1), "_end_at": d_tz(2013, 4, 8), "value": 0},
            {"_start_at": d_tz(2013, 4, 8), "_end_at": d_tz(2013, 4, 15), "value": 0},
        ))

    def test_adds_data_at_appropriate_places(self):
        data = [
            {"_start_at": d_tz(2013, 4, 1), "_end_at": d_tz(2013, 4, 8), "value": 12}
        ]

        ts = timeseries(start=d_tz(2013, 4, 1),
                        end=d_tz(2013, 4, 15),
                        period=WEEK,
                        data=data,
                        default={"value": 0})

        assert_that(ts, contains(
            {"_start_at": d_tz(2013, 4, 1), "_end_at": d_tz(2013, 4, 8), "value": 12},
            {"_start_at": d_tz(2013, 4, 8), "_end_at": d_tz(2013, 4, 15), "value": 0},
        ))

    def test_start_and_end_are_expanded_to_week_limits(self):
        data = [
            {"_start_at": d_tz(2013, 4, 8), "_end_at": d_tz(2013, 4, 15), "value": 12},
            {"_start_at": d_tz(2013, 4, 15), "_end_at": d_tz(2013, 4, 22), "value": 23}
        ]

        ts = timeseries(start=d_tz(2013, 4, 5),
                        end=d_tz(2013, 4, 25),
                        period=WEEK,
                        data=data,
                        default={"value": 0})

        assert_that(ts, contains(
            {"_start_at": d_tz(2013, 4, 1), "_end_at": d_tz(2013, 4, 8), "value": 0},
            {"_start_at": d_tz(2013, 4, 8), "_end_at": d_tz(2013, 4, 15), "value": 12},
            {"_start_at": d_tz(2013, 4, 15), "_end_at": d_tz(2013, 4, 22), "value": 23},
            {"_start_at": d_tz(2013, 4, 22), "_end_at": d_tz(2013, 4, 29), "value": 0},
        ))


class TestWeek_start(TestCase):
    def test_that_it_returns_previous_monday_for_midweek(self):
        tuesday = datetime.datetime(2013, 4, 9)

        start = week_start(tuesday)

        assert_that(start, is_(datetime.datetime(2013, 4, 8)))

    def test_that_it_truncates_the_time_part(self):
        tuesday = datetime.datetime(2013, 4, 9, 23, 12)

        start = week_start(tuesday)

        assert_that(start, is_(datetime.datetime(2013, 4, 8)))

    def test_that_it_returns_the_same_day_for_monday(self):
        monday = datetime.datetime(2013, 4, 8, 23, 12)

        start = week_start(monday)

        assert_that(start, is_(datetime.datetime(2013, 4, 8)))

    def test_that_it_returns_the_same_day_for_monday_midnight(self):
        monday = datetime.datetime(2013, 4, 8, 0, 0)

        start = week_start(monday)

        assert_that(start, is_(datetime.datetime(2013, 4, 8)))


class TestWeek_end(TestCase):
    def test_that_it_returns_next_monday_for_midweek(self):
        tuesday = datetime.datetime(2013, 4, 9)

        end = week_end(tuesday)

        assert_that(end, is_(datetime.datetime(2013, 4, 15)))

    def test_that_it_truncates_the_time_part(self):
        tuesday = datetime.datetime(2013, 4, 9, 23, 12)

        end = week_end(tuesday)

        assert_that(end, is_(datetime.datetime(2013, 4, 15)))

    def test_that_it_returns_the_same_day_for_monday_midnight(self):
        monday = datetime.datetime(2013, 4, 8, 0, 0)

        end = week_end(monday)

        assert_that(end, is_(datetime.datetime(2013, 4, 8)))

    def test_that_it_returns_the_next_monday_for_monday_after_midnight(self):
        monday = datetime.datetime(2013, 4, 8, 23, 12)

        end = week_end(monday)

        assert_that(end, is_(datetime.datetime(2013, 4, 15)))
