import streamlit as st

def generate_voice_feedback(text: str) -> bytes:
    try:
        from elevenlabs import generate, set_api_key
        set_api_key(st.secrets["ELEVENLABS_API_KEY"])
        audio = generate(text=text, voice="Bella", model="eleven_monolingual_v1")
        return audio
    except:
        return text.encode("utf-8")
