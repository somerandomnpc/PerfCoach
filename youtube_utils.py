import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_KEY = st.secrets.get("GOOGLE_API_KEY")

def extract_video_id(url: str) -> str:
    import re
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def fetch_all_comments(url: str):
    video_id = extract_video_id(url)
    if not video_id:
        st.error("Invalid YouTube URL.")
        return []

    try:
        service = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        comments = []

        request = service.commentThreads().list(
            videoId=video_id,
            part="snippet",
            maxResults=100,
            textFormat="plainText"
        )

        while request:
            response = request.execute()
            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append({"text": comment, "timestamp": 0})
            request = service.commentThreads().list_next(request, response)

        return comments

    except HttpError as e:
        st.error("YouTube API error.")
        st.exception(e)
        return []

    except Exception as e:
        st.error("Unexpected error occurred.")
        st.exception(e)
        return []
