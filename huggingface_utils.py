import requests
import streamlit as st

HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}


def analyze_comments(events):
    comments_text = "\n".join(e["text"] for e in events[:20])

    prompt = (
        "You're a concert performance coach. Based on these comments:\n"
        f"{comments_text}\n\n"
        "Summarize audience feedback and give friendly coaching advice."
    )

    show_debug = st.sidebar.checkbox("🛠 Show debug output")

    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt}, timeout=60)

        if show_debug:
            st.sidebar.subheader("📤 Prompt")
            st.sidebar.code(prompt)
            st.sidebar.subheader("📥 Raw Response")
            st.sidebar.text(response.text)

        if response.status_code != 200:
            st.warning(f"Error {response.status_code}: {response.text}")
            return "No summary.", "No coach feedback."

        result = response.json()
        text = result[0]["generated_text"]
        summary, _, coaching = text.partition("\n\n")

        return summary.strip(), coaching.strip()

    except Exception as e:
        st.error("API failure.")
        if show_debug:
            st.sidebar.exception(e)
        return "Failed.", "Unavailable."
