import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 130)  # Slower speech for kids
engine.setProperty('volume', 1.0)

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize child's voice input with retries
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Child said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that. Could you please say it again?")
            return None
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the recognition service.")
            return None

# Function to fetch the answer to a general knowledge question
def fetch_general_knowledge():
    speak("What do you want to know?")
    question = listen()
    if question:
        try:
            answer = wikipedia.summary(question, sentences=2)
            speak(f"Here's what I found: {answer}")
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"Sorry, there are multiple results for {question}. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak(f"Sorry, I couldn't find any information about {question}.")
        except wikipedia.exceptions.HTTPError:
            speak("There was a problem fetching data from Wikipedia.")
        except Exception as e:
            speak(f"An error occurred: {str(e)}")

# Function to play nursery rhymes or educational videos
def play_educational_video():
    speak("What nursery rhyme or educational video would you like to watch?")
    video_name = listen()
    if video_name:
        speak(f"Playing {video_name} for you.")
        pywhatkit.playonyt(f"{video_name} nursery rhyme or educational video")

# Function to tell a joke for kids
def tell_joke():
    joke = pyjokes.get_joke(category='neutral')
    speak(joke)

# Function to tell the current time and date
def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")  # 12-hour format
    current_date = now.strftime("%B %d, %Y")
    speak(f"The current time is {current_time} and today's date is {current_date}.")

# Main function to run the assistant
def run_learning_assistant():
    speak("Hello! I am your Voice-Activated Learning Assistant. How can I help you today?")
    
    while True:
        command = listen()

        if command:
            if 'what is' in command or 'tell me about' in command:
                fetch_general_knowledge()

            elif 'play nursery rhyme' in command or 'play educational video' in command:
                play_educational_video()

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
    run_learning_assistant()
