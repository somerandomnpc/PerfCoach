import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def analyze_comments(events):
    comments = "\n".join(f"{e['timestamp']}: {e['text']}" for e in events[:100])
    prompt = (
        "These are timestamped audience comments:\n"
        f"{comments}\n"
        "Provide a concise summary and 3 actionable suggestions for the performer."
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    content = resp.choices[0].message.content
    lines = [l.strip() for l in content.split("\n") if l.strip()]
    summary = lines[0] if lines else ""
    suggestions = [l.strip("- ") for l in lines[1:4]]
    return summary, suggestions
