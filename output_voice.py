import pygame
import os
import threading
import asyncio
from mtranslate import translate
from input_voice import Speech_to_text_py

import edge_tts

VOICE = "hi-IN-MadhurNeural"
BUFFER_SIZE=1024

def remove_file(file_path):
    attempts=0
    try:
        with open(file_path, "wb") as f:
            pass
            os.remove(file_path)
            
    except Exception as e:
        attempts += 1
        print(f"Error removing file: {e}")


async def amain(TEXT,output_file) -> None:
    try:
        communicate = edge_tts.Communicate(TEXT, VOICE)
        await communicate.save(output_file)
    except Exception as e:
        print(e)

def play_audio(file_path):
    try:
        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound(file_path)
        sound.play()

        # Wait for audio to finish playing
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)

        pygame.quit()
    except Exception as e:
        print(f"Error playing audio: {e}")


def translate_en_to_hi(text):
    hi_text=translate(text, "hi")
    speak(hi_text)
    return hi_text



def speak(text, output_file=None):

    if output_file is None:
        output_file = os.path.join(os.getcwd(), "speech.mp3")

        # Generate speech
        asyncio.run(amain(text, output_file))

    # Play audio in a separate thread
    thread = threading.Thread(target=play_audio, args=(output_file,))
    thread.start()
    thread.join()

    Speech_to_text_py()

