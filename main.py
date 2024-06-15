import asyncio
import platform
import eel
import sqlite3
import playsound
import psutil
import yaml
import get_text
import os
import subprocess

eel.init('web', allowed_extensions=['.html', ".css"])

@eel.expose
def selected_device():
    try:
        res = get_text.selected_device()
        return res
    except Exception as e:
        print("Error:", e)

@eel.expose
def create_commands(name, type, path, com):
    com = com.split(", ")
    path = path.split(", ")
    system = platform.system().lower()
    print("ok")
    with open("./commands/all/main.yaml", "r", encoding="utf8") as f:
        data = yaml.safe_load(f)
        cmd = "ahk/start.exe" if type=="program" else "ahk/main.exe"
        try:
            data['list'].append(
                {
                    "name": name,
                    "command": cmd,
                    "voice": [''],
                    "phrases": com,
                    "arg": path
                }
            )
        except:
            data = {"list": []}
            data['list'].append(
                {
                    "name": name,
                    "command": cmd,
                    "voice": [''],
                    "phrases": com,
                    "arg": path
                }
            )
    with open("./commands/all/main.yaml", "w", encoding="utf8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    playsound.playsound("./sounds/ok3.wav")

@eel.expose
def os_listdir():
    try:
        data = []
        for i in os.listdir("./commands"):
            with open(f"./commands/{i}/main.yaml", "r+", encoding="utf8") as f:
                for j in yaml.safe_load(f)['list']:
                    data.append(f"{i} / {j['name']}")
        eel.handleData(data)
    except Exception as e:
        print("Error:", e)

@eel.expose
def delete_command(com):
    path, name = com.split(" / ")
    with open(f"./commands/{path}/main.yaml", "r+", encoding="utf8") as f:
        data = yaml.safe_load(f)
        for i in range(len(data['list'])):
            if data['list'][i]['name'] == name:
                data['list'].pop(i)
    with open(f"./commands/{path}/main.yaml", "w+", encoding="utf8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    playsound.playsound("./sounds/ok3.wav")

@eel.expose
def add_auto_start(path, name):
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    name=name.replace(" ", "_")
    cursor.execute(f"INSERT INTO auto_start ('path', 'name') VALUES ('{path}', '{name}')")
    db.commit()
    playsound.playsound("./sounds/ok3.wav")

@eel.expose
def del_auto_start(name):
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM auto_start WHERE name='{name}'")
    db.commit()
    playsound.playsound("./sounds/ok3.wav")

@eel.expose
def auto_start():
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    data = cursor.execute(f"SELECT * FROM auto_start").fetchall()
    eel.del_auto(data)

@eel.expose
def settings():
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    settings = {}
    data = cursor.execute(f"SELECT * FROM settings").fetchone()
    settings['background'] = data[0]
    settings['header'] = data[1]
    settings['text'] = data[2]
    settings['name'] = data[3]
    settings['settings'] = data[4]
    print(settings)
    return settings

@eel.expose
def replace_settings(b, h, t, n, s):
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    cursor.execute(f"UPDATE settings SET background='{b}', header='{h}', text='{t}', name='{n}', settings='{s}'")
    db.commit()
    playsound.playsound("./sounds/ok3.wav")
    #{'background': '#2A3738', 'header': '#232C2E', 'text': '#616F6F', 'name': '#F32A2A', 'settings': '#1C1C1C'}

@eel.expose
def task():
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    data = cursor.execute(f"SELECT * FROM processes").fetchall()
    return data

@eel.expose
def remove_task(name):
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    data = cursor.execute(f"SELECT * FROM processes WHERE name='{name}'").fetchone()
    p = psutil.Process(int(data[1]))
    p.terminate()

@eel.expose
def get_token():
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    return cursor.execute(f"SELECT * FROM settings").fetchone()[0]

@eel.expose
def replace_token(token):
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    cursor.execute(f"UPDATE settings SET bot_token='{token}'")
    db.commit()
    playsound.playsound("./sounds/ok3.wav")
    
def start_auto_start():
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    data = cursor.execute(f"SELECT * FROM auto_start").fetchall()
    cursor.execute("DELETE FROM processes")
    db.commit()
    for i in data:
        try:
            print(i[1])
            p = subprocess.Popen([i[0]], shell=True)
            cursor.execute(f"INSERT INTO processes (name, id) VALUES ('{i[1]}', '{p.pid}')")
            db.commit()
        except Exception as ex: print(ex)

async def start_get_text():
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, get_text.main)
    except Exception as e:
        print("Error:", e)

async def start_gui():
    try:
        eel.start('main.html', port=8080, size=(600, 700))
    except Exception as e:
        print("Error:", e)

async def start_async():
    start_auto_start()
    await asyncio.gather(start_get_text(), start_gui())

loop = asyncio.get_event_loop()
loop.create_task(start_async())
loop.run_forever()
