import re
from googleapiclient.discovery import build
from datetime import timedelta
import streamlit as st

YOUTUBE_API_KEY = st.secrets["GOOGLE_API_KEY"]

def fetch_timestamped_comments(url):
    vid = url.split("v=")[-1].split("&")[0]
    service = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    resp = service.commentThreads().list(videoId=vid, part="snippet", maxResults=100).execute()
    pattern = r"(\d{1,2}:\d{2})"
    events = []
    for item in resp.get("items", []):
        text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        for match in re.findall(pattern, text):
            m, s = map(int, match.split(":"))
            ts = timedelta(minutes=m, seconds=s).total_seconds()
            events.append({"timestamp": ts, "text": text})
    return events
