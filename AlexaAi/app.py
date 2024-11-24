import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to the user's voice and return the recognized command."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Dynamically adjust to noise
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not catch that. Could you repeat?")
            return None
        except sr.RequestError:
            speak("It seems there is a network issue.")
            return None
        except sr.WaitTimeoutError:
            speak("I did not hear anything. Please try again.")
            return None

def process_command(command):
    """Process the user's command and perform actions."""
    if command:
        if 'play' in command:
            song = command.replace('play', '').strip()
            speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)

        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {current_time}.")

        elif 'who is' in command or 'what is' in command:
            query = command.replace('who is', '').replace('what is', '').strip()
            try:
                info = wikipedia.summary(query, sentences=2)
                speak(info)
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results for this query. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("I couldn't find any information on that.")

        elif 'joke' in command:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'stop' in command or 'exit' in command:
            speak("Goodbye!")
            return False

        else:
            speak("I am not sure how to respond to that.")
        return True
    else:
        return True

# Main program loop
def main():
    speak("Hello! I am your assistant. How can I help you?")
    active = True
    while active:
        command = listen()
        if command is not None:
            active = process_command(command)

if __name__ == "__main__":
    main()
