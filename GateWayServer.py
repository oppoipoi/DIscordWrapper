import websocket
import json
import threading
import time
from replit import web
from flask import Flask, request, jsonify, abort
import requests
global Interactions
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType
Interaction = {}
LastBody = []
Add = 0
CLIENT_PUBLIC_KEY = ""
app = Flask(__name__)

@app.route('/roblox', methods=['POST'])
def roblox(): 
  global Add
  global Interaction
  print(Interaction)
  uwu = Interaction
  Add = 1
  Interaction = {}
  Add = 0
  return json.dumps(uwu), 200 
@app.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
  body = request.data.decode()
  if request.json['type'] == InteractionType.APPLICATION_COMMAND:
    Json = json.loads(body) 
    global LastBody
    LastBody = []
    print(Json)
    LastBody.insert(0,Json["data"]["options"][0]["value"])
    LastBody.insert(0,Json["token"])
    LastBody.insert(0,Json["channel_id"])
    LastBody.insert(0,Json["id"])
    LastBody.insert(0,Json["data"]["name"])
    LastBody.insert(0,Json["member"]["user"]["username"])
    LastBody.insert(0,Json["member"]["user"]["id"])
    LastBody.insert(0,"INTERACTION_CREATE")
    Interaction[len(Interaction)+1] = LastBody
    return jsonify({
            "type": 4,
            "data": {
                "tts": False,
                "content": "Loading Please Wait",
                "embeds": [],
                "allowed_mentions": { "parse": [] }
          }
    })


def send_json_request(ws, request):
  ws.send(json.dumps(request))
  
def receive_json_response(ws):
  response = ws.recv()
  if response:
    return json.loads(response)


def heartbeat(interval, ws):
  print("Heartbeat Begin")
  while True:
    time.sleep(interval)
    heartbeatJson = {
      "op": 1,
      "d": "null"
    }
    send_json_request(ws,heartbeatJson)

ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=10&encoding=json")
event = receive_json_response(ws)

heartbeat_interval = event["d"]["heartbeat_interval"] / 1000
threading._start_new_thread(heartbeat,(heartbeat_interval, ws))

token = ""
payload = {
  "op": 2,
  "d": {
    "token": token,
    "intents": 130815,
    "properties": {
      "os": "linux",
      "browser": "my_library",
      "device": "my_library"
    }
  }
}
send_json_request(ws, payload)


def run():
  while True:
    event = receive_json_response(ws)
    global Interaction
    print(event)
    try:
      global Add
      if Add == 0:
        pass
      else:
       while Add != 0:
        time.sleep(float(0.1))
      if event['t'] == "MESSAGE_CREATE":
        Interaction[len(Interaction)+1] = [event['t'],event['d']['content'],event['d']['channel_id'],event['d']['id'],event['d']['author']['username'],event['d']['author']['id']]
      if event['t'] == "MESSAGE_REACTION_ADD":  
        Interaction[len(Interaction)+1] = [event['t'],event['d']['channel_id'],event['d']['user_id'],event['d']['message_id'],event['d']['emoji']['name'],event['d']['member']['user']['username']]

    except:
      pass
    print(" ")
    try:
        print(f"{event['d']['author']['username']}: {event['d']['content']}")
        op_code = event("op")
        if op_code == 11:
          pass
    except:
      pass
  
threading._start_new_thread(run,())

web.run(app)
