#
# Gmail sending helper script.
#
# Requirements:
# - google-api-python-client (tested with 1.5.0)
#

import base64
import httplib2
import os
import sys
from email.mime.text import MIMEText

from apiclient import errors
from apiclient import discovery
from oauth2client.client import OAuth2WebServerFlow


def get_service(client_id, client_secret):
    flow = OAuth2WebServerFlow(client_id=client_id,
                           client_secret=client_secret,
                           # we care only about sending emails here
                           scope='https://www.googleapis.com/auth/gmail.send',
                           redirect_uri='urn:ietf:wg:oauth:2.0:oob')
    auth_uri = flow.step1_get_authorize_url()
    # TODO: think about better way of getting the auth token here
    print("Paste following URL into the browser:")
    print(auth_uri)
    code = input('Enter the code it gives you here: ')
    credentials = flow.step2_exchange(code)
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = discovery.build('gmail', 'v1', http=http)
    return service

def send_message(service, message):
    try:
        return service.users().messages().send(userId='me', body=message).execute()
    except errors.HttpError as error:
        print('An error occurred:', error)

def create_message(sender, to, subject):
    message = MIMEText(\
"""
<The email text goes here>
""")
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': str(base64.b64encode(str.encode(message.as_string())), 'ascii')}

if __name__ == '__main__':
    if len(sys.argv) == 0:
        sys.exit("Missing file argument to be parsed for email data to be sent.")
    if "GMAIL_CLIENT_ID" not in os.environ or "GMAIL_CLIENT_SECRET" not in os.environ:
        sys.exit("Missing GMAIL_CLIENT_ID or GMAIL_CLIENT_SECRET environment variables.")

    with open(sys.argv[1]) as file:
        # each line of the file contains single address to send the email to
        service = get_service(os.environ["GMAIL_CLIENT_ID"], os.environ["GMAIL_CLIENT_SECRET"])
        for email in file:
            send_message(service, create_message('<from email goes here>', email,
                "<title goes here>"))

