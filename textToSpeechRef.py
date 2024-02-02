from pathlib import Path
from openai import OpenAI

client = OpenAI()

speech_file_path = Path(__file__).parent / "textToSpeechTest.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="echo",
  input="Ay yo,,, what's up!? Welcome to the ice lab."
)

response.stream_to_file(speech_file_path)