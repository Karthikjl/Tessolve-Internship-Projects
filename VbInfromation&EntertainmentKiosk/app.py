import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize the user's voice input
def listen():
    with sr.Microphone() as source:
        print("Listening...")  # Informing that the system is listening
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that. Could you please say it again?")
            return ""
        except sr.RequestError:
            speak("Sorry, I am unable to connect to the speech recognition service.")
            return ""

# Function to tell jokes
def tell_joke():
    joke = pyjokes.get_joke(category='neutral')
    speak(joke)

# Function to provide the current time and date
def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")  # 12-hour format
    current_date = now.strftime("%B %d, %Y")
    speak(f"The current time is {current_time} and today's date is {current_date}.")

# Function to fetch information from Wikipedia
def fetch_information(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Sorry, there are multiple results for {query}. Could you be more specific?")
    except wikipedia.exceptions.PageError:
        speak(f"Sorry, I couldn't find any information about {query}.")
    except Exception as e:
        speak(f"An error occurred: {str(e)}")

# Function to play songs using YouTube
def play_song(song):
    speak(f"Playing {song} on YouTube.")
    pywhatkit.playonyt(song)

# Function to send a message via WhatsApp
def send_whatsapp_message(contact, message):
    speak(f"Sending message to {contact}.")
    pywhatkit.sendwhatmsg_instantly(contact, message)

# Main function to run the kiosk
def run_kiosk():
    speak("Hello! I am your Voice-Based Information and Entertainment Kiosk.")
    
    while True:
        command = listen()
        
        if command:
            if 'what is' in command or 'tell me about' in command:
                query = command.replace("what is", "").replace("tell me about", "").strip()
                fetch_information(query)
            
            elif 'joke' in command:
                tell_joke()
                
            elif 'time' in command or 'date' in command:
                tell_time()
                
            elif 'play' in command:
                song = command.replace("play", "").strip()
                play_song(song)
                
            elif 'send a message' in command:
                speak("Please tell me the contact number or name to send the message to.")
                contact = listen()
                speak("What message would you like to send?")
                message = listen()
                send_whatsapp_message(contact, message)
                
            elif 'exit' in command or 'quit' in command:
                speak("Goodbye! Have a great day!")
                break

            else:
                speak("Sorry, I didn't understand that command. Please try again.")

if __name__ == "__main__":
    run_kiosk()
