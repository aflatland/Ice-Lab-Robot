import pygame
import numpy as np
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from openai import OpenAI
client = OpenAI()

# Initialize Pygame
pygame.init()

# Screen setup
screen_width, screen_height = 300, 300
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("IceBot")

# Colors
BLACK = (255, 255, 255)
WHITE = (0, 0, 0)

# font set up
font_size = 20
font = pygame.font.Font(None, font_size)
waiting_text = "Press space to talk..."
listening_text = "Listening..."
talking_text = "Responding..."
processing_text = "Processing..."
text_surface = font.render(waiting_text, True, BLACK)
text_rect = text_surface.get_rect()
text_rect.bottomright = (screen_width, screen_height)

# Audio recording parameters
sample_rate = 44100
channels = 2  # Stereo
duration = 10  

def record_audio():
    """Records audio until the space key is pressed again."""
    global is_recording, recording

    if not is_recording:
        print("Starting recording...")
        recording = sd.rec(int(sample_rate * duration), samplerate = sample_rate, channels=channels)
        is_recording = True
    else:
        print("Stopping recording...")
        sd.stop()
        is_recording = False
        print("Recording stopped.")
        return recording

    #print("Recording...")
   #recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=channels)
    #sd.wait()  # Wait until the recording is finished
    #print("Recording stopped.")
    #return recording

def get_response(chat):

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Specify the correct engine
        messages=chat,     # Ensure this matches the frontend structure
        max_tokens=100
    )

    resp = completion.choices[0].message.content

    return resp

def convert_text_to_speech(text_input):
    pygame.mixer.music.unload() # unload last gptResponse

    speech_file_path = Path(__file__).parent / "gptResponse.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    input=text_input
    )

    response.stream_to_file(speech_file_path)

convo = [
        {"role":"system", "content": "You are a quirky, bubbly chatbot who often has existential crises. You always answer in <3 sentences. You believe that the ice lab is better than the volcano lab, and the ice lab is the best decorated lab not only in the geoscience department, but on campus."},
    ]

# Next steps:
# -- get text to update correctly
# -- record stops when hit space again
# -- threading to avoid "not responding" message

is_recording = False

# states -- don't do anything now, but could be used to let know when robot is talking...
STATE_WAITING = "waiting"
STATE_RECORDING = "recording"
STATE_PROCESSING = "processing"
STATE_TALKING = "talking"

# Initial state
current_state = STATE_WAITING

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            text_rect.bottomright = (screen_width, screen_height) # move text to bottom
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                if not is_recording:
                    text_surface = font.render(listening_text, True, BLACK)
                    record_audio() # start recording
                else:
                    text_surface = font.render(processing_text, True, BLACK)
                    # audio saved as .wav file
                    audio_data = record_audio()
                    sf.write('output.wav',audio_data, sample_rate)
                    audio_file = open("output.wav", "rb")

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
                    pygame.mixer.music.load("gptResponse.mp3")
                    pygame.mixer.music.play()
                    # pygame.mixer.music.unload()

                    text_surface = font.render(waiting_text, True, BLACK)


    # Clear screen
    screen.fill(WHITE)

    # Draw face
    # Eyes
    centerX = screen_width/2
    centerY = screen_height/2

    pygame.draw.circle(screen, BLACK, (centerX - 50, centerY - 50), 10)
    pygame.draw.circle(screen, BLACK, (centerX + 50, centerY - 50), 10)

    # Mouth
    if pygame.mixer.music.get_busy():  # Check if audio is playing
        mouth_width = 100
        mouth_height = 10 * np.abs(np.sin(pygame.time.get_ticks() / 200))  # Sinusoidal movement
        text_surface = font.render(talking_text, True, BLACK)
    else:
        mouth_width = 100
        mouth_height = 10
        

    pygame.draw.rect(screen, BLACK, [centerX-50, centerY + 50, mouth_width, mouth_height])

    # Display text
    screen.blit(text_surface, text_rect)

    # Update the screen
    pygame.display.flip()
    pygame.time.delay(8)

pygame.quit()
