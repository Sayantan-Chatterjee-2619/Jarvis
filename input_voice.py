import speech_recognition as sr
import os
import threading
from mtranslate import translate
from colorama import Fore,Style,init
from output_voice import translate_en_to_hi

init(autoreset=True)

def print_loop():
    while True:
        print(Fore.GREEN + "Listening...", end="", flush=True)
        print(Style.RESET_ALL, end="",flush=True)

def translate_hi_to_en(text):
    en_text=translate(text, "en-us")
    return en_text

def Speech_to_text_py():
    recognizer= sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 34000
    recognizer.dynamic_energy_adjustment_damping = 0.010
    recognizer.dynamic_energy_ratio = 1.0
    recognizer.pause_threshold= 0.9
    recognizer.operation_timeout=None
    recognizer.pause_threshold=0.5
    recognizer.non_speaking_duration=0.5

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            print(Fore.GREEN + "Listening...", end="", flush=True)
            try:
                audio = recognizer.listen(source, timeout=None)
                print("\r" + Fore.CYAN + "Recognizing...", end="", flush=True)
                recognized_text=recognizer.recognize_google(audio).lower()
                if recognized_text:
                    text_output= translate_hi_to_en(str(recognized_text))
                    translate_en_to_hi(text_output)
                    print("\r" + Fore.LIGHTBLUE_EX + text_output)
                    return text_output
                else:
                    return ""
            except sr.UnknownValueError:
                recognized_text="Sorry! Not recognized"
            finally:
                print("\r", end="", flush=True)
            
            os.system("cls" if os.name == "jv" else "clear")
        
        stt_thread=threading.Thread(target=Speech_to_text_py)
        print_thread=threading.Thread(target=print_loop)
        stt_thread.start()
        stt_thread.join()
        print_loop.join()
        
    

def input_voice():
    Speech_to_text_py()
