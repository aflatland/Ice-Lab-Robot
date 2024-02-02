import sounddevice as sd
import keyboard
import numpy as np
import soundfile as sf
import io

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

def main():
    audio_data = record_audio()

    

    
    # Save the audio data to a file
    sf.write('output.wav', audio_data, sample_rate)
    print("Audio saved to 'output.wav'.")

if __name__ == "__main__":
    main()
 