import streamlit as st
from openai import OpenAI, RateLimitError
import requests

openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY")
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def analyze_comments(events):
    comments = "\n".join(e["text"] for e in events[:50])
    prompt = (
        "These are YouTube comments from a concert performance:\n"
        f"{comments}\n\n"
        "Summarize the audience's reactions and give 3 clear suggestions for the performer."
    )

    # Try OpenAI first
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a performance coach for virtual concerts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        content = response.choices[0].message.content
        lines = content.strip().split("\n")
        summary = lines[0]
        suggestions = [line.strip("-• ") for line in lines[1:] if line.strip()]
        return summary, suggestions

    except RateLimitError:
        st.warning("⚠️ OpenAI rate limit hit. Using fallback model instead…")

    except Exception as e:
        st.warning(f"⚠️ OpenAI failed: {e}. Trying fallback…")

    # Fallback to Hugging Face
    try:
        payload = {"inputs": comments}
        res = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=30)
        result = res.json()

        if "error" in result:
            return f"HF error: {result['error']}", []

        summary = result[0]["summary_text"]
        fallback_suggestions = [
            "Add more energy during mid-performance dips.",
            "Use visuals or crowd calls to engage more.",
            "Highlight the strongest chorus section next time."
        ]
        return summary, fallback_suggestions

    except Exception as e:
        return f"🚫 All models failed: {e}", []
