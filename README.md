# 🎙️ Voice-Activated AI Chatbot using Streamlit

## 📘 Overview
This project is a **Voice-Enabled AI Chatbot** built using **Python** and **Streamlit**.  
It listens to your voice commands, processes them intelligently, performs tasks like searching Wikipedia, opening websites, managing notes, and speaking responses aloud.  
The chatbot also supports text commands for accessibility and has a simple, user-friendly web interface.

---

## 🧩 Features
- 🎧 **Voice Recognition** – Listens to your commands via microphone  
- 🗣️ **Text-to-Speech** – Speaks responses using `pyttsx3`  
- 🔍 **Wikipedia Integration** – Fetches short summaries on any topic  
- 🌐 **Web Automation** – Opens YouTube, Google, or GitHub  
- 🕒 **Tells the Time** – Reads the current time  
- 📝 **Note-Taking** – Saves and displays user notes  
- 👋 **Smart Greeting** – Greets you based on the time of day  
- 📴 **Exit Mode** – Stops listening until manually reactivated  

---



## ⚙️ Installation
  **Install dependencies**
  pip install streamlit speechrecognition pyttsx3 wikipedia pyaudio

 ## CODE EXPALINATION
 **Importing Required Libraries**
 
 import streamlit as st
 
 import speech_recognition as sr
 
 import pyttsx3
 
 import wikipedia
 
 import datetime, webbrowser, os, re

**Explaination:**

streamlit: Builds the interactive web app.

speech_recognition: Converts spoken audio into text.

pyttsx3: Handles text-to-speech conversion.

wikipedia: Fetches brief summaries from Wikipedia.

datetime, webbrowser, os, re: Support modules for utilities, file access, and regex cleanup.

**Safe Text-to-Speech Function**

def speak(text: str):

    engine = pyttsx3.init()
    
    engine.setProperty("rate", 180)
    
    voices = engine.getProperty("voices")
    
    engine.setProperty("voice", voices[0].id)
    
    engine.say(text)
    
    engine.runAndWait()
    
    engine.stop()

**Explaination:**
This function initializes the speech engine, sets the voice speed and tone, and audibly speaks the response. It ensures proper shutdown to prevent memory leaks.



**Greeting Based on Time**

def wish_user():

    h = datetime.datetime.now().hour
    
    if h < 12: return "Good morning!"
    
    if h < 18: return "Good afternoon!"
    
    return "Good evening!"

**Explaination:**
Checks the current system time and returns a suitable greeting (morning, afternoon, or evening).

**Cleaning User Input**

def clean_text(txt: str) -> str:

    """lowercase, remove punctuation and extra spaces"""
    
    return re.sub(r"[^a-z0-9 ]+", "", txt.lower()).strip()

**Explaination:**
Prepares user input by converting to lowercase, removing special characters, and trimming spaces — improving accuracy for command matching.

**Listening to Voice Commands**

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

**Explaination:**
1.Uses the microphone to capture speech input.

2.Converts the voice to text using Google Speech API.

3.Displays the recognized command in the Streamlit UI.

4.Handles network and recognition errors gracefully.

**Processing Commands**

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

**Explaination:**
This is the brain of the chatbot. It checks for keywords in the user’s command and performs the appropriate action:

Greets the user

Searches Wikipedia

Opens websites

Tells the current time

Manages notes

Exits the session
All outputs are displayed and optionally spoken aloud.

**Streamlit User Interface**

st.set_page_config(page_title="Voice Chatbot", page_icon="🎙️", layout="centered")

if "listening" not in st.session_state:

    st.session_state["listening"] = True

st.title("🎙️ Voice-Activated AI Chatbot")

st.info(wish_user())

**Explaination:**
Shows all saved notes in the sidebar for quick access.

**Main Interaction Area**

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

**Explaination:**
Creates two columns — one for voice input and another for text input.
When a button is pressed, it processes the input, displays the response, and speaks it aloud.

**Footer**

st.caption("Built with Streamlit • SpeechRecognition • pyttsx3 • Wikipedia")

**Explaination:**
Displays credits and the technologies used in building the chatbot.


## Run the App

  streamlit run app.py


 ## Technologies Used:
Python 3.x
Streamlit
SpeechRecognition
pyttsx3
Wikipedia API
Regex, Datetime, Webbrowser, OS

## Future Enhancements
Add emotion detection for smarter responses
Integrate ChatGPT for natural conversations
Enable multi-language voice support
Add persistent database for notes
Deploy on Streamlit Cloud



### 1️⃣ Clone this repository
```bash
git clone https://github.com/VVVARMA-DataAnalyst/voice-chatbot.git
cd voice-chatbot


