from RealtimeSTT import AudioToTextRecorder
from colorama import Fore, Back, Style
import colorama
import os
import socket
import requests

if __name__ == '__main__':

    print("Initializing RealtimeSTT test...")

    colorama.init()

    full_sentences = []
    displayed_text = ""

    def clear_console():
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def send_rosstalk(ip, port, message):
        # Add /r/n to the message to comply with the specified format
        message += '\r\n'
        
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the server
            s.connect((ip, port))
            
            # Send the message
            s.sendall(message.encode())

    def send_text(text, url="http://10.10.80.101:3000/transcript"):
        payload = {'text': text}

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print("Text sent successfully.")
                return response.json()
            else:
                print(f"Failed to send text. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred.{e}")

    def text_detected(text):
        global displayed_text
        #send_rosstalk('10.10.80.101', 7795, text)
        sentences_with_style = [
            f"{Fore.YELLOW + sentence + Style.RESET_ALL if i % 2 == 0 else Fore.CYAN + sentence + Style.RESET_ALL} "
            for i, sentence in enumerate(full_sentences)
        ]
        new_text = "".join(sentences_with_style).strip() + " " + text if len(sentences_with_style) > 0 else text

        if new_text != displayed_text:
            displayed_text = new_text
            clear_console()
            print(displayed_text, end="", flush=True)

    # def text_detected(text):
    #     global displayed_text
    #     clear_console()
    #     print(text)
        # sentences_with_style = [
        #     f"{Fore.YELLOW + sentence + Style.RESET_ALL if i % 2 == 0 else Fore.CYAN + sentence + Style.RESET_ALL} "
        #     for i, sentence in enumerate(full_sentences)
        # ]
        # new_text = "".join(sentences_with_style).strip() + " " + text if len(sentences_with_style) > 0 else text

        # if new_text != displayed_text:
        #     displayed_text = new_text
        #     clear_console()
        #     print(displayed_text, end="", flush=True)

    def process_text(text):
        full_sentences.append(text)
        #send_rosstalk("10.10.80.101", 7795, text)
        send_text(text)
        text_detected("")

    recorder_config = {
        'spinner': False,
        'model': 'large-v2',
        'language': 'en',
        'silero_sensitivity': 0.4,
        'webrtc_sensitivity': 2,
        'post_speech_silence_duration': 0.1,
        'min_length_of_recording': 0,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0.1,
        'realtime_model_type': 'distil-medium.en',
        'on_realtime_transcription_update': text_detected, 
        #'on_realtime_transcription_stabilized': text_detected,
    }

    recorder = AudioToTextRecorder(**recorder_config)

    clear_console()
    print("Say something...", end="", flush=True)

    while True:
        recorder.text(process_text)