import paho.mqtt.client as mqtt
import json
import threading


class Client(threading.Thread):
    def __init__(self, username, projectName, password):
        threading.Thread.__init__(self)
        self.username = username
        self.projectName = projectName
        self.password = password
        self.initalized = False
        self.mqtt_client = mqtt.Client(client_id=projectName + "@" + username)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.username_pw_set(
            username=projectName + "@" + username, password=password)
        self.mqtt_client.connect('thingesp.siddhesh.me', 1893, 60)

    def setCallback(self, func):
        self.callback_func = func
        self.initalized = True

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to WhatsApp")
        self.mqtt_client.subscribe(self.projectName + "/" + self.username)

    def on_message(self, client, userdata, msg):
        if not self.initalized:
            return
        else:
            payload = json.loads(msg.payload.decode("utf-8"))
            # print(payload)
            if payload['action'] == 'query':
                out = self.callback_func(
                    payload['query'].lower()) or "Invalid Command"
                sendr = {
                    "msg_id": payload['msg_id'], "action": "returned_api_response", "returned_api_response": out}
                self.mqtt_client.publish(
                    self.projectName + "/" + self.username, json.dumps(sendr))

    # def device_call(self, to_num, msg):
    #     out = {"action": "device_call", "to_number": to_num, "msg": msg}
    #     self.mqtt_client.publish(
    #         self.projectName + "/" + self.username, json.dumps(out))

    def run(self):
        self.mqtt_client.loop_forever()
