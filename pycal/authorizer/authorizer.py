import json

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class GoogleAuthorizer:
    """

    """
    def __init__(self, credentials_path, config_path):
        self.credentials_path = credentials_path
        self.config_path = config_path
        self._credentials = None

    @property
    def credentials(self):
        """
        Get refreshed auth token.

        :return: Google auth token
        """
        if self._credentials is None:
            try:
                self._credentials = Credentials.from_authorized_user_file(self.credentials_path)

            except FileNotFoundError:
                self._credentials = self.run_installed_app_flow()
                self.save_credentials()

        self.refresh_credentials()

        return self._credentials

    def run_installed_app_flow(self):
        """
        Opens local browser with login prompt to authorize application

        :return: Google credentials for r/w calendar scope
        """
        scopes = ['https://www.googleapis.com/auth/calendar']
        flow = InstalledAppFlow.from_client_secrets_file(self.config_path, scopes)
        credentials = flow.run_local_server(port=0)

        return credentials

    def save_credentials(self):
        credentials_dict = {
            'client_id': self._credentials.client_id,
            'client_secret': self._credentials.client_secret,
            'refresh_token': self._credentials.refresh_token
        }

        with open(self.credentials_path, 'w') as credentials_file:
            json.dump(credentials_dict, credentials_file)

    def refresh_credentials(self):
        if self._credentials and self._credentials.expired and self._credentials.refresh_token:
            self._credentials.refresh(Request())
