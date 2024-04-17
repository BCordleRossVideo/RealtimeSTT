from RealtimeSTT import AudioToTextRecorder
from colorama import Fore, Back, Style
import colorama # type: ignore
import os
import socket
import requests # type: ignore
import asyncio
import websockets
import json

if __name__ == '__main__':

    print("Initializing RealtimeSTT test...")

    colorama.init()

    full_sentences = []
    displayed_text = ""
    initial_prompt = "Ready 1, take 1. ready 2, take 2. Ready XPression 1, Take XPression 1. Take. Ready 3, effect 3. Ready 16, take 16. Preview 4. Take 4. Standby font. Font in. Ready 99, dissolve. Ready blue, take blue. Ready red, take red. Ready X, roll X, dissolve. Ready Y, roll Y, dissolve. XPression. Ross Carbonite. Ross Video."

    def clear_console():
        os.system('clear' if os.name == 'posix' else 'cls')
    
    # def send_rosstalk(ip, port, message):
    #     # Add /r/n to the message to comply with the specified format
    #     message += '\r\n'
        
    #     # Create a socket object
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #         # Connect to the server
    #         s.connect((ip, port))
            
    #         # Send the message
    #         s.sendall(message.encode())

    async def send_text_via_websocket(text, uri="ws://10.10.80.101:3000"):
        try:
            async with websockets.connect(uri) as websocket:
                payload = json.dumps({'text': text})
                await websocket.send(payload)
                response = await websocket.recv()
                print(f"Response from server: {response}", flush=True)
        except (websockets.exceptions.WebSocketException, OSError) as e:
            print(f"An error occurred while sending text via websocket: {e}", flush=True)


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
            print(displayed_text, flush=True)


    def process_text(text):
        asyncio.run(send_text_via_websocket(text))
        #send_text(text)
        full_sentences.append(text)
        #send_rosstalk("10.10.80.101", 7795, text)
        text_detected("")

    recorder_config = {
        'spinner': False,
        'model': 'tiny.en',
        'language': 'en',
        'silero_sensitivity': 0.4,
        'silero_use_onnx': True,
        'webrtc_sensitivity': 2,
        'post_speech_silence_duration': 0,
        'min_length_of_recording': 0,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0,
        'realtime_model_type': 'tiny.en',
        'on_realtime_transcription_update': text_detected,
        'level' : 'WARNING',
        'debug_mode': False,
        'beam_size_realtime': 3,
        'initial_prompt': initial_prompt,
        # 'suppress_tokens': [-1],
        #'on_realtime_transcription_stabilized': text_detected,
    }

    recorder = AudioToTextRecorder(**recorder_config)

    clear_console()
    print("Say something...", end="", flush=True)

    while True:
        recorder.text(process_text)