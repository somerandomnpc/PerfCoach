import streamlit as st
from youtube_utils import fetch_all_comments
from openai_utils import analyze_comments
from tts_utils import generate_voice_feedback

st.set_page_config(page_title="Perf Coach")
st.title("🎤 Perf Coach")

url = st.text_input("YouTube Video URL")
if st.button("Analyze"):
    if not url.strip():
        st.error("Please enter a valid YouTube URL.")
    else:
        st.info("Fetching comments…")
        events = fetch_all_comments(url)
        if not events:
            st.error("No timestamped comments found.")
        else:
            st.success(f"Found {len(events)} timestamped comments.")

            timestamps = [e["timestamp"] for e in events]
            counts = {ts: timestamps.count(ts) for ts in timestamps}
            st.line_chart(counts)

            st.info("Generating feedback with ChatGPT…")
            summary, suggestions = analyze_comments(events)

            st.subheader("📈 Text Feedback")
            st.markdown(summary)
            for s in suggestions:
                st.write(f"- {s}")

            st.info("Generating voice summary…")
            audio_bytes = generate_voice_feedback(summary)
            st.audio(audio_bytes)
