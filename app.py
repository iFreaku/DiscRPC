#!!-----------------------------------------------------!!#

# After Running the file
# Open your browser and go to http://127.0.0.1:5000/

# For adding apps you need to go to https://discord.com/developers/applications
# Copy the app id and then in the "static/apps.json" file store it
# Example: ("appname": "appid")
# [
#   {"GTA VI": "32555456445xxxx"},
#   {"RPC.exe": "2435655342xxxx"},
#   ...
# ]

#!!-----------------------------------------------------!!#

import os, sys, json
import threading
import asyncio
import time
import requests
from flask import Flask, request, render_template, jsonify
from pypresence import Presence

app = Flask(__name__)

rpc_data = {
    "appid": None,
    "large_image": None,
    "large_text": None,
    "details": None,
    "state": None,
    "buttons": []
}
rpc_running = False
RPC = None


def update_rpc():
    global rpc_running, RPC

    client_id = rpc_data.get("appid", "")
    if not client_id:
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        RPC = Presence(client_id)
        RPC.connect()
        rpc_running = True

        while rpc_running:
            RPC.update(
                large_image=rpc_data.get("large_image", ""),
                large_text=rpc_data.get("large_text", ""),
                details=rpc_data.get("details", ""),
                state=rpc_data.get("state", ""),
            )
            time.sleep(5)

    except Exception as e:
        print(f"RPC Error: {e}")

    finally:
        if RPC:
            RPC.close()
        rpc_running = False


@app.route("/")
def index():
    try:
        with open("static/apps.json", "r") as f:
            apps = json.load(f)
        return render_template("index.html", apps=apps)
    except Exception as e:
        return f"{e}<br>Have you updated your app list??"


@app.route("/update_rpc", methods=["POST"])
def update_rpc_data():
    global rpc_data, rpc_running

    data = request.json
    rpc_data.update(data)

    if rpc_running:
        terminate_rpc()

    threading.Thread(target=update_rpc, daemon=True).start()

    return jsonify({"status": "success", "message": "RPC updated and restarted!"})


@app.route("/terminate_rpc", methods=["POST"])
def terminate_rpc():
    global rpc_running, RPC
    rpc_running = False

    if RPC:
        try:
            RPC.close()
        except Exception as e:
            print(f"Error closing RPC: {e}")
    
    return jsonify({"status": "success", "message": "RPC terminated!"})


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
