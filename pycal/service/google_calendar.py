import datetime as dt
from typing import Optional, List, Dict, Tuple, Any

from googleapiclient.discovery import build


class GoogleCalendar:
    """Google Calendar API adapter"""
    def __init__(self, credentials):
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_events(
            self, start_date: Optional[str] = None, end_date: Optional[str] = None,
            calendar_id: str = 'primary'
    ) -> List[Optional[dict]]:
        """
        Get events from calendar.

        :param start_date: lower bound (exclusive) for an event's end time to filter by
        :param end_date: upper bound (exclusive) for an event's start time to filter by
        :param calendar_id: calendar identifier; defaults to 'primary'
        :return: list of events (dictionaries)
        """
        start_date, end_date = _get_valid_dates(start_date, end_date)

        events: List[Optional[dict]] = []
        next_page_token = None
        while True:
            next_events = self.service.events().list(
                calendarId=calendar_id,
                timeMin=start_date,
                timeMax=end_date,
                singleEvents=True,
                orderBy='startTime',
                pageToken=next_page_token
            ).execute()

            events += next_events['items']
            next_page_token = next_events.get('nextPageToken', None)

            if next_page_token is None:
                break

        return events

    def delete_event(
            self, event_id: str, calendar_id: str = 'primary', notify: Optional[str] = None
    ) -> bool:
        """
        Delete an event from a calendar.

        :param event_id: event identifier
        :param calendar_id: calendar identifier; defaults to 'primary'
        :type notify: send notifications of deletion. Possible values: 'all', 'externalOnly'.
        :return: list of events (dictionaries)
        """

        self.service.events().delete(
            calendarId=calendar_id,
            eventId=event_id,
            sendUpdates=notify
        ).execute()

        return True

    def insert_event(
            self, body, calendar_id: str = 'primary', notify: Optional[str] = None,
            attachments: bool = False, conference_version: int = 0
    ) -> Dict:
        """
        Insert an event into a calendar.

        :param body: event identifier
        :param calendar_id: calendar identifier; defaults to 'primary'
        :param notify: send notifications of deletion. Possible values: 'all', 'externalOnly'
            or None.
        :param attachments: send notifications of deletion. Possible values: 'all',
            'externalOnly' or None.
        :param conference_version: send notifications of deletion. Possible values: 'all',
            'externalOnly' or None.
        :return: list of events (dictionaries)
        """

        result = self.service.events().insert(
            calendarId=calendar_id,
            body=body,
            sendUpdates=notify,
            supportsAttachments=attachments,
            conferenceDataVersion=conference_version
        ).execute()

        return result


def _get_valid_dates(start_date: Any, end_date: Any) -> Tuple[Optional[str], Optional[str]]:
    """
    Get dates in ISO format. Checks that end_date >= start_date

    :param start_date:
    :param end_date:
    :return:
    :raises: ValueError if end_date < start_date and both dates are not None.
    """
    try:
        start_date = dt.datetime.fromisoformat(start_date).astimezone()
    except TypeError:
        pass

    try:
        end_date = dt.datetime.fromisoformat(end_date).astimezone()
    except TypeError:
        pass

    if end_date is not None and start_date is not None and end_date < start_date:
        raise ValueError(f'End date {end_date} must be after start date {start_date}')

    return (
        start_date.isoformat() if start_date is not None else start_date,
        end_date.isoformat() if end_date is not None else end_date
    )
