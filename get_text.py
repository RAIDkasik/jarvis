from pvrecorder import PvRecorder
import playsound
import speech_recognition as sr
import commands
import random
import requests
import vosk
import sys
import sounddevice as sd
import queue
import json
import platform

model = vosk.Model("model_small")
samplerate = 16000
device = 1

system = platform.system()
q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def translate_text(text, source_language='ru', target_language='en'):
    url = 'https://translate.googleapis.com/translate_a/single'
    params = {
        'client': 'gtx',
        'sl': source_language,
        'tl': target_language,
        'dt': 't',
        'q': text
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        translation = response.json()[0][0][0]
        return translation
    else:
        print("Translation failed. Status code:", response.status_code)
        return None

def selected_device():
    recorder = PvRecorder(device_index=0, frame_length=2)
    recorder.start()
    selected_device = recorder.selected_device
    recorder.stop()

    return selected_device

def main():
    yes_sir = ["greet1.wav", "greet2.wav"]
    with sd.RawInputStream(samplerate=samplerate, blocksize=2000, device=device, dtype='int16', channels=1, callback=q_callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result())["text"]
                print(text)
                if "джарвис" in text or "джервис" in text:
                    print("Yes, sir!")
                    playsound.playsound(f"./sounds/{yes_sir[random.randint(0, len(yes_sir)-1)]}")

                    recognizer = sr.Recognizer()
                    microphone = sr.Microphone()

                    recognizer.pause_threshold = 0.3
                    recognizer.non_speaking_duration = 0.3

                    for i in range(100):
                        with microphone as source:
                            try: audio = recognizer.listen(source, timeout=0.3)
                            except sr.WaitTimeoutError: continue

                        try:
                            text = recognizer.recognize_google(audio, language="ru-RU").lower()
                            print(text)
                            commands.main(text, system.lower())
                        except Exception as ex: print(ex)


