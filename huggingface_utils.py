import requests
import streamlit as st

# Hugging Face config
HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"  # Faster model
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}


def analyze_comments(events):
    """
    Summarizes YouTube comments using Hugging Face's distilBART model.
    Returns: summary string, suggestions list.
    """
    # Limit input text to reduce size
    comments_text = "\n".join(e["text"] for e in events[:20])
    payload = {"inputs": comments_text}

    with st.spinner("Generating feedback… please wait up to 60 seconds."):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
            result = response.json()

            if "error" in result:
                st.error("🤖 Hugging Face API error:")
                st.code(result["error"])
                return "No summary available.", []

            summary = result[0]["summary_text"]

            # Generic suggestions for now
            suggestions = [
                "Use stronger build-ups before key moments.",
                "Add expressive visuals to increase crowd engagement.",
                "Introduce variation between chorus and verse patterns."
            ]
            return summary, suggestions

        except requests.exceptions.ReadTimeout:
            st.error("⚠️ Request timed out. Try again with fewer comments or retry later.")
            return "Timeout error", []

        except Exception as e:
            st.error("🚫 Unexpected error during feedback generation.")
            st.exception(e)
            return "Error", []
