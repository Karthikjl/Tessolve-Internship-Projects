import tkinter as tk
from tkinter import messagebox
import pyttsx3
import requests
import datetime
import pywhatkit
import wolframalpha
import pyjokes
import json
import speech_recognition as sr
import keyboard
import wikipedia

# Setup for text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Setup for WolframAlpha API
wolfram_client = wolframalpha.Client("H3RGGW-RK4Y5QH4T3")

# Weather API key
weather_api_key = "bea7558629b8172159af7eac4ef8ad18"

# Global variable for assistant's name
assistant_name = "David"

# Knowledge base for storing learned answers
knowledge_base = {}

# Function to speak the response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get weather information
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data['cod'] == 200:
            weather = data['main']
            description = data['weather'][0]['description']
            temp = weather['temp']
            weather_info = f"The weather in {city} is currently {description} with a temperature of {temp}°C."
            return weather_info
        elif data['cod'] == 404:
            return f"City '{city}' not found. Please try again."
        else:
            return f"Error fetching weather data. (Code: {data['cod']})"
    except Exception as e:
        return f"There was an error fetching the weather information. Please try again. (Error: {e})"

# Function to get Wikipedia search results
def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found. Please be more specific. Choices: {e.options}"
    except Exception as e:
        return "There was an issue with Wikipedia search. Please try again."

# Function to get news headlines
def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=fd237b1ac0bc4267bb47c48e9a843dae"
        response = requests.get(url)
        data = response.json()
        articles = data['articles'][:5]
        news = "Top 5 News Headlines:\n"
        for i, article in enumerate(articles):
            news += f"{i + 1}. {article['title']}\n"
        return news
    except Exception:
        return "There was an error fetching the news. Please try again."

# Function to answer general knowledge questions
def answer_general_questions(query):
    try:
        res = wolfram_client.query(query)
        answer = next(res.results, None)
        if answer:
            return answer.text
        else:
            return "I couldn't find an answer for that. Would you like to ask something else?"
    except Exception:
        return "There was an issue with fetching the answer. Please try again."

# Function to handle joke requests
def tell_joke():
    return pyjokes.get_joke()

# Function to handle time-related queries
def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

# Function to send WhatsApp messages
def send_whatsapp_message(phone, message):
    try:
        pywhatkit.sendwhatmsg_instantly(phone, message)
        return f"Message sent to {phone}: {message}"
    except Exception:
        return "Failed to send the WhatsApp message. Please check the phone number and try again."

# Function to play YouTube video
def play_youtube_video(video_name):
    try:
        pywhatkit.playonyt(video_name)  # Automatically searches and plays the video on YouTube
        return f"Playing '{video_name}' on YouTube."
    except Exception as e:
        return f"An error occurred while trying to play the video: {e}"

# Function to process the command
def process_command(query):
    query = query.lower()
    if 'how are you' in query:
        response = "I'm an AI assistant, always ready to help you. How can I assist?"
    elif 'hello' in query:
        response = "Hello! How can I assist you today?"
    elif 'weather' in query:
        city = query.split('in')[-1].strip()
        response = get_weather(city)
    elif 'news' in query:
        response = get_news()
    elif 'joke' in query:
        response = tell_joke()
    elif 'time' in query:
        response = f"The time is {get_time()}."
    elif 'whatsapp' in query:
        try:
            parts = query.split("to")
            phone = parts[1].strip().split("message")[0].strip()
            message = parts[1].split("message")[1].strip()
            response = send_whatsapp_message(phone, message)
        except IndexError:
            response = "Please provide both the phone number and the message."
    elif 'who is' in query or 'what is' in query or 'how does' in query or 'why' in query or 'calculate' in query:
        response = answer_general_questions(query)
    elif 'thank you' in query:
        response = "You're welcome! Let me know if you need further help."
    elif 'wikipedia' in query:
        search_term = query.split("wikipedia")[-1].strip()
        response = search_wikipedia(search_term)
    elif 'play video' in query or 'play youtube' in query:
        video_name = query.replace("play video on youtube", "").replace("play youtube", "").strip()
        if not video_name:
            response = "Please specify the video name."
        else:
            response = play_youtube_video(video_name)
    else:
        response = "I'm sorry, I couldn't understand that. Could you please clarify?"
    return response

# Save the knowledge base to a file
def save_knowledge():
    with open("knowledge_base.json", "w") as file:
        json.dump(knowledge_base, file)

# Load the knowledge base from a file
def load_knowledge():
    global knowledge_base
    try:
        with open("knowledge_base.json", "r") as file:
            knowledge_base = json.load(file)
    except FileNotFoundError:
        knowledge_base = {}

# Submit command from entry box
def submit_command():
    user_input = command_entry.get()
    result_text.insert(tk.END, f"User: {user_input}\n")
    response = process_command(user_input)
    result_text.insert(tk.END, f"Assistant: {response}\n")
    speak(response)

# Quit the application using Ctrl+Q
def quit_application(event=None):
    root.quit()

# Function for speech recognition
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=5)
        try:
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            result_text.insert(tk.END, f"User: {query}\n")
            response = process_command(query)
            result_text.insert(tk.END, f"Assistant: {response}\n")
            speak(response)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Sorry, the speech service is down.")
        except Exception as e:
            print(f"An error occurred: {e}")

# Setting up the GUI
root = tk.Tk()
root.title(f"{assistant_name} - Virtual Assistant")
root.geometry("500x500")
root.configure(bg="lightblue")

# Bind Ctrl+Q to quit
root.bind("<Control-q>", quit_application)

# Display for showing conversation
result_text = tk.Text(root, height=20, width=60, wrap=tk.WORD)
result_text.pack(pady=10)

# Entry box for user input
command_entry = tk.Entry(root, width=50)
command_entry.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", width=20, command=submit_command)
submit_button.pack(pady=5)

# Microphone button for voice command
microphone_button = tk.Button(root, text="Speak", width=20, command=listen_command)
microphone_button.pack(pady=5)

# Start the GUI
load_knowledge()
root.mainloop()
