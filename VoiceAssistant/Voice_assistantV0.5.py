import re
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import wolframalpha  # Import WolframAlpha for mathematical operations

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

# Global variable for assistant's name
assistant_name = "Assistant"

# WolframAlpha API setup
client = wolframalpha.Client('GQL8WE-P9J2HLJ39Q')  # Replace with your WolframAlpha API Key

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to set the voice type (male or female)
def set_voice(gender='female'):
    voices = engine.getProperty('voices')
    selected_voice = None

    for voice in voices:
        if gender.lower() in voice.name.lower():
            selected_voice = voice
            break

    if not selected_voice:
        # Default to second voice (usually female)
        selected_voice = voices[1]
    
    engine.setProperty('voice', selected_voice.id)
    speak(f"Voice set to: {selected_voice.name}")

# Function to set the assistant's name
def set_assistant_name():
    global assistant_name
    speak("Please tell me what name you would like to give me.")
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            audio = recognizer.listen(source, timeout=5)  # Add timeout
            assistant_name = recognizer.recognize_google(audio, language='en-in')
            speak(f"My name is now {assistant_name}.")
        except sr.WaitTimeoutError:
            speak("Sorry, I didn't hear anything. I'll use the default name.")
        except Exception:
            speak("Sorry, I didn't catch that. I'll use the default name.")
        assistant_name = assistant_name or "Assistant"

# Function to take voice input from the user
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source)  # Handle background noise
        try:
            audio = recognizer.listen(source, timeout=5)  # Add timeout
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
        except sr.WaitTimeoutError:
            print("Timeout, didn't hear anything.")
            return None
        except Exception:
            print("Sorry, I didn't catch that. Please say that again.")
            return None
    return query.lower()

# Function to handle WolframAlpha queries for math operations
def calculate_math(query):
    try:
        # Check if it's a basic math operation like '500 + 500'
        math_pattern = r'(\d+)\s*(\+|\-|\*|\/)\s*(\d+)'  # Regex for basic operations
        match = re.search(math_pattern, query)
        
        if match:
            num1, operator, num2 = match.groups()
            formatted_query = f"{num1} {operator} {num2}"
            print(f"Formatted Query for WolframAlpha: {formatted_query}")  # Debug output
            res = client.query(formatted_query)
            answer = next(res.results).text  # Fetching the result from WolframAlpha
            print(f"Answer from WolframAlpha: {answer}")  # Debug output
            speak(f"The result is {answer}")
        else:
            # Handle more complex math queries like factorials
            if 'factorial' in query:
                query = query.replace("factorial", "!")  # WolframAlpha uses "!" for factorial
            elif 'square' in query:
                query = query.replace("square", "^2")  # Replace square with exponentiation

            # Replace common math words with symbols
            query = query.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divide", "/")
            
            print(f"Formatted Query for WolframAlpha: {query}")  # Debug output
            res = client.query(query)
            answer = next(res.results).text  # Fetching the result from WolframAlpha
            print(f"Answer from WolframAlpha: {answer}")  # Debug output
            speak(f"The result is {answer}")
    except Exception as e:
        print(f"Error occurred: {e}")  # Debug output
        speak("Sorry, I couldn't understand the math operation.")

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

        elif 'thank you' in query:
            speak("You're welcome! I'm glad I could help.")

        elif 'how old are you' in query:
            speak("I'm as old as the code that runs me. I don't age like humans do!")

        elif 'what can you do' in query:
            speak("I can help you with playing music, telling jokes, providing information from Wikipedia, solving math problems, and answering general knowledge questions. You can ask me anything!")

        # Handle basic math operations using WolframAlpha
        elif 'calculate' in query or 'math' in query or 'plus' in query or 'minus' in query or 'times' in query or 'divide' in query:
            calculate_math(query)

        # Music and Media
        elif 'play' in query:
            song = query.replace('play', '').strip()
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        # Current Time
        elif 'time' in query:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {current_time}")

        # Wikipedia Search
        elif 'search on wikipedia' in query or 'who is' in query or 'what is' in query:
            search_query = query.replace('search on wikipedia', '').replace('who is', '').replace('what is', '').strip()
            speak(f"Searching Wikipedia for {search_query}")
            try:
                summary = wikipedia.summary(search_query, sentences=2)
                speak(summary)
            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"Which one did you mean? {e.options[:3]}")  # Show up to 3 options
            except Exception:
                speak("Sorry, I couldn't find any information on that.")

        # Telling a joke
        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        # Exit Command
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a great day!")
            break

        else:
            speak("Sorry, I didn't understand that. Can you please repeat?")

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
