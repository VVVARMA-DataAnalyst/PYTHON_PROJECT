import streamlit as st
import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime, webbrowser, os, re

# ---------- safe text-to-speech ----------
def speak(text: str):
    engine = pyttsx3.init()
    engine.setProperty("rate", 180)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# ---------- helpers ----------
def wish_user():
    h = datetime.datetime.now().hour
    if h < 12: return "Good morning!"
    if h < 18: return "Good afternoon!"
    return "Good evening!"

def clean_text(txt: str) -> str:
    """lowercase, remove punctuation and extra spaces"""
    return re.sub(r"[^a-z0-9 ]+", "", txt.lower()).strip()

# ---------- microphone ----------
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as src:
        st.info("🎙️ Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(src)
    try:
        query = r.recognize_google(audio, language="en-in")
        query = clean_text(query)
        st.success(f"🗣️ Heard: {query}")
        return query
    except sr.UnknownValueError:
        st.warning("❌ Didn't catch that.")
    except sr.RequestError:
        st.error("⚠️ Speech service unavailable.")
    return ""

# ---------- command logic ----------
def handle_command(q: str):
    if not q:
        return "Say something again, please."

    if any(k in q for k in ["hello", "hi", "hey"]):
        return "Hello! How can I help you?"

    if "wikipedia" in q or "who is" in q or "what is" in q:
        topic = q.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
        if not topic:
            return "Tell me what to search on Wikipedia."
        try:
            res = wikipedia.summary(topic, sentences=2)
            return f"According to Wikipedia: {res}"
        except Exception:
            return "Couldn't fetch that topic on Wikipedia."

    if "youtube" in q:
        webbrowser.open("https://youtube.com"); return "Opening YouTube."
    if "google" in q:
        webbrowser.open("https://google.com"); return "Opening Google."
    if "github" in q:
        webbrowser.open("https://github.com"); return "Opening GitHub."

    if "time" in q:
        return f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}."

    if "note" in q or "remember" in q:
        note = st.text_input("✏️ Type the note to save:")
        if note:
            with open("notes.txt", "a") as f:
                f.write(f"{datetime.datetime.now()}: {note}\n")
            return "Note saved!"
        return "Waiting for your note above."

    if "show notes" in q or "read notes" in q:
        if os.path.exists("notes.txt"):
            with open("notes.txt") as f: return f"📝 Your notes:\n\n{f.read()}"
        return "No notes yet."

    if any(k in q for k in ["exit", "quit", "goodbye", "stop listening"]):
        st.session_state["listening"] = False
        speak("Goodbye! I’ll stop listening until you press the button again.")
        return "Goodbye! Listening paused."

    return "I didn’t recognize that command."

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Voice Chatbot", page_icon="🎙️", layout="centered")

if "listening" not in st.session_state:
    st.session_state["listening"] = True

st.title("🎙️ Voice-Activated AI Chatbot")
st.info(wish_user())

# sidebar
with st.sidebar:
    st.header("🧾 Notes")
    if os.path.exists("notes.txt"):
        with open("notes.txt") as f: st.text(f.read())
    else:
        st.caption("No notes yet.")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎧 Speak Command"):
        st.session_state["listening"] = True
        q = listen_command()
        if q:
            ans = handle_command(q)
            st.success(ans)
            if st.session_state["listening"]: speak(ans)

with col2:
    text_q = st.text_input("⌨️ Or type a command:")
    if st.button("Submit Text Command"):
        if text_q:
            q = clean_text(text_q)
            ans = handle_command(q)
            st.success(ans)
            if st.session_state["listening"]: speak(ans)

st.caption("Built with Streamlit • SpeechRecognition • pyttsx3 • Wikipedia")
