import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    youtube = build('youtube', 'v3', credentials=creds)

    # Subscriptions
    try:
        subscriptions = []
        next_page = None
        while True:
            subs_response = youtube.subscriptions().list(
                part="snippet",
                mine=True,
                maxResults=50,
                pageToken=next_page
            ).execute()
            subscriptions.extend(subs_response.get('items', []))
            next_page = subs_response.get('nextPageToken')
            if not next_page:
                break

        if subscriptions:
            print(f"\nYou are subscribed to {len(subscriptions)} channels:")
            for sub in subscriptions:
                print(f"- {sub['snippet']['title']}")
    except:
        pass

    # Playlists
    try:
        playlists = []
        next_page = None
        while True:
            pl_response = youtube.playlists().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=50,
                pageToken=next_page
            ).execute()
            playlists.extend(pl_response.get('items', []))
            next_page = pl_response.get('nextPageToken')
            if not next_page:
                break

        if playlists:
            print(f"\nYou have {len(playlists)} playlists:")
            for pl in playlists:
                print(f"- {pl['snippet']['title']} ({pl['contentDetails']['itemCount']} videos)")
    except:
        pass

    # Liked Videos
    try:
        channel_response = youtube.channels().list(
            part="contentDetails",
            mine=True
        ).execute()

        items = channel_response.get('items', [])
        if items:
            likes_playlist_id = items[0]['contentDetails']['relatedPlaylists']['likes']

            likes_response = youtube.playlistItems().list(
                part="snippet",
                playlistId=likes_playlist_id,
                maxResults=10
            ).execute()

            liked_videos = likes_response.get('items', [])
            if liked_videos:
                print(f"\nYour Liked Videos:")
                for video in liked_videos:
                    title = video['snippet']['title']
                    video_id = video['snippet']['resourceId']['videoId']
                    print(f"- {title} (https://www.youtube.com/watch?v={video_id})")
    except:
        pass

if __name__ == '__main__':
    main()
