import streamlit as st
from youtube_utils import fetch_all_comments
from huggingface_utils import analyze_comments
from voice_utils import generate_voice_feedback

st.set_page_config(page_title="Perf Coach", layout="centered")
st.title("🎤 Perf Coach")

# --- Input: YouTube URL ---
url = st.text_input("Paste a YouTube Video URL")

# Init session state
if "voice_feedback" not in st.session_state:
    st.session_state.voice_feedback = None

# --- Fetch and Analyze Comments ---
if st.button("Analyze"):
    if not url.strip():
        st.error("Please enter a valid YouTube link.")
    else:
        st.info("Fetching comments from YouTube…")
        events = fetch_all_comments(url)

        if not events:
            st.error("No comments found or comments are disabled on this video.")
        else:
            st.success(f"Fetched {len(events)} comments.")

            # Get summary + coaching comment
            summary, coaching_comment = analyze_comments(events)

            st.subheader("📈 Audience Summary")
            st.markdown(summary)

            st.subheader("🎤 Coach Feedback")
            st.success(coaching_comment)

            # Optional: clear voice on re-analyze
            st.session_state.voice_feedback = None

            # Voice generation button
            if st.button("▶️ Play Voice Summary"):
                with st.spinner("Generating voice feedback…"):
                    audio = generate_voice_feedback(coaching_comment)
                    if audio:
                        st.session_state.voice_feedback = audio
                    else:
                        st.error("Voice generation failed.")

# --- Audio Playback ---
if st.session_state.voice_feedback:
    st.subheader("🔊 Audio Summary")
    st.audio(st.session_state.voice_feedback, format="audio/mp3")
