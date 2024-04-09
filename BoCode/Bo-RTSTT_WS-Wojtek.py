from RealtimeSTT import AudioToTextRecorder
import colorama  # type: ignore
import os
import asyncio
import websockets
import json

# Initialize colorama
colorama.init()

# Globals
full_sentences = []
displayed_text = ""
websocket_connection = None  # Global variable to store the WebSocket connection

async def manage_websocket_connection(uri="ws://10.10.80.101:3000"):
    """
    Coroutine to manage WebSocket connection.
    Keeps the connection open and listens for server messages.
    """
    global websocket_connection
    async with websockets.connect(uri) as websocket:
        websocket_connection = websocket
        while True:
            # Wait indefinitely, you can modify this part to listen for incoming messages if necessary
            await asyncio.sleep(10)  # Keep the connection alive

async def send_text_via_websocket(text):
    """
    Sends text to the server via an open WebSocket connection.
    """
    global websocket_connection
    if websocket_connection:
        payload = json.dumps({'text': text})
        await websocket_connection.send(payload)
        response = await websocket_connection.recv()
        print(f"Response from server: {response}", flush=True)
    else:
        print("WebSocket connection is not established.")

def clear_console():
    """
    Clears the console.
    """
    os.system('clear' if os.name == 'posix' else 'cls')

def text_detected(text):
    """
    Handles detected text: formats it, prints it, and sends it over WebSocket.
    """
    global displayed_text, full_sentences
    sentences_with_style = [
        f"{colorama.Fore.YELLOW + sentence + colorama.Style.RESET_ALL if i % 2 == 0 else colorama.Fore.CYAN + sentence + colorama.Style.RESET_ALL} "
        for i, sentence in enumerate(full_sentences)
    ]
    new_text = "".join(sentences_with_style).strip() + " " + text if len(sentences_with_style) > 0 else text

    if new_text != displayed_text:
        displayed_text = new_text
        clear_console()
        print(displayed_text, flush=True)
        asyncio.run_coroutine_threadsafe(send_text_via_websocket(new_text), asyncio.get_event_loop())

def process_text(text):
    """
    Processes detected text: sends it over WebSocket and updates the UI.
    """
    full_sentences.append(text)
    text_detected(text)

if __name__ == '__main__':
    clear_console()
    print("Initializing RealtimeSTT test...")
    print("Say something...", end="", flush=True)

    recorder_config = {
        'spinner': False,
        'model': 'distil-medium.en',
        'language': 'en',
        'silero_sensitivity': 0.4,
        'silero_use_onnx': True,
        'webrtc_sensitivity': 2,
        'post_speech_silence_duration': 0,
        'min_length_of_recording': 0,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0,
        'realtime_model_type': 'distil-small.en',
        'on_realtime_transcription_update': process_text,
        'level': 'WARNING'
    }

    recorder = AudioToTextRecorder(**recorder_config)

    # Start the WebSocket connection manager in the background
    loop = asyncio.get_event_loop()
    loop.run_until_complete(manage_websocket_connection())

    try:
        # Assuming the recorder starts its own loop or blocking process
        while True:
            # Your audio processing loop or a blocking call to start recording
            pass
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

