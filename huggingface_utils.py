import requests
import streamlit as st

# Hugging Face Inference API
HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}


def analyze_comments(events):
    """
    Analyzes comments and returns:
    - summary: what the audience felt
    - coaching_comment: dynamic, natural coaching feedback
    """
    comments_text = "\n".join(e["text"] for e in events[:20])

    prompt = (
        "You're a virtual performance coach watching a concert. Based on these comments:\n"
        f"{comments_text}\n\n"
        "Summarize the audience’s reaction, then give performance advice in a helpful, coach-like tone. Be specific and encouraging."
    )

    try:
        with st.spinner("Generating feedback…"):
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json={"inputs": prompt},
                timeout=60
            )
            result = response.json()

            if "error" in result:
                return "Audience summary not available.", "Coach feedback unavailable."

            text = result[0]["generated_text"]
            summary, _, coaching_comment = text.partition("\n\n")

            return summary.strip(), coaching_comment.strip()

    except Exception as e:
        st.error("Hugging Face generation failed.")
        st.exception(e)
        return "Error summarizing.", "Error generating coaching comment."
