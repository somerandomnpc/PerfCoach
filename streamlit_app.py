import streamlit as st
from youtube_utils import fetch_all_comments
from huggingface_utils import analyze_comments
from voice_utils import generate_voice_feedback

st.set_page_config(page_title="Perf Coach")
st.title("🎤 Perf Coach")

# Input field
url = st.text_input("Paste a YouTube Video URL")

# State: voice playback toggle and memory
if "voice_feedback" not in st.session_state:
    st.session_state.voice_feedback = None

# Analyze button logic
if st.button("Analyze"):
    if not url.strip():
        st.error("Please enter a valid YouTube link.")
    else:
        st.info("Fetching comments…")
        events = fetch_all_comments(url)

        if not events:
            st.error("No comments found.")
        else:
            st.success(f"Fetched {len(events)} comments.")

            # Analyze comments
            summary, suggestions = analyze_comments(events)

            st.subheader("📈 Text Feedback")
            st.markdown(summary)
            st.markdown("**Suggestions:**")
            for s in suggestions:
                st.write(f"- {s}")

            # Optional: clear voice feedback so we generate fresh audio
            st.session_state.voice_feedback = None

            # Show voice button below feedback
            if st.button("▶️ Play Voice Summary"):
                with st.spinner("Generating voice summary..."):
                    audio = generate_voice_feedback(summary)
                    if audio:
                        st.session_state.voice_feedback = audio
                    else:
                        st.error("Voice generation failed.")

# Play voice feedback if it exists (after button click)
if st.session_state.voice_feedback:
    st.subheader("🔊 Audio Summary")
    st.audio(st.session_state.voice_feedback, format="audio/mp3")
