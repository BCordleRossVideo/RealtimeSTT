import pyaudio

def list_microphones():
    p = pyaudio.PyAudio()
    print("Available audio input devices:")

    input_devices = []
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if dev_info['maxInputChannels'] > 0:
            input_devices.append(dev_info)
            print(f"{i}: {dev_info['name']}")

    if not input_devices:
        print("No audio input devices found.")

    p.terminate()

if __name__ == "__main__":
    list_microphones()
