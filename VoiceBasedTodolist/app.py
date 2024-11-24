import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time
from textblob import TextBlob  # Importing TextBlob for spell correction

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Initialize recognizer
recognizer = sr.Recognizer()

# To store the tasks
task_list = []

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize user's voice input with retries
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            corrected_command = correct_spelling(command)  # Correct the spelling
            print(f"Corrected command: {corrected_command}")  # Show the corrected command
            return corrected_command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that. Could you please say it again?")
            return None
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the recognition service.")
            return None

# Function to correct spelling of a command
def correct_spelling(command):
    blob = TextBlob(command)  # Using TextBlob to correct spelling
    corrected = blob.correct()  # Correct the spelling of the sentence
    return str(corrected)

# Function to add a task
def add_task():
    speak("Please tell me the task you'd like to add.")
    task = listen()
    if task:
        task_list.append({"task": task, "deadline": None})
        speak(f"Task '{task}' has been added to your to-do list.")
    else:
        speak("Sorry, I couldn't understand the task. Please try again.")

# Function to show tasks
def show_tasks():
    if not task_list:
        speak("Your to-do list is empty.")
    else:
        speak("Here are your tasks:")
        for index, task in enumerate(task_list, 1):
            deadline_text = f" Deadline: {task['deadline']}" if task['deadline'] else ""
            speak(f"Task {index}: {task['task']}{deadline_text}")

# Function to set a deadline for a task
def set_deadline():
    speak("Please tell me the task number to which you'd like to add a deadline.")
    task_number = listen()
    try:
        if task_number:
            task_number = int(task_number.split()[-1]) - 1
            if task_number < len(task_list):
                speak("Please tell me the deadline for this task.")
                deadline = listen()
                if deadline:
                    task_list[task_number]["deadline"] = deadline
                    speak(f"Deadline '{deadline}' has been set for task '{task_list[task_number]['task']}'.")
                else:
                    speak("Sorry, I didn't understand the deadline. Please try again.")
            else:
                speak("Invalid task number.")
    except ValueError:
        speak("Please provide a valid task number.")

# Function to play motivational music based on task
def play_motivational_music():
    speak("Tell me the task or topic you'd like to hear motivational music about.")
    task = listen()
    if task:
        speak(f"Playing motivational music related to {task}.")
        pywhatkit.playonyt(f"motivational music for {task}")
    else:
        speak("Sorry, I didn't catch that. Please try again.")

# Function to fetch information related to a task from Wikipedia
def fetch_task_info():
    speak("Please tell me the task or topic you'd like information on.")
    task = listen()
    if task:
        try:
            summary = wikipedia.summary(task, sentences=2)
            speak(f"Here's what I found about {task}: {summary}")
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"Sorry, there are multiple results for {task}. Please be more specific.")
        except wikipedia.exceptions.HTTPError:
            speak("There was a problem fetching data from Wikipedia.")
        except wikipedia.exceptions.PageError:
            speak(f"Sorry, I couldn't find any information on {task}.")
        except Exception as e:
            speak(f"An error occurred: {str(e)}")

# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Main function to run the assistant
def run_voice_assistant():
    speak("Hello! I am your Interactive Voice-Based To-Do List Manager.")
    speak("What would you like to do today?")
    
    while True:
        command = listen()

        if command:
            if 'add task' in command:
                add_task()

            elif 'show tasks' in command:
                show_tasks()

            elif 'set deadline' in command:
                set_deadline()

            elif 'motivational music' in command:
                play_motivational_music()

            elif 'task info' in command:
                fetch_task_info()

            elif 'joke' in command:
                tell_joke()

            elif 'exit' in command or 'quit' in command:
                speak("Goodbye! Have a great day!")
                break

            else:
                speak("Sorry, I didn't understand that command. Please try again.")
        else:
            speak("I didn't catch that, can you please repeat?")

if __name__ == "__main__":
    run_voice_assistant()
