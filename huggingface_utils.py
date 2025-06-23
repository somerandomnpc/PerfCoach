import requests
import streamlit as st

# Hugging Face API setup
HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}


def analyze_comments(events):
    """
    Summarizes YouTube comments using Hugging Face summarization model.
    Returns: summary (str), suggestions (list of str)
    """
    comments_text = "\n".join(e["text"] for e in events[:50])
    payload = {"inputs": comments_text}

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        result = response.json()

        if "error" in result:
            st.error("🤖 Hugging Face API error:")
            st.code(result["error"])
            return "No summary available.", []

        summary = result[0]["summary_text"]

        # Generic suggestions (static for now)
        suggestions = [
            "Add more variety in visual or vocal delivery.",
            "React to moments when fans get more active.",
            "Try creating a highlight moment in the middle section."
        ]

        return summary, suggestions

    except Exception as e:
        st.error("⚠️ Hugging Face API request failed.")
        st.exception(e)
        return "No summary generated.", []
