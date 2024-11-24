import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import random
import html

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

# Function to recognize user's voice input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the recognition service.")
        return ""

# Function to fetch quiz questions from OpenTDB API
def fetch_quiz_questions(amount=5):
    url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"
    try:
        response = requests.get(url)
        data = response.json()
        questions = data.get("results", [])
        return questions
    except Exception as e:
        print(f"Error fetching quiz questions: {e}")
        return []

# Function to start the quiz
def start_quiz():
    score = 0
    questions = fetch_quiz_questions()

    if not questions:
        speak("I couldn't fetch quiz questions from the internet. Please try again later.")
        return

    speak("Let's start the quiz! I will ask you some general knowledge questions.")
    
    for q in questions:
        question = html.unescape(q["question"])
        correct_answer = html.unescape(q["correct_answer"])
        options = [html.unescape(opt) for opt in q["incorrect_answers"]] + [correct_answer]
        random.shuffle(options)
        
        # Asking the question
        speak(question)
        speak("Your options are:")
        for i, option in enumerate(options, start=1):
            speak(f"Option {i}: {option}")

        user_answer = listen()

        # Check the answer
        if user_answer and any(str(i) in user_answer for i in range(1, 5)):
            user_index = int(user_answer.split()[-1]) - 1
            selected_answer = options[user_index] if user_index < len(options) else ""

            if selected_answer.lower() == correct_answer.lower():
                speak("Correct answer!")
                score += 1
            else:
                speak(f"Wrong answer. The correct answer is {correct_answer}.")
        else:
            speak(f"No valid answer provided. The correct answer was {correct_answer}.")

        # Providing additional information using Wikipedia
        speak("Would you like to know more about it?")
        response = listen()
        if "yes" in response:
            try:
                wiki_summary = wikipedia.summary(correct_answer, sentences=2)
                speak(wiki_summary)
            except wikipedia.exceptions.DisambiguationError:
                speak("The topic is too ambiguous to provide more information.")
            except Exception:
                speak("I couldn't fetch information from Wikipedia at the moment.")

        # Play related videos using pywhatkit
        speak("Shall I play a related video on YouTube?")
        response = listen()
        if "yes" in response:
            pywhatkit.playonyt(correct_answer)

    speak(f"Quiz completed! Your score is {score} out of {len(questions)}.")

    # Ending with a joke
    speak("Would you like to hear a joke?")
    response = listen()
    if "yes" in response:
        joke = pyjokes.get_joke()
        speak(joke)

# Function to provide the current time
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

# Main function to handle user commands
def main():
    speak("Hello! Welcome to the Voice-Based Educational Quiz App.")
    speak("Please tell me your name.")
    
    user_name = listen()
    if user_name:
        speak(f"Hello {user_name}, how can I assist you today?")
    
    while True:
        speak("You can ask me to start a quiz, tell the current time, or entertain you with a joke.")
        command = listen()
        
        if "quiz" in command:
            start_quiz()
        
        elif "time" in command:
            tell_time()
        
        elif "joke" in command:
            joke = pyjokes.get_joke()
            speak(joke)
        
        elif "exit" in command or "stop" in command:
            speak(f"Goodbye {user_name}, have a great day!")
            break
        
        else:
            speak("I didn't understand that. Please try again.")

if __name__ == "__main__":
    main()
