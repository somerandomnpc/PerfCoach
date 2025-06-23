import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_comments(events):
    comments = "\n".join(f"{e.get('timestamp', 0)}: {e['text']}" for e in events[:100])
    prompt = (
        "These are YouTube comments from a concert performance:\n"
        f"{comments}\n\n"
        "Summarize the audience's reactions and give 3 clear, helpful suggestions for the performer."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a performance coach for virtual artists."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content
    lines = content.strip().split("\n")
    summary = lines[0] if lines else ""
    suggestions = [line.strip("-• ") for line in lines[1:] if line.strip()]
    return summary, suggestions

