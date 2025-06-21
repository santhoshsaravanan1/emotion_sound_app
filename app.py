import os
import streamlit as st
import freesound   # from freesound-api

# Initialize client
FS_CLIENT = freesound.FreesoundClient()
API_KEY = "bnvLHj0a3oBdWCUyfY61Rds7SINt4cntex3UBI5n"
if not API_KEY:
    st.error("Please set FREESOUND_API_KEY env var")
    st.stop()
FS_CLIENT.set_token(API_KEY, "token")

st.title("🎧 Emotion‑Based Sound Player")
st.write("Enter an emotion (e.g. “happy”, “sad”, “calm”) to find a matching sound.")

emotion = st.text_input("Emotion", placeholder="happy")

def play_looping_audio(url: str):
    html = f """
    <audio autoplay loop>
      <source src="{url}" type="audio/mp3">
      Your browser does not support the audio element.
    </audio>"""
    st.markdown(html, unsafe_allow_html=True)

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
            preview_url = getattr(sound.previews, 'preview_hq_mp3', None) or getattr(sound.previews, 'preview_lq_mp3', None)
            if preview_url:
                st.subheader(f"🎵 {sound.name}  — by {sound.username}")
                play_looping_audio(preview_url)
            else:
                st.error("No preview available for this sound.")
