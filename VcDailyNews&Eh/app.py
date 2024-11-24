import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
from textblob import TextBlob  # For spell correction

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Initialize recognizer
recognizer = sr.Recognizer()

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

# Function to fetch the latest news headlines
def fetch_news():
    speak("Fetching the latest news headlines.")
    pywhatkit.playonyt("latest news headlines")

# Function to play trending music videos
def play_trending_music():
    speak("Playing trending music videos.")
    pywhatkit.playonyt("trending music videos")

# Function to fetch information about a trending topic
def fetch_trending_topic_info():
    speak("Please tell me the topic you'd like to know more about.")
    topic = listen()
    if topic:
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(f"Here's what I found about {topic}: {summary}")
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"Sorry, there are multiple results for {topic}. Please be more specific.")
        except wikipedia.exceptions.HTTPError:
            speak("There was a problem fetching data from Wikipedia.")
        except wikipedia.exceptions.PageError:
            speak(f"Sorry, I couldn't find any information on {topic}.")
        except Exception as e:
            speak(f"An error occurred: {str(e)}")

# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Function to tell the current date and time
def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%B %d, %Y")
    speak(f"The current time is {current_time} and today's date is {current_date}.")

# Main function to run the assistant
def run_voice_assistant():
    speak("Hello! I am your Voice-Controlled Daily News and Entertainment Hub.")
    speak("What would you like to do today?")
    
    while True:
        command = listen()

        if command:
            if 'latest news' in command:
                fetch_news()

            elif 'trending music' in command or 'play music' in command:
                play_trending_music()

            elif 'trending topic' in command or 'topic info' in command:
                fetch_trending_topic_info()

            elif 'joke' in command:
                tell_joke()

            elif 'time' in command or 'date' in command:
                tell_time()

            elif 'exit' in command or 'quit' in command:
                speak("Goodbye! Have a great day!")
                break
        else:
            speak("I didn't catch that, can you please repeat?")

if __name__ == "__main__":
    run_voice_assistant()
