import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to list and set the voice type (male or female)
def set_voice(gender='female'):
    voices = engine.getProperty('voices')
    
    # Default to female if gender is not recognized
    selected_voice = None
    if gender.lower() == 'male':
        for voice in voices:
            if 'male' in voice.name.lower():
                selected_voice = voice
                break
        # If no male voice is found, use the first available voice
        if not selected_voice:
            selected_voice = voices[0]
    
    elif gender.lower() == 'female':
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                selected_voice = voice
                break
        # If no female voice is found, use the first available voice
        if not selected_voice:
            selected_voice = voices[1] if len(voices) > 1 else voices[0]

    # Apply the selected voice
    engine.setProperty('voice', selected_voice.id)
    print(f"Voice set to: {selected_voice.name}")

# Function to take voice input from the user
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception as e:
        print("Sorry, I didn't catch that. Please say that again.")
        return None
    return query.lower()

# Main function to handle commands
def run_voice_assistant():
    speak("Hello! I am your voice assistant. How can I help you today?")
    
    while True:
        query = take_command()
        if query is None:
            continue

        # Playing a song on YouTube
        elif 'play' in query:
            song = query.replace('play', '')
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        # Telling the current time
        elif 'time' in query:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {current_time}")

        # Searching something on Wikipedia
        elif 'who is' in query or 'what is' in query:
            search_query = query.replace('who is', '').replace('what is', '')
            speak(f"Searching Wikipedia for {search_query}")
            try:
                summary = wikipedia.summary(search_query, sentences=2)
                speak("According to Wikipedia")
                speak(summary)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple results for this query. Please be more specific.")
            except Exception as e:
                speak("Sorry, I could not find any information on that.")

        # Telling a joke
        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        # Sending a WhatsApp message (requires phone number and message content)
        elif 'send whatsapp message' in query:
            speak("To whom do you want to send the message?")
            phone_number = input("Enter the phone number (with country code): ")
            speak("What is the message?")
            message = input("Enter your message: ")
            pywhatkit.sendwhatmsg(phone_number, message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
            speak("Message will be sent shortly.")

        # Exiting the assistant
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a great day!")
            break

        else:
            speak("I didn't understand that. Please try again.")

if __name__ == "__main__":
    print("Select Voice Type:")
    print("1. Male")
    print("2. Female")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        set_voice('male')
    else:
        set_voice('female')

    run_voice_assistant()
