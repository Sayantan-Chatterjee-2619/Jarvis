import speech_recognition as sr
import os
import threading
import sys
from mtranslate import translate
from colorama import Fore,Style,init
from output_voice import translate_en_to_hi

init(autoreset=True)

stop_listening = threading.Event()

def clear_terminal():
    # ANSI escape code to clear screen and move cursor to top-left
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

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
        while not stop_listening.is_set():   # check stop flag
            print(Fore.GREEN + "Listening..." + Style.RESET_ALL, end="", flush=True)
            try:
                audio = recognizer.listen(source, timeout=None)
                print("\r" + Fore.CYAN + "Recognizing..." + Style.RESET_ALL, end="", flush=True)
                recognized_text = recognizer.recognize_google(audio).lower()
                if recognized_text:
                    if recognized_text.strip() == "exit":
                        print("\r" + Fore.RED + "Exit command detected. Stopping..." + Style.RESET_ALL)
                        stop_listening.set()   # signal stop
                        break
                    text_output = translate_hi_to_en(recognized_text)
                    translate_en_to_hi(text_output)
                    print("\r" + Fore.LIGHTBLUE_EX + text_output + Style.RESET_ALL)
                    clear_terminal()
                else:
                    print("\rNo speech detected.")
            except sr.UnknownValueError:
                print("\rSorry! Not recognized")
            finally:
                clear_terminal()
        
            stt_thread=threading.Thread(target=Speech_to_text_py)
            stt_thread.start()
            stt_thread.join()
        
    


