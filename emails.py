from __future__ import print_function
import os
import base64
import re
import json
from email.utils import parsedate_to_datetime

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
]

def main():
    creds = None
    # 1. Check if we already have a saved token.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # 2. If there are no valid credentials, do the OAuth flow.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # 3. Build the Gmail service.
    service = build('gmail', 'v1', credentials=creds)

    # 4. List all messages in the INBOX.
    all_messages = []
    response = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = response.get('messages', [])

    while True:
        all_messages.extend(messages)
        if 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId='me', labelIds=['INBOX'], pageToken=page_token
            ).execute()
            messages = response.get('messages', [])
        else:
            break

    print(f"Found {len(all_messages)} messages in INBOX.")

    # 5. Retrieve and collect details for each message.
    messages_data = []
    for msg in all_messages:
        full_msg = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = full_msg['payload'].get('headers', [])
        subject = get_header(headers, 'Subject')
        sender = get_header(headers, 'From')
        date_str = get_header(headers, 'Date')
        formatted_date = format_date_to_day_month_year(date_str)
        body_text = get_body(full_msg)

        message_entry = {
            "subject": subject,
            "date": formatted_date,
            "body": body_text,
            "sender": sender
        }
        messages_data.append(message_entry)

    # 6. Print the collected data in JSON format.
    print(json.dumps(messages_data, indent=2))


def get_header(headers, name):
    """Return the value of a header from the headers list."""
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return ""


def format_date_to_day_month_year(date_str):
    """Parse the date string and return it in dd-mm-yyyy format."""
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.strftime("%d-%m-%Y")
    except Exception:
        return date_str


def get_body(message):
    """
    Extract the plain-text body from the message.
    If the payload contains parts, try to find the first 'text/plain' part.
    """
    payload = message.get('payload', {})
    if 'parts' in payload:
        # Look for a part with mimeType 'text/plain'
        for part in payload['parts']:
            if part.get('mimeType') == 'text/plain':
                data = part.get('body', {}).get('data')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8', errors='replace').strip()
    # If no parts or no plain text part, fallback to the body.
    data = payload.get('body', {}).get('data')
    if data:
        return base64.urlsafe_b64decode(data).decode('utf-8', errors='replace').strip()
    return ""

if __name__ == '__main__':
    main()
