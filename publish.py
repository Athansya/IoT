# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


# broker = "broker.emqx.io"
broker = "mqtt-dashboard.com"
port = 1883
topic = "iotunam/test"
# topic = "python/mqtt"
# Generate a Client ID with the publish prefix.
client_id = f"publish-{random.randint(0, 1000)}"
# username = 'emqx'
# password = 'public'


def connect_mqtt():
    """Inicializa y conecta 
    """
    def on_connect(client, userdata, flags, rc):
        """

        Args:
            client (_type_): _description_
            userdata (_type_): _description_
            flags (_type_): _description_
            rc (_type_): _description_

        Returns:
            _type_: _description_
        """
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect  # Se llama la función interna cada vez que se ejecuta
    client.connect(broker, port)
    return client


def publish(client):
    """Manda un mensaje con un número del 1 al 5.

    Args:
        client (_type_): _description_
    """
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count} - TEST"
        result = client.publish(topic, msg, qos=0)  # Manda un mensaje bajo un tópico
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    # publish(client)
    client.loop_stop()


if __name__ == "__main__":
    run()
