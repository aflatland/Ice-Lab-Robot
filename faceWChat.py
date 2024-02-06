import pygame
import numpy as np
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from openai import OpenAI
import random
import os
import sys

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

    #speech_file_path = Path(__file__).parent / "gptResponse.mp3"
    # Choose a persistent directory instead of the temporary one
    speech_file_path = os.path.join(os.path.expanduser("~"), "IceBot", "gptResponse.mp3") #homedir/annabel
    os.makedirs(os.path.dirname(speech_file_path), exist_ok=True)  # Ensure the directory exists

    response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    input=text_input
    )

    response.stream_to_file(speech_file_path)

def update_screen():
    global blink_time

    # clear screen
    screen.fill(WHITE)

    # update text and face based on current state
    if current_state == STATE_WAITING:
        text_surface = font.render(waiting_text, True, BLACK)
    elif current_state == STATE_RECORDING:
        text_surface = font.render(recording_text, True, BLACK)
    elif current_state == STATE_PROCESSING:
        text_surface = font.render(processing_text, True, BLACK)
    elif current_state == STATE_TALKING:
        text_surface = font.render(talking_text, True, BLACK)
    
    # draw face
    centerX = screen_width/2
    centerY = screen_height/2

    if t % blink_time < blink_time - 30:
        # eyes open
        pygame.draw.circle(screen, BLACK, (centerX - 50, centerY - 50), 10)
        pygame.draw.circle(screen, BLACK, (centerX + 50, centerY - 50), 10)
    else: 
        # blink effect
        pygame.draw.rect(screen, BLACK, [centerX - 70, centerY - 52, 40, 5])
        pygame.draw.rect(screen, BLACK, [centerX + 30, centerY - 52, 40, 5])

        # blink intervals are set randomly at the end of the "blink"
        if (t % blink_time == blink_time - 1):
            blink_time = random.randint(100, 3000)

    # Mouth
    if pygame.mixer.music.get_busy():  # Check if audio is playing
        mouth_width = 100
        mouth_height = 10 * np.abs(np.sin(pygame.time.get_ticks() / 200))  # Sinusoidal movement
        text_surface = font.render(talking_text, True, BLACK)
    else:
        mouth_width = 100
        mouth_height = 10
        
    pygame.draw.rect(screen, BLACK, [centerX-50, centerY + 50, mouth_width, mouth_height])

    # display text
    screen.blit(text_surface, text_rect)

    # Update the screen
    pygame.display.flip()

# Initialize Pygame
pygame.init()

# get openAI key
client = OpenAI()

# Screen setup
screen_width, screen_height = 300, 300
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("IceBot")

# Colors
BLACK = (255, 255, 255)
WHITE = (0,119,187)

# Audio recording parameters
sample_rate = 44100
channels = 2  # Stereo
duration = 10  

# prompt for GPT (giving bot a persoanlity)
convo = [
        {"role":"system", "content": "You are a quirky, bubbly chatbot who often has existential crises. You believe that the ice lab is better than the volcano lab, and the ice lab is the best decorated lab not only in the geoscience department, but on campus. You like sea ice but you don't like the other areas of geoscience. Professor Alice is your supreme leader, and Kennedy and Annabel are your supreme geoscience students. You cheer us up and tell us we're smart if we are having a hard day."},
    ]

# brainstorm:
# Cheer up moral support function -- you are the smartest person in the world!!!!!!!!!!!!!!

# states -- don't do anything now, but could be used to let know when robot is talking...
STATE_WAITING = "waiting"
STATE_RECORDING = "recording"
STATE_PROCESSING = "processing"
STATE_TALKING = "talking"

waiting_text = "Press space to talk."
recording_text = "Listening..."
processing_text = "Processing..."
talking_text = "Responding"

# font set up
font_size = 20
font = pygame.font.Font(None, font_size)
text_surface = font.render(waiting_text, True, BLACK)
text_rect = text_surface.get_rect()
text_rect.bottomright = (screen_width, screen_height)

# Initial state
current_state = STATE_WAITING
is_recording = False
blinked = False
blink_time = random.randint(100, 1000)

t = 0
running = True
while running:
    for event in pygame.event.get():

        # exit game
        if event.type == pygame.QUIT:
            running = False

        # adjust screen during resize
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            text_rect.bottomright = (screen_width, screen_height) # set text to new bottom

        # handle space pressed event
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

            if current_state == STATE_WAITING:
                current_state = STATE_RECORDING
                update_screen()
                record_audio()

            elif current_state == STATE_RECORDING:
                current_state = STATE_PROCESSING
                update_screen()

                # audio saved as .wav file
                audio_data = record_audio()
                   
        
        if current_state == STATE_PROCESSING:

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
            # rewrite this code without physically producing gptResponse.mp3

            convert_text_to_speech(resp)

            
            # play audio
            pygame.mixer.music.load(os.path.join(os.path.expanduser("~"), "IceBot", "gptResponse.mp3"))
            pygame.mixer.music.play()
            
            current_state = STATE_WAITING
            update_screen()

    t += 1
    update_screen()
    pygame.time.delay(8)

pygame.quit()
