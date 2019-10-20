import datetime as dt

from googleapiclient.discovery import build


class GoogleCalendar:
    """

    """
    def __init__(self, credentials):
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_events(self, start_date=None, end_date=None, calendar_id='primary'):
        """
        Get events from calendar API.

        :param start_date: lower bound (exclusive) for an event's end time to filter by
        :type start_date: str
        :param end_date: upper bound (exclusive) for an event's start time to filter by
        :type end_date: str
        :param calendar_id: calendar identifier; defaults to 'primary'
        :type calendar_id: str
        :return: list of events (dictionaries)
        """
        start_date, end_date = _get_valid_dates(start_date, end_date)

        events = []
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

    def delete_event(self, event_id, calendar_id='primary', notify=None):
        """
        Delete an event from calendar API.

        :param event_id: event identifier
        :type event_id: str
        :param calendar_id: calendar identifier; defaults to 'primary'
        :type calendar_id: str
        :type notify: send notifications of deletion. Possible values: 'all', 'externalOnly'.
        :type calendar_id: str
        :return: list of events (dictionaries)
        """

        self.service.events().delete(
            calendarId=calendar_id,
            eventId=event_id,
            sendUpdates=notify
        ).execute()

        return True


def _get_valid_dates(start_date, end_date):
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
