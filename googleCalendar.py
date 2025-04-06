import os
import json
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import timezone
from datetime import timedelta


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials, run the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Calendar API client
    service = build('calendar', 'v3', credentials=creds)

    # Fetch events from now onward
    now = datetime.now(timezone.utc)
    time_min = (now - timedelta(days=365)).isoformat() #change date range
    time_max = (now + timedelta(days=365)).isoformat() #change date range
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        maxResults=250,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    print(f"Found {len(events)} upcoming events.\n")

    # Build clean event list
    all_events = []

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        all_events.append({
            'summary': event.get('summary', 'No Title'),
            'start': start,
            'end': end,
            'location': event.get('location', 'N/A'),
            'description': event.get('description', 'N/A')
        })

    print(json.dumps(all_events, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
