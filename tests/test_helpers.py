import datetime as dt

import pytest

from pycal.service.google_calendar import _get_valid_dates


def test_get_valid_dates():
    start_date, end_date = _get_valid_dates('2019-10-11', '2019-10-12')

    assert end_date == dt.datetime(2019, 10, 12).astimezone().isoformat()
    assert start_date == dt.datetime(2019, 10, 11).astimezone().isoformat()


def test_get_valid_dates_with_none():
    start_date, end_date = _get_valid_dates('2019-10-11', None)

    assert end_date is None
    assert start_date == dt.datetime(2019, 10, 11).astimezone().isoformat()


def test_get_valid_dates_raises_value_error_on_end_after_start():
    with pytest.raises(ValueError):
        _get_valid_dates('2019-10-11', '2019-10-08')
