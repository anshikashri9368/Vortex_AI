import speech_recognition as sr
import pyttsx3
import webbrowser, random, datetime, time, os, platform, subprocess, re
from dateutil import parser
from sympy import sympify, sqrt, sin, cos, tan, log, pi
import pyautogui
import numpy as np
from num2words import num2words
import datetime
import requests
import psutil
import cv2
import time
import webbrowser
import urllib.parse


# ---------- SPEAK ----------
def say(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 175)
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# ---------- LISTEN ----------
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-US")
        print(f"You said: {query}")
        return query.lower()
    except Exception as e:
        print("Error in recognition:", e)
        return ""

# ---------- INTRO ----------
def introduce():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon!"
    elif 17 <= hour < 21:
        greeting = "Good Evening!"
    else:
        greeting = "Hello!"
    say(f"{greeting}! I am Vortex, your intelligent virtual assistant.")
say("I was created by Anshika Shrivastava to simplify the way you interact with your digital world.")
say("From managing your dates and schedules to solving calculations in seconds, I’m always ready to help.")
say("I can open applications, launch your favorite websites, crack a joke to lighten your mood, or check the latest weather for you.")
say("Need a screenshot or a screen recording? I can handle that too—quickly and efficiently.")
say("I can also play games with you, manage your to-do lists, and assist with daily tasks that make life easier.")
say("And the best part? I’m constantly learning and evolving, because my creator keeps updating me with new skills and features.")
say("Over time, I’ll only get smarter, more interactive, and more capable of understanding your needs.")
say("Think of me as your personal companion—always alert, always adapting, and always here to assist you.")
say("Whether it’s work, study, or entertainment, I’ll make your experience faster and smoother.")
say("So go ahead, give me a command, and let’s get started.")
say("How can I assist you today?")




# ---------- DATE HANDLER ----------
def handle_date_query(query):
    today = datetime.date.today()
    if "today" in query or "current" in query:
        date_str = today.strftime("%d %B %Y")
        day_name = today.strftime("%A")
        return f"Today is {date_str} and it’s {day_name}."
    elif any(char.isdigit() for char in query):
        try:
            parsed_date = parser.parse(query, fuzzy=True).date()
            day_name = parsed_date.strftime("%A")
            return f"{parsed_date.strftime('%d %B %Y')} was a {day_name}."
        except:
            return "Sorry, I could not understand that date."
    else:
        days_map = {"monday":0, "tuesday":1, "wednesday":2,"thursday":3,"friday":4,"saturday":5,"sunday":6}
        for day_word, day_num in days_map.items():
            if day_word in query.lower():
                today_num = today.weekday()
                days_ahead = (day_num - today_num + 7) % 7
                if days_ahead == 0:
                    days_ahead = 7
                upcoming_date = today + datetime.timedelta(days=days_ahead)
                return f"The upcoming {day_word.capitalize()} is on {upcoming_date.strftime('%d %B %Y')}."
        return "Sorry, I couldn’t understand your question."

# ---------- AGE HANDLER ----------

def handle_age_query(query):
    today = datetime.date.today()
    
    # Ask for birthday if not provided
    if "age" in query and not any(char.isdigit() for char in query):
        say("May I know your birthday? Please say it like: I was born on 5 May 2000.")
        return ""

    try:
        # Parse the date from the query
        parsed_date = parser.parse(query, fuzzy=True).date()
        
        # Calculate age
        age = today.year - parsed_date.year - ((today.month, today.day) < (parsed_date.month, parsed_date.day))
        
        # Birthday message
        birthday_msg = ""
        if today.month == parsed_date.month and today.day == parsed_date.day:
            birthday_msg = "Happy Birthday! 🎉🎂 "

        return (f"{birthday_msg}You are {age} years old. "
                f"You were born on {parsed_date.strftime('%d %B %Y')} "
                f"which was a {parsed_date.strftime('%A')}.")

    except Exception as e:
        return "Sorry, I could not understand your birthday."


