from RealtimeSTT import AudioToTextRecorder
from colorama import Fore, Back, Style
import colorama # type: ignore
import os
import socket
import requests # type: ignore
import asyncio
import websockets
import json
import torch

if __name__ == '__main__':

    print("Initializing RealtimeSTT test...")

    colorama.init()

    full_sentences = []
    displayed_text = ""
    #initial_prompt = "path to 270. road to 270. top 5 closest races. race to 270. 5 closest races. vote margin. outstanding vote. vote difference. vote difference for Alabama. vote margin for Alabama. vote difference for Alaska. vote margin for Georgia. vote difference for Georgia. outstanding vote for Wisconsin. outstanding vote for Michigan. outstanding vote for Georgia. vote difference for Michigan. vote margin for Michigan.vote difference for Arizona. vote margin for Arizona. outstanding vote for Pennsylvania."
    initial_prompt = "Arizona. Maricopa. Pima. Pinal. Coconino. Georgia. Fulton. Gwinnett. DeKalb. Taliaferro. Michigan. Wayne. Oakland. Macomb. Keweenaw. Minnesota. Hennepin. Ramsey. Mahnomen. Nevada. Clark. Washoe. North Carolina. Mecklenburg. Guilford. Tyrrell. Pennsylvania. Philadelphia. Allegheny. Montgomery. Wisconsin. Milwaukee. Waukesha. Menominee. Vote Difference. Vote Margin. Outstanding Vote. Top Five Closest Races. Race to two-seventy. Path to 270. Election data in US States & Counties."

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

    async def send_text_via_websocket(text, uri="ws://localhost:3000"):
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
        'silero_sensitivity': 0.3,
        'silero_use_onnx': True,
        'webrtc_sensitivity': 3,
        'post_speech_silence_duration': 0.1,
        'min_length_of_recording': 0,
        'min_gap_between_recordings': 0.1,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0.1,
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
    if torch.cuda.is_available():
        print("GPU is available.")
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        print(f"CUDA version: {torch.version.cuda}")
        print(f"cuDNN version: {torch.backends.cudnn.version()}")
        print(f"GPU device name: {torch.cuda.get_device_name(0)}")
    else:
        print("GPU is NOT available.")
    print("Say something...", end="", flush=True)

    while True:
        recorder.text(process_text)