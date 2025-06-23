import requests
import streamlit as st

HUGGINGFACE_API_KEY = st.secrets["HUGGINGFACE_API_KEY"]
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def analyze_comments(events):
    comments_text = "\n".join(e["text"] for e in events[:50])
    payload = {"inputs": comments_text}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()

        if "error" in result:
            return "⚠️ Hugging Face API error: " + result["error"], []

        summary = result[0]["summary_text"]
        suggestions = [
            "Include more visual or vocal variations during repetitive segments.",
            "Engage the audience directly if comment volume is low.",
            "Use emotes or reactions where fans tend to spike in comments."
        ]
        return summary, suggestions

    except Exception as e:
        return f"⚠️ Request failed: {e}", []
