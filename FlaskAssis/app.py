from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Speed of speech

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Speech recognition function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Helps reduce background noise
        audio = recognizer.listen(source)
        print("Got audio, now recognizing...")
        try:
            command = recognizer.recognize_google(audio)
            print(f"Recognized: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")
            return None

# Assistant functionality
def process_command(command):
    if 'play' in command:
        song = command.replace('play', '').strip()
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)
        return f"Playing {song} on YouTube."

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"Current time is {current_time}")
        return f"Current time is {current_time}."

    elif 'who is' in command or 'what is' in command:
        query = command.replace('who is', '').replace('what is', '').strip()
        try:
            info = wikipedia.summary(query, sentences=2)
            speak(info)
            return info
        except wikipedia.exceptions.DisambiguationError:
            return "There are multiple results. Please be more specific."
        except wikipedia.exceptions.PageError:
            return "Sorry, I couldn't find any information."

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)
        return joke

    else:
        return "I'm not sure how to help with that."

# Flask route to handle voice commands from text input
@app.route('/voice_command', methods=['POST'])
def voice_command():
    data = request.json
    if 'command' in data:
        command = data['command']
        response = process_command(command)
        return jsonify({"response": response})
    else:
        return jsonify({"error": "No command provided."}), 400

# Flask route to handle speech recognition
@app.route('/recognize', methods=['GET'])
def recognize():
    command = recognize_speech()
    if command:
        response = process_command(command)
        return jsonify({"response": response})
    else:
        return jsonify({"response": "No command recognized or understood."})

# Route for the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
