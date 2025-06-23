import streamlit as st
from youtube_utils import fetch_all_comments
from huggingface_utils import analyze_comments
from voice_utils import generate_voice_feedback

st.set_page_config(page_title="Perf Coach")
st.title("🎤 Perf Coach")

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
            
            # 🧠 Get feedback
            summary, suggestions = analyze_comments(events)

            st.subheader("📈 Text Feedback")
            st.markdown(summary)
            st.markdown("**Suggestions for Performer:**")
            for s in suggestions:
                st.write(f"- {s}")

            # 🔊 Voice Feedback Button (generate & store in session_state)
            st.subheader("🔊 Voice Feedback")
            if st.button("▶️ Play Voice Summary"):
                with st.spinner("Generating voice feedback…"):
                    audio = generate_voice_feedback(summary)
                    if audio:
                        st.session_state["voice_feedback"] = audio
                    else:
                        st.error("Voice generation failed.")

# Always try to play audio if it exists in session
if "voice_feedback" in st.session_state:
    st.audio(st.session_state["voice_feedback"], format="audio/mp3")
