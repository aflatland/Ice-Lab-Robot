import speech_recognition as sr
from openai import OpenAI
client = OpenAI()

# init recognizer
recognizer = sr.Recognizer()

# get audio input
def listen():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            return text
        except Exception as e:
            error_message = str(e)
            return "Error recognizing speech: " + error_message
        

def main():
    while True:
        print("Listening...")
        question = listen()
        print(f"You said: {question}")
        if question.lower() == "stop":
            break

if __name__ == "__main__":
    main()