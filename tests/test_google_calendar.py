import json
from operator import attrgetter
from unittest.mock import MagicMock, patch

import pytest

from pycal.service import GoogleCalendar


@pytest.fixture
def calendar():
    with patch.object(GoogleCalendar, '__init__', lambda _: None):
        calendar = GoogleCalendar()
        calendar.service = MagicMock()

    return calendar


def mock_service_events(calendar, return_value, command):
    get_command = attrgetter(
        f'service.events.return_value.{command}.return_value.execute'
    )

    calendar_command = get_command(calendar)
    calendar_command.return_value = return_value

    return calendar


def test_get_events(calendar):
    with open('tests/assets/events.json') as fp:
        expected = json.load(fp)
    calendar = mock_service_events(calendar, {'items': expected}, 'list')

    result = calendar.get_events(start_date='2019-10-19 20:10:01', end_date='2019-11-19 20:10:01')

    assert result == expected


def test_get_events_empty(calendar):
    calendar = mock_service_events(calendar, {'items': []}, 'list')

    result = calendar.get_events(start_date='2019-10-19 20:10:01', end_date='2019-11-19 20:10:01')

    assert result == []


def test_delete_event(calendar):
    calendar = mock_service_events(calendar, None, 'delete')

    result = calendar.delete_event(event_id='12345')

    assert result is True
