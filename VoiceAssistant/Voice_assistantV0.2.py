import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import wolframalpha

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# WolframAlpha Client (Replace with your own API key)
wolfram_client = wolframalpha.Client("QGER3J-5QJAJE6UGV")

# Global variable for assistant's name
assistant_name = "Assistant"

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to set the voice type (male or female)
def set_voice(gender='female'):
    voices = engine.getProperty('voices')
    selected_voice = None

    if gender.lower() == 'male':
        for voice in voices:
            if 'male' in voice.name.lower():
                selected_voice = voice
                break
        if not selected_voice:
            selected_voice = voices[0]
    elif gender.lower() == 'female':
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                selected_voice = voice
                break
        if not selected_voice:
            selected_voice = voices[1] if len(voices) > 1 else voices[0]

    engine.setProperty('voice', selected_voice.id)
    speak(f"Voice set to: {selected_voice.name}")

# Function to set the assistant's name
def set_assistant_name():
    global assistant_name
    speak("Please tell me what name you would like to give me.")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        assistant_name = recognizer.recognize_google(audio, language='en-in')
        speak(f"My name is now {assistant_name}.")
    except Exception:
        speak("Sorry, I didn't catch that. I'll use the default name.")
        assistant_name = "Assistant"

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
    except Exception:
        print("Sorry, I didn't catch that. Please say that again.")
        return None
    return query.lower()

# Function to answer general questions using WolframAlpha
def answer_general_questions(query):
    try:
        res = wolfram_client.query(query)
        answer = next(res.results, None)
        if answer:
            speak(answer.text)
        else:
            speak("I couldn't find an answer for that. Would you like to ask something else?")
    except Exception as e:
        print(f"Error: {e}")
        speak("There was an issue with fetching the answer. Please try again.")

# Main function to handle commands
def run_voice_assistant():
    speak(f"Hello! My name is {assistant_name}. How can I help you today?")

    while True:
        query = take_command()
        if query is None:
            continue

        # General Conversation
        if 'how are you' in query:
            speak("I'm an AI assistant, always ready to help you. How can I assist?")
        
        elif 'what is your name' in query or 'your name' in query:
            speak(f"My name is {assistant_name}. You can call me by this name.")

        elif 'who created you' in query:
            speak("I was created by a developer who loves to make intelligent systems.")

        elif 'thank you' in query:
            speak("You're welcome! I'm glad I could help.")

        elif 'how old are you' in query:
            speak("I'm as old as the code that runs me. I don't age like humans do!")

        elif 'what can you do' in query:
            speak("I can help you with playing music, telling jokes, providing information from Wikipedia, solving math problems, and answering general knowledge questions. You can ask me anything!")

        elif 'who is' in query or 'what is' in query or 'how does' in query or 'why' in query or 'calculate' in query:
            answer_general_questions(query)

        # Music and Media
        elif 'play' in query:
            song = query.replace('play', '')
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        # Current Time
        elif 'time' in query:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {current_time}")

        # Wikipedia Search
        elif 'search on wikipedia' in query:
            search_query = query.replace('search on wikipedia', '')
            speak(f"Searching Wikipedia for {search_query}")
            try:
                summary = wikipedia.summary(search_query, sentences=2)
                speak(summary)
            except Exception:
                speak("Sorry, I couldn't find any information on that.")

        # Telling a joke
        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        # Sending a WhatsApp message
        elif 'send whatsapp message' in query:
            speak("To whom do you want to send the message?")
            phone_number = input("Enter the phone number (with country code): ")
            speak("What is the message?")
            message = input("Enter your message: ")
            pywhatkit.sendwhatmsg(phone_number, message, datetime.datetime.now().hour, datetime.datetime.now().minute)
            speak("Message will be sent shortly.")

        # Exit Command
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a great day!")
            break

        # General Question Handler
        else:
            answer_general_questions(query)

if __name__ == "__main__":
    print("Select Voice Type:")
    print("1. Male")
    print("2. Female")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        set_voice('male')
    else:
        set_voice('female')

    set_assistant_name()
    run_voice_assistant()
