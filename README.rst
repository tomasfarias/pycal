*****
pycal
*****

CLI tool to interact with Google's Calendar API

Install
#######

Clone the repo and run the installation script:

::

    git clone https://github.com/tomasfarias/pycal
    sh install.sh


Set environment variables with location of credentials and client configuration files (otherwise the credentials file path  argument needs to be passed with every call):

::

    export GOOGLE_CREDENTIALS_FILE=/path/to/credentials.json
    export GOOGLE_CLIENT_CONFIG_FILE=/path/to/client/config.json

Examples
########

Get all events between 2019-10-10 and 2019-10-20:

::

    pycal list --start 2019-10-10 --end 2019-10-20

Get the first event after 2019-10-12 12:00:00:

::

    pycal first --start 2019-10-12 12:00:00
