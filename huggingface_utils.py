import requests
import streamlit as st

HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-common_gen"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}


def analyze_comments(events):
    """
    Sends comments to Hugging Face Inference API
    Returns:
      - summary: brief overall audience feedback
      - coaching_comment: friendly performance advice
    Shows debug info in sidebar if toggled.
    """
    comments_text = "\n".join(e["text"] for e in events[:20])

    prompt = (
        "You're a virtual concert performance coach. Based on these comments:\n"
        f"{comments_text}\n\n"
        "Summarize the audience’s reaction, then give performance advice in a helpful, coach-like tone."
    )

    # Toggle for UI debug
    show_debug = st.sidebar.checkbox("🛠 Show debug output")

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt},
            timeout=60
        )

        if show_debug:
            st.sidebar.subheader("📤 Sent Prompt")
            st.sidebar.code(prompt)

            st.sidebar.subheader("📥 Raw Response")
            st.sidebar.text(response.text)

        if response.status_code != 200:
            st.warning(f"Hugging Face returned {response.status_code}: {response.text}")
            return "Audience summary not available.", "Coach feedback unavailable."

        try:
            result = response.json()

            if show_debug:
                st.sidebar.subheader("🧾 Parsed JSON")
                st.sidebar.json(result)

            text = result[0]["generated_text"]
            summary, _, coaching_comment = text.partition("\n\n")

            return summary.strip(), coaching_comment.strip()

        except Exception as json_error:
            st.warning("⚠️ Hugging Face response could not be parsed.")
            if show_debug:
                st.sidebar.exception(json_error)
            return "Error parsing summary.", "Error parsing coach feedback."

    except requests.exceptions.RequestException as req_error:
        st.error("❌ Could not reach Hugging Face API.")
        if show_debug:
            st.sidebar.exception(req_error)
        return "Connection error.", "Coaching unavailable."