# ---------- APP OPENER ----------
APP_PATHS = {
    "notepad": "notepad.exe",
    "figma": "C:\\Users\\HP5CD\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Figma",
    "calculator": "calc.exe",
}
def open_app(query):
    system_os = platform.system()
    for app_name, app_path in APP_PATHS.items():
        if app_name in query:
            try:
                if system_os == "Windows":
                    os.startfile(app_path)
                elif system_os == "Darwin":
                    subprocess.Popen(["open", app_path])
                else:
                    subprocess.Popen([app_path])
                if app_name == "notepad":
                    time.sleep(1)
                    say("Do you want to write yourself or should I write for you?")
                    choice = takeCommand()
                    if "you write" in choice or "write for me" in choice:
                        say("What topic should I write about?")
                        topic = takeCommand()
                        with open("notepad_temp.txt","w") as f:
                            f.write(f"This is a note about {topic}. You can edit it later.\n")
                        os.startfile("notepad_temp.txt")
                    say("Notepad has been opened and written successfully.")
                elif app_name == "calculator":
                    say("Calculator has been opened successfully.")
                else:
                    say(f"{app_name.capitalize()} has been opened successfully.")
                return f"Opening {app_name.capitalize()}."
            except Exception as e:
                return f"Sorry, I couldn’t open {app_name}. Error: {e}"
    return "Sorry, I don’t know this app. Please add it to APP_PATHS."

# ---------- MATHS HANDLER ----------
def handle_math_query(query):
    try:
        # 1️⃣ Normalize input
        query = query.lower()
        query = query.replace("calculate", "").replace("what is", "").replace("solve", "").strip()

        # 2️⃣ Replace words with math symbols
        replacements = {
            "plus":"+","minus":"-","times":"*","multiply":"*","x":"*",
            "divide":"/","over":"/","mod":"%","power":"**","raised to":"**","pi":"pi"
        }
        for word, symbol in replacements.items():
            query = re.sub(rf"\b{word}\b", symbol, query)  # word-boundary safe replacement

        # Helper to format numbers for speech
        def speak_num(val):
            val = round(float(val), 2)
            return num2words(val)  # converts 12.5 → "twelve point five"

        # 3️⃣ Square root
        if "square root" in query:
            match = re.search(r"square root of (\d+(\.\d+)?)", query)
            if match:
                num = float(match.group(1))
                result = speak_num(sqrt(num).evalf())
                return f"The square root of {num} is {result}."

        # 4️⃣ Trigonometry (degrees)
        trig_match = re.search(r"(sin|cos|tan)\s*(\d+(\.\d+)?)", query)
        if trig_match:
            func, angle, _ = trig_match.groups()
            angle_rad = float(angle) * pi / 180
            result = speak_num({"sin": sin(angle_rad), "cos": cos(angle_rad), "tan": tan(angle_rad)}[func].evalf())
            return f"The result of {func} {angle} degrees is {result}."

        # 5️⃣ Logarithms
        log_match = re.search(r"log(?: base (\d+))? of (\d+(\.\d+)?)", query)
        if log_match:
            base, num, _ = log_match.groups()
            num = float(num)
            base = float(base) if base else 10
            result = speak_num(log(num, base).evalf())
            return f"The log base {base} of {num} is {result}."

        # 6️⃣ General arithmetic / exponentiation
        expression = sympify(query)
        result = speak_num(expression.evalf())
        return f"The result of {expression} is {result}."

    except Exception as e:
        return f"Sorry, I couldn’t solve that. Error: {e}"


# ---------- JOKES ----------
def tell_joke():
    jokes = [
        "Why did the computer show up at work late? It had a hard drive.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "Why was the math book sad? Because it had too many problems."
    ]
    return random.choice(jokes)

# ---------- SCREENSHOT ----------
def take_screenshot():
    screenshot = pyautogui.screenshot()
    filename = f"screenshot_{int(time.time())}.png"
    screenshot.save(filename)
    say(f"Screenshot saved successfully as {filename}.")

