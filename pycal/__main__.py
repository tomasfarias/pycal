import argparse
import datetime as dt
import os

from pycal.service import GoogleCalendar
from pycal.authorizer import GoogleAuthorizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs=1, help='')
    parser.add_argument('--output', '-o', default='json', help='')

    default_start = dt.datetime.today().astimezone()
    default_end = default_start + dt.timedelta(days=1)
    parser.add_argument('--start', '-s', default=default_start.isoformat(), help='')
    parser.add_argument('--end', '-e', default=default_end.isoformat(), help='')
    parser.add_argument('--credentials-file', '-t', default=None, help='')
    parser.add_argument('--config-file', '-c', default=None, help='')

    args = parser.parse_args()

    command = args.command[0]

    credentials_file_path = args.credentials_file or os.getenv('GOOGLE_CREDENTIALS_FILE', None)
    if credentials_file_path is None:
        print('Credentials file path not defined.')
        exit(1)

    config_file_path = args.config_file or os.getenv('GOOGLE_CONFIG_FILE', None)
    if not os.path.exists(credentials_file_path) and config_file_path is None:
        print('Need client config file to be defined when token needs to be created.')
        exit(1)

    ga = GoogleAuthorizer(credentials_file_path, config_file_path)
    gc = GoogleCalendar(ga.credentials)

    if command == 'list' or command == 'first':
        events = gc.get_events(args.start, args.end)
        if not events:
            print(f'No events between {args.start} and {args.end}')
            exit(0)

        if command == 'first':
            events = events[0]

        if args.output == 'json':
            print(events)

    else:
        print(f'Invalid command {command}. See --help for a list of available commands.')
        exit(1)


if __name__ == '__main__':
    main()
