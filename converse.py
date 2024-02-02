import sounddevice as sd
import keyboard
import numpy as np
import soundfile as sf
import io
from pathlib import Path
import winsound
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
client = OpenAI()

# Audio recording parameters
sample_rate = 44100
channels = 2  # Stereo
duration = 10  

def record_audio():
    """Records audio until the space key is pressed again."""
    print("Press space to start recording.")
    keyboard.wait('space')
    print("Recording... Press space to stop.")
    
    recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=channels)
    sd.wait()  # Wait until the recording is finished
    print("Recording stopped.")
    return recording

def get_response(chat):

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
    input=text_input
    )

    response.stream_to_file(speech_file_path)


def main():

    convo = [
        {"role":"system", "content": "You are a quirky, bubbly chatbot who often has existential crises. You always answer in <3 sentences. You believe that the ice lab is better than the volcano lab, and the ice lab is the best decorated lab not only in the geoscience department, but on campus."},
    ]

    while(True):

        # audio saved as .wav file
        audio_data = record_audio()
        sf.write('output.wav',audio_data, sample_rate)
        audio_file= open("output.wav", "rb")

        # text extracted from .wav file
        transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format="json"
        )
    
        print("USER-INPUT: " + transcript.text) # JSON: transcript.text gets the text
        convo.append({"role":"user", "content":transcript.text})

        print(convo)

        # ask chatgpt question 
        resp = get_response(convo)
        print("GPT-RESPONSE: " + resp)
        convo.append({"role":"assistant", "content":resp})

        # convert response to audio
        convert_text_to_speech(resp)

    
        # play audio
        audio = AudioSegment.from_mp3("gptResponse.mp3")
        play(audio)




if __name__ == "__main__":
    main()
 