# ---------- SCREEN RECORD ----------
def screen_record(duration=10):
    say(f"Recording screen for {duration} seconds.")
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    filename = f"screen_record_{int(time.time())}.avi"
    out = cv2.VideoWriter(filename,fourcc,8.0,screen_size)
    start_time = time.time()
    while time.time()-start_time < duration:
        img = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        out.write(frame)
    out.release()
    say(f"Screen recording of {duration} seconds saved successfully as {filename}.")

# ------------- WEATHER HANDLER ----------
# open weather handler..

API_KEY = "768e8b49893fd5a7148bbb1435a21c98"  # Get it from https://openweathermap.org/api

# Precautions based on weather condition
WEATHER_PRECAUTIONS = {
    "rain": "Carry an umbrella or wear a raincoat.",
    "storm": "Avoid going outside and stay safe indoors.",
    "snow": "Wear warm clothes and be careful while traveling.",
    "sun": "Use sunscreen and stay hydrated.",
    "fog": "Drive carefully and avoid outdoor travel if possible.",
    "cloud": "Weather is cloudy, a light jacket is recommended.",
    "thunderstorm": "Stay indoors and avoid using electrical appliances.",
    "drizzle": "Carry a small umbrella or raincoat."
}

def get_weather(query):
    try:
        # Try to detect city/state/country from query
        location_match = re.search(r"in ([a-zA-Z\s]+)", query)
        if location_match:
            location = location_match.group(1).strip()
        else:
            say("Please tell me the city, state, or country name for weather information.")
            location = takeCommand()

        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            return f"Sorry, I could not find weather information for {location}."

        # Weather details
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Suggest precautions
        precaution = ""
        for key in WEATHER_PRECAUTIONS:
            if key in weather_desc.lower():
                precaution = WEATHER_PRECAUTIONS[key]
                break

        # Build response
        response_text = (f"Weather in {location}: {weather_desc}, temperature {temp}°C, "
                         f"feels like {feels_like}°C, humidity {humidity}%, wind speed {wind_speed} m/s.")
        if precaution:
            response_text += f" Suggestion: {precaution}"

        response_text += " Weather information retrieved successfully."
        return response_text

    except Exception as e:
        return f"Sorry, I couldn't retrieve the weather. Error: {e}"



# ---------- NEWS HANDLER ----------
import requests

NEWS_API_KEY = "6cded99431a94183bc28a90e18e86417"  # Replace with your NewsAPI key

def get_news(query="general", country="us"):
    """
    query: topic like 'technology', 'sports', 'business', 'entertainment'
    country: ISO 2-letter country code, e.g., 'us', 'in', 'gb'
    """
    try:
        url = f"https://newsapi.org/v2/top-headlines?q={query}&country={country}&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data["status"] != "ok" or len(data["articles"]) == 0:
            return f"Sorry, no news found for {query} in {country.upper()}."

        # Get top 5 news headlines
        headlines = [f"{i+1}. {article['title']}" for i, article in enumerate(data["articles"][:5])]
        news_text = f"Here are the top news for {query} in {country.upper()}:\n" + "\n".join(headlines)
        news_text += "\nNews retrieved successfully."
        return news_text

    except Exception as e:
        return f"Sorry, I couldn't fetch the news. Error: {e}"


# ---------------------- SYSTEM CONTROL ----------------------
def confirm_action(action_name):
    say(f"Are you sure you want me to {action_name}? Please say yes or no.")
    response = takeCommand()
    return "yes" in response or "sure" in response

def system_shutdown():
    if confirm_action("shutdown the computer"):
        if platform.system() == "Windows":
            os.system("shutdown /s /t 5")
        else:
            os.system("sudo shutdown now")
        say("Shutting down...")

def system_restart():
    if confirm_action("restart the computer"):
        if platform.system() == "Windows":
            os.system("shutdown /r /t 5")
        else:
            os.system("sudo reboot")
        say("Restarting...")

