import os
import random

import playsound
import yaml
import pygetwindow as gw
from pywinauto import Desktop
import psutil
import subprocess

def get_activate_window():
    active_window = gw.getActiveWindow()
    handle = active_window._hWnd
    window = Desktop(backend="win32").window(handle=handle)
    process_id = window.process_id()
    process = psutil.Process(process_id)
    process_name = process.name()

    return process_name

def replace_word(text):
    words = [
        'jarvis',
        'please'
    ]
    for i in words:
        text = text.replace(i, "")
    return text.strip()

def main(text, system):
    activate_window = get_activate_window()
    folder = f"{os.getcwd()}/commands/".replace("\\", "/")
    print(text)
    try:
        with open(f"{folder}/{activate_window}/main.yaml", "r+", encoding="utf8") as f:
            main = yaml.safe_load(f)
            for i in main['list']:
                for j in i['phrases']:
                    if j in text:
                        subprocess.Popen([f"{folder}/{activate_window}/{i['command']}", i['arg']], shell=True)
                        playsound.playsound(f"./sounds/{j['voice'][random.randint(0, len(j['voice'])-1)]}")
                        return

    except Exception as ex: print(78, ex)

    for i in os.listdir(folder):
        try:
            with open(f"{folder}{i}/main.yaml", "r+", encoding="utf8") as f:
                main = yaml.safe_load(f)
                for n in main['list']:
                    for j in n['phrases']:
                        if j in text:
                            subprocess.Popen([f"{folder}{i}/{n['command']}", *n['arg']], shell=True)
                            playsound.playsound(f"./sounds/{j['voice'][random.randint(0, len(j['voice'])-1)]}")
                            return

        except Exception as ex: print(91, ex)





            # sound_file = f"./sounds/{main['audio'][random.randint(0, len(main['audio'])-1)]}"
            # playsound.playsound(sound_file)
