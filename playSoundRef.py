from pydub import AudioSegment
from pydub.playback import play


# Load your MP3 file
audio = AudioSegment.from_mp3("gptResponse.mp3")
play(audio)

#playsound('gptResponseConverted.wav')