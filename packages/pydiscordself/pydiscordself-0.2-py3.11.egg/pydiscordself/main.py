import websocket
import threading
import requests
import json
import time

class SelfBot:
    def __init__(self, token):
        self.token = token
        self.isRunning = False

        self.heartbeatInterval = 0
        self.heartbeatCountdown = 0
        self.sequence = 0

        self.events = {}

    def addEventListener(self, event_name, function):
        if event_name not in self.events.keys():
            self.events[event_name] = []
        
        if callable(function):
            self.events[event_name].append(function)

    def start(self):
        self.isRunning = True
        self.ws = websocket.WebSocketApp("wss://gateway.discord.gg?v=10&encoding=json",
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close
        )
        self.ws.run_forever()

    def on_open(self, _ws):
        print("[{}][{}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), "INFO", "Connected to discord api ..."))

    def on_close(self, _ws, _one, _two):
        self.isRunning = False
        print("[{}][{}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), "INFO", "Disconnected from discord api ..."))

    
    def heartbeat(self):
        while self.isRunning:
            if self.heartbeatCountdown <= 0:
                self.ws.send(json.dumps({
                    "op": 1,
                    "d": self.sequence
                }))

                self.heartbeatCountdown = self.heartbeatInterval
        
            time.sleep(0.1)
            self.heartbeatCountdown -= 100

    def setActiveGuild(self, guild_id):
        self.ws.send(json.dumps({
            "op": 14,
            "d": {
                "guild_id": "759270446478000179",
                "typing": True,
                "threads": True,
                "activities":True,
                "members":[],
                "channels":{},
                "thread_member_lists":[]
            }
        }))

    def on_message(self, ws, message):
        message = json.loads(message)
        self.sequence = message["s"]

        match message["op"]:
            case 10:
                self.heartbeatInterval = message["d"]["heartbeat_interval"] - 1000

                thread = threading.Thread(target=self.heartbeat)
                thread.daemon = True
                thread.start()

                self.ws.send(json.dumps({
                    "op": 2,
                    "d": {
                        "token": self.token,
                        "capabilities": 3276799,
                        "compress": False,
                        "properties":{
                            "os": "pydiscordself",
                            "browser": "pydiscordself",
                            "device": "pydiscordself"
                        }
                    }
                }))

            case 0:
                if message["t"] not in self.events.keys():
                    return
                
                for event in self.events[message["t"]]:
                    event(message["d"])

    def send_message(self, channel_id, content):
        return requests.post("https://discord.com/api/v10/channels/{}/messages".format(channel_id),
            headers={
                "Authorization": self.token,
                "Contennt-Type": "application/json"
            },
            json={
                "content": content
            }
        ).json()

    def delete_message(self, channel_id, message_id):
        requests.delete("https://discord.com/api/v10/channels/{}/messages/{}".format(channel_id, message_id),
            headers={
                "Authorization": self.token
            }
        )

    def edit_message(self, channel_id, message_id, content):
        return requests.patch("https://discord.com/api/v10/channels/{}/messages/{}".format(channel_id, message_id),
            headers={
                "Authorization": self.token,
                "Contennt-Type": "application/json"
            },
            json={
                "content": content
            }
        ).json()

    def get_user(self, id):
        return requests.get("https://discord.com/api/v10/users/{}".format(id),
            headers={
                "Authorization": self.token
            }
        ).json()

    def get_current_user(self):
        return requests.get("https://discord.com/api/v10/users/@me",
            headers={
                "Authorization": self.token
            }
        ).json()