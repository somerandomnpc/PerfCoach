import requests
import streamlit as st

HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def analyze_comments(events):
    comments_text = "\n".join(e["text"] for e in events[:20])

    prompt = (
        "You're a virtual performance coach watching a concert. Based on these comments:\n"
        f"{comments_text}\n\n"
        "Summarize the audience’s reaction, then give performance advice in a helpful, coach-like tone. Be specific and encouraging."
    )

    try:
        with st.spinner("Generating feedback…"):
            response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt}, timeout=60)

            if response.status_code != 200:
                st.warning(f"Hugging Face error {response.status_code}: {response.text}")
                return "Audience summary not available.", "Coach feedback unavailable."

            try:
                result = response.json()
                text = result[0]["generated_text"]
                summary, _, coaching_comment = text.partition("\n\n")
                return summary.strip(), coaching_comment.strip()

            except Exception as json_error:
                st.warning("⚠️ Hugging Face model returned an unexpected response.")
                st.exception(json_error)
                return "Summary failed.", "Could not interpret model output."

    except requests.exceptions.RequestException as req_error:
        st.error("❌ Could not reach Hugging Face API.")
        st.exception(req_error)
        return "Connection error.", "Coaching unavailable."
