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
    initial_prompt = "preview camera 1. preview camera 1?. take camera 1. preview camera 2. ready to?. ready too.. standby to?. set to?. preview to?. ready to.. standby to.. set to. preview to. take camera 2. take to?. switch to?. cut to?. preview camera 3. take camera 3. ready split. standby split. set split. preview split. readysplit. pretty split. preview 2-box. take split. go split. takesplit. take camera 2-box. ready black. standby black. set black. preview black. black on the line. take black. take.. cut.. take it. cut it. take!. fade.. dissolve.. fade it. fade up. fade to black. with font. ready font 1. ready xpression 1. font in. xpression in. graphic in. lower third in. expression in. fawn in. fun in. fontin. font out. clear font. xpression out. expression out. clear expression. graphic out. clear it. fawn out. clearfont. fun out. ready me. take me. show me the multiviewer. multiviewer full screen. multiviewer fullscreen. show me the multi viewer. show me the multi-viewer. bring me back fullscreen.. bring me back full screen. route me full screen. bring me full screen. bring me fullscreen. dashboard fullscreen. dashboard full screen. on an effect. set effect. ready effect. take effect.. do it.. effect it. 2-box with 1 left 2 right. camera 2 on the right. 2-box 1 left to right. 2-box 1 left 2 right. 2-box with 1 left to right. 2-box with 1 left to right. split with 1 left 2 right. split with 1 left to right. 2-box with 1 left 3 right. 2-box 1 left 3 right. split with 1 left 3 right. take."

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

    async def send_text_via_websocket(text, uri="ws://127.0.0.1:3000"):
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
        'webrtc_sensitivity': 3,
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