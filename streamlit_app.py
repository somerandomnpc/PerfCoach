import streamlit as st
from youtube_utils import fetch_all_comments
from huggingface_utils import analyze_comments
from voice_utils import generate_voice_feedback

st.set_page_config(page_title="Perf Coach")
st.title("🎤 Perf Coach")

# 📥 User inputs YouTube video URL
url = st.text_input("Paste a YouTube Video URL")

if st.button("Analyze"):
    if not url.strip():
        st.error("Please enter a valid YouTube link.")
    else:
        st.info("Fetching comments from YouTube…")
        events = fetch_all_comments(url)

        if not events:
            st.error("No comments were fetched from this video.")
        else:
            st.success(f"Fetched {len(events)} comments.")
            
            # 🧠 AI Feedback from Hugging Face
            summary, suggestions = analyze_comments(events)

            st.subheader("📈 Text Feedback")
            st.markdown(summary)
            st.markdown("**Suggestions for Performer:**")
            for s in suggestions:
                st.write(f"- {s}")

            # 🔊 Voice Feedback using ElevenLabs
            st.subheader("🔊 Voice Feedback")
            if st.button("▶️ Play Voice Summary"):
                with st.spinner("Generating voice summary..."):
                    audio = generate_voice_feedback(summary)
                    if audio:
                        st.audio(audio, format="audio/mp3")
                    else:
                        st.error("Voice generation failed.")
