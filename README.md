# Vortex_AI (A Virtual Assistant)
🌀 Vortex – Your AI Virtual Assistant

Vortex is an advanced voice-controlled AI assistant built with Python.
It helps you interact with your digital world through voice commands – from solving math problems to controlling your system, fetching weather, news, and even recording your screen or webcam.

**🚀 Features**

✅ Speech Recognition & Voice Output – Talk to Vortex naturally

✅ Smart Introductions – Time-based greetings

✅ Date & Age Handling – Ask about today’s date, weekdays, or calculate age

✅ Application & Website Control – Open apps and favorite websites by voice

✅ Mathematical Solver – Handles arithmetic, square roots, trigonometry, logs, and more

✅ Entertainment – Tells jokes, plays music, controls YouTube searches

✅ Screenshots & Recording – Take screenshots, screen recordings, selfies, and webcam videos

✅ Weather Updates – Get real-time weather info with safety precautions (OpenWeather API)

✅ News Headlines – Fetch top news by topic and country (NewsAPI)

✅ System Control – Shutdown, restart, log off, sleep, and monitor CPU/RAM/Disk usage

✅ Proactive Monitoring – Warns you about high resource usage or low disk space

**🛠️ Tech Stack**

Python 3.9+

Libraries Used:

speech_recognition – voice input

pyttsx3 – text-to-speech

webbrowser, subprocess, os, platform – system & web controls

dateutil.parser – date parsing

sympy – advanced math

pyautogui – screenshots & screen size

opencv-python (cv2) – webcam & screen recording

numpy – image processing

psutil – system monitoring

requests – API requests

num2words – number-to-words conversion

urllib.parse – YouTube query encoding

**⚙️ Setup & Installation**

**Clone this repository**

git clone https://github.com/your-username/vortex-assistant.git
cd vortex-assistant


**Install dependencies**

pip install -r requirements.txt


**Add your API keys**

Replace API_KEY in the code with your OpenWeather API Key → Get one here

Replace NEWS_API_KEY with your NewsAPI Key → Get one here

Run the assistant

python vortex.py


**🎤 Example Commands****

Introduction → "Who are you?"

Date/Day → "What’s the date today?"

Maths → "Calculate 25 times 4", "What is the square root of 81"

Weather → "What’s the weather in New York?"

News → "Give me sports news from US"

System Control → "Shutdown the computer", "Show CPU usage"

Entertainment → "Tell me a joke", "Play music", "Open YouTube"

Camera & Recording → "Take a selfie", "Record webcam video for 10 seconds"

**🔮 Future Improvements**

Smarter AI Chatbot → Integrate with Gemini API / GPT for natural conversations

Personalized Assistant → Save user preferences (e.g., favorite apps, locations, reminders)

Reminder & Calendar Integration → Set alarms, events, and reminders with Google Calendar API

Email & Messaging Support → Send/Read emails, WhatsApp, or SMS using voice commands

Home Automation → Control IoT devices (smart lights, fans, AC) via Google Home / MQTT

Offline Mode → Enable limited functionality without internet (math, system control, apps)

Continuous Listening → Background wake word detection (“Hey Vortex”)

Improved Security → Voice recognition & authentication before executing sensitive commands

Web Dashboard → GUI to configure commands, view logs, and track system stats

Plugin System → Let users add custom commands easily without editing core code

Multi-language Support → Add support for commands in Hindi, Spanish, etc.

Mobile Companion App → Control PC via a connected mobile app