def system_logoff():
    if confirm_action("log off"):
        if platform.system() == "Windows":
            os.system("shutdown /l")
        else:
            os.system("logout")
        say("Logging off...")

def system_sleep():
    if confirm_action("put the computer to sleep"):
        if platform.system() == "Windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        else:
            os.system("systemctl suspend")
        say("Sleeping...")

def system_info():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_total = round(ram.total / (1024**3),2)
    ram_used = round(ram.used / (1024**3),2)
    ram_free = round(ram.available / (1024**3),2)
    disk = psutil.disk_usage('/')
    disk_total = round(disk.total / (1024**3),2)
    disk_used = round(disk.used / (1024**3),2)
    disk_free = round(disk.free / (1024**3),2)
    say(f"CPU: {cpu}%, RAM: {ram_used}/{ram_total} GB ({ram.percent}%), Disk: {disk_used}/{disk_total} GB ({disk.percent}%)")

def drive_status():
    drives = ['C','D','E','F']
    for drive in drives:
        if os.path.exists(f"{drive}:\\"):
            usage = psutil.disk_usage(f"{drive}:\\")
            say(f"Drive {drive}: Total {round(usage.total/1024**3,2)} GB, Used {round(usage.used/1024**3,2)} GB, Free {round(usage.free/1024**3,2)} GB, Usage {usage.percent}%")
        else:
            say(f"Drive {drive} does not exist.")

# ---------------------- PROACTIVE MONITOR ----------------------
def proactive_system_monitor(interval=60):
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        if cpu>80:
            say(f"Warning! High CPU usage: {cpu}%")
        if ram.percent>85:
            say(f"Warning! High RAM usage: {ram.percent}%")
        drives = ['C','D','E','F']
        for drive in drives:
            if os.path.exists(f"{drive}:\\"):
                usage = psutil.disk_usage(f"{drive}:\\")
                if 100-usage.percent <10:
                    say(f"Warning! Low disk space on drive {drive}: {round(usage.free/1024**3,2)} GB free.")
        time.sleep(interval)


# ------------------ TAKE PICTURE FUNCTION ------------------
def take_picture():
    say("Now pose, I will click your picture. Get ready!")
    
    # Countdown
    for i in range(3, 0, -1):
        say(str(i))
        time.sleep(1)

    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        say("Sorry, I could not access the camera.")
        return

    ret, frame = cap.read()
    if ret:
        filename = f"selfie_{int(time.time())}.png"
        cv2.imwrite(filename, frame)
        say("Smile! Your picture has been clicked successfully.")
        print(f"Picture saved as {filename}")
    else:
        say("Sorry, I could not capture the image.")
    
    
    # ---------- WEBCAM VIDEO RECORDING BLOCK ----------
def record_webcam_video():
    say("For how many seconds should I record the video?")
    try:
        duration = int(takeCommand())
    except:
        duration = 15  # default duration if recognition fails
    
    say("Get ready! Recording will start in 3 seconds.")
    
    # Countdown before recording
    for i in range(3, 0, -1):
        say(str(i))
        time.sleep(1)
    
    say(f"Recording video from your webcam for {duration} seconds.")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        say("Sorry, I could not access the webcam.")
        return

    # Get frame dimensions
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    filename = f"webcam_video_{int(time.time())}.avi"
    out = cv2.VideoWriter(filename, fourcc, 20.0, (frame_width, frame_height))

    start_time = time.time()
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            continue
        out.write(frame)

    cap.release()
    out.release()
    say(f"Video recording completed successfully. Saved as {filename}.")
    print(f"Video saved as {filename}")

# ---------- SMART YOUTUBE CONTROL BLOCK ----------
def smart_youtube_control():
    say("What would you like to watch on YouTube?")
    query = takeCommand()
    
    if query == "":
        say("I didn't catch that. Please try again.")
        return
    
    # Encode the search query for URL
    search_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={search_query}"
    
    # Open YouTube search results in default browser
    webbrowser.open(url)
    say(f"Here are the search results for {query} on YouTube.")
    
    # Optional: Ask to play first video automatically
    say("Do you want me to play the first video automatically?")
    choice = takeCommand()
    if "yes" in choice or "sure" in choice:
        first_video_url = f"https://www.youtube.com/results?search_query={search_query}&sp=EgIQAQ%3D%3D"
        webbrowser.open(first_video_url)
        say(f"Playing the first video for {query} on YouTube.")


