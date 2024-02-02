from openai import OpenAI
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play

client = OpenAI()

def get_response(inputText):

    chat = [
        {"role":"system", "content": "You are a friendly chat bot. Answer in <4 sentences."},
        {"role":"user", "content":inputText}
    ]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Specify the correct engine
        messages=chat,     # Ensure this matches the frontend structure
        max_tokens=100
    )

    resp = completion.choices[0].message.content

    return resp

def convert_text_to_speech(text_input):
    speech_file_path = Path(__file__).parent / "gptResponse.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    input=text_input,
    )

    response.stream_to_file(speech_file_path)


def main():

    # ask chatgpt question 
    resp = get_response("Tell me a story...")

    print(resp)

    #convert_text_to_speech(resp)

    #audio = AudioSegment.from_mp3("gptResponse.mp3")
    #play(audio)





if __name__ == "__main__":
    main()

