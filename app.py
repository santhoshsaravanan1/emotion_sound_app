import os
import streamlit as st
import freesound   # from freesound-api

# Initialize client
FS_CLIENT = freesound.FreesoundClient()
API_KEY = os.getenv("FREESOUND_API_KEY")
if not API_KEY:
    st.error("Please set FREESOUND_API_KEY env var")
    st.stop()
FS_CLIENT.set_token(API_KEY, "token")

st.title("🎧 Emotion‑Based Sound Player")
st.write("Enter an emotion (e.g. “happy”, “sad”, “calm”) to find a matching sound.")

emotion = st.text_input("Emotion", placeholder="happy")
if st.button("Play Sound") and emotion:
    with st.spinner("Searching Freesound..."):
        try:
            results = FS_CLIENT.text_search(
                query=emotion,
                fields="id,previews,username,name",
                filter="duration:[1.0 TO 10.0]",
                sort="rating_desc",
                page_size=1
            )
        except Exception as e:
            st.error(f"API error: {e}")
            st.stop()

        if results.count == 0:
            st.warning("😞 No sounds found. Try another emotion.")
        else:
            sound = results[0]
            preview_url = sound.previews.get("preview-hq-mp3") or sound.previews.get("preview-lq-mp3")
            st.subheader(f"🎵 {sound.name}  — by {sound.username}")
            st.audio(preview_url, format="audio/mp3")
