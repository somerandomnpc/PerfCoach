import streamlit as st
from elevenlabs.client import ElevenLabs
from io import BytesIO

def generate_voice_feedback(text: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL") -> bytes:
    """
    Generate spoken audio from ElevenLabs and return as MP3 bytes.
    Uses default voice_id unless overridden.
    """
    try:
        client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            model_id="eleven_monolingual_v1",
            text=text
        )
        return BytesIO(audio).read()

    except Exception as e:
        st.error(f"Voice generation failed: {e}")
        return