# ---------- MAIN ----------
if __name__ == "__main__":
    say("Hello!")
    music_dir = "C:\\Users\\HP5CD\\OneDrive\\Desktop\\music"
    songs = [s for s in os.listdir(music_dir) if s.endswith(".mp3")] if os.path.exists(music_dir) else []
    websites = {"google":"https://www.google.com","youtube":"https://www.youtube.com","facebook":"https://www.facebook.com"}
    
    while True:
        query = takeCommand()
        if query == "":
            continue
        
# introduction
        elif "who are you" in query or "introduce yourself" in query:
            introduce()
            
#smart youtube controller
        elif "youtube" in query or "play on youtube" in query:
            smart_youtube_control()  
     
        elif "ask jan" in query or "smart mode" in query:
            say("What do you want to ask me?")
            user_input = takeCommand()  # your existing function to listen
            if user_input:
                answer = ask_jan(user_input)  # call Jan AI
                say(answer)
          
# tell the date
        elif "date" in query or "day" in query:
            say(handle_date_query(query))
            say("Date information retrieved successfully.")

#  take picture
        elif "click" in query or "take picture" in query or "selfie" in query:
            take_picture()

#video recording
    
        elif "record video" in query or "webcam video" in query or "start video recording" in query:
           record_webcam_video()
      
# age handler
        elif "age" in query or "born" in query or "birthday" in query:
            response = handle_age_query(query)
            if response:
                say(response)
                say("Age calculation completed successfully.")
             
       
#weather...........
        elif "weather" in query:
           say(get_weather(query))

# open apps
        elif "open" in query:
            say(open_app(query))
            
 # calculate maths
        elif "calculate" in query or "solve" in query or "what is" in query:
            say(handle_math_query(query))
            say("Calculation completed successfully.")
            
         
# open sites
        elif any(site in query for site in websites):
            for site,url in websites.items():
                if site in query:
                    say(f"Opening {site}")
                    webbrowser.open(url)
                    say(f"{site.capitalize()} opened successfully.")
                    break
             
# play music
        elif "play music" in query:
            if songs:
                song = random.choice(songs)
                os.startfile(os.path.join(music_dir,song))
                say(f"Playing {song}")
                say("Music playback started successfully.")
            else:
                say("No songs found in your music folder.")
                
# tell jokes
        elif "joke" in query:
            say(tell_joke())
            say("Joke delivered successfully.")
            
 # screen shot
        elif "screenshot" in query:
            take_screenshot()
            
# screen record
        elif "screen record" in query:
            
            say("Starting screen recording.")
            say("For how many seconds should I record?")
            say("Please specify the duration in seconds.")
            try:
                duration = int(takeCommand())
            except:
                duration = 30
            screen_record(duration)
            
# tell the news
        elif "news" in query:
            say("Which topic do you want news for? For example: technology, sports, business, entertainment.")
            topic = takeCommand()
            say("Which country? Please say the 2-letter country code like us, in, gb.")
            country = takeCommand()
            say(get_news(topic, country))
       
# System control
        elif "shutdown" in query:
            system_shutdown()
        elif "restart" in query:
            system_restart()
        elif "log off" in query:
            system_logoff()
        elif "sleep" in query:
            system_sleep()
        elif "cpu" in query or "ram" in query or "disk" in query:
            system_info()
        elif "drive status" in query or "storage" in query:
            drive_status()

# exit the assistant
        elif "exit" in query or "quit" in query or "stop" in query:
            say("i never want to leave you but if you want me to go... then i go")
            say("Goodbye! Have a nice day.")
            break
            