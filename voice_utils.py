from elevenlabs import generate, set_api_key
import streamlit as st

def generate_voice_feedback(text: str, voice: str = "Bella") -> bytes:
    """
    Generate voice audio using ElevenLabs for a given text.
    Returns MP3 bytes, or None if something fails.
    """
    try:
        set_api_key(st.secrets["ELEVENLABS_API_KEY"])
        audio = generate(
            text=text,
            voice=voice,
            model="eleven_monolingual_v1"
        )
        return audio
    except Exception as e:
        st.warning(f"Voice feedback failed: {e}")
        return None
