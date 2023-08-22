"""
File: practica_2.py
Project: <<projectname>>
File Created: Monday, 21st August 2023 2:12:51 pm
Author: Alfonso Toriz Vazquez (atoriz98@comunidad.unam.mx)
-----
Last Modified: Monday, 21st August 2023 2:12:51 pm
Modified By: Alfonso Toriz Vazquez (atoriz98@comunidad.unam.mx>)
-----
License: MIT License
-----
Description: 
"""

# ---------------------------------------------------------------------------- #
#                                  BIBLIOTECAS                                 #
# ---------------------------------------------------------------------------- #
import funciones_mqtt_utils as mqtt
from random import randint
import time

# ---------------------------------------------------------------------------- #
#                                  CONSTANTES                                  #
# ---------------------------------------------------------------------------- #
BROKER = "mqtt-dashboard.com"
PORT = 1883
TOPIC = "testeo_practica_2/"
CLIENT_NAMES = ["X", "Y", "Z"]
CLIENT_IDS = [f"Client-{name}" for name in CLIENT_NAMES]
MESSAGE_LISTS = [[] for _ in CLIENT_NAMES]  # Una lista por cliente

if __name__ == "__main__":
    # Creamos dict de objetos
    clients = [
        mqtt.connect_mqtt(
            client_id=client_id,
            broker=BROKER,
            port=PORT
        ) for client_id in CLIENT_IDS
    ]

    # START
    print("------- STARTING CONNECTIONS -------")
    for client in clients:
        client.loop_start()
        time.sleep(1)
        print(40 * '-')

    # SUBSCRIBE
    print("------- SUBSCRIBING TO TOPICS -------")
    for index, client in enumerate(clients):
        if index == 0:
            topic = TOPIC + CLIENT_NAMES[-1]
        else:
            topic = TOPIC + CLIENT_NAMES[index - 1]

        mqtt.subscribe(
            client=client,
            client_id=CLIENT_IDS[index],
            topic=topic,
            message_list=MESSAGE_LISTS[index]
        )
        print(f"{CLIENT_IDS[index]} subscribed to {topic}")
        time.sleep(1)
        print(40 * '-')
        
    # PUBLISHING
    print("------- PUBLISHING IN TOPICS -------")
    for index, client in enumerate(clients):
        topic = TOPIC + CLIENT_NAMES[index]
        if index == 0:
            message = "Telefono descompuesto..."
            mqtt.publish(
                client=client,
                client_id=CLIENT_IDS[index],
                topic=topic,
                msg=message,
                qos=1
            )
        else:
            mqtt.publish(
                client=client,
                client_id=CLIENT_IDS[index],
                topic=topic,
                msg=MESSAGE_LISTS[index][0],
                qos=1
            )
        time.sleep(1)
        print(40 * '-')

    # CLOSE
    for client in clients:
        client.loop_stop()
        client.disconnect()
        
    # SHOW MESSAGES
    for index, name in enumerate(CLIENT_NAMES):
        print(f"Messages received by {name}:")
        mqtt.show_received_messages(MESSAGE_LISTS[index])
        

    # clients = {
        # name:{
            # "client": mqtt.connect_mqtt(
                # client_id=client_id,
                # broker=BROKER,
                # port=PORT),
            # "ID": client_id,
            # "msgs": []
        # } for name, client_id in zip(CLIENT_NAMES, CLIENT_IDS)
    # }
    # print(clients)
# 
    # for index, key in enumerate(clients.keys()):
        # clients[key]["client"].loop_start()

    # Subscribing clients
    # print("--- CONNECTED AND SUBSCRIBED ---")
    # for index, key in enumerate(clients.keys()):
        # clients[key]["client"].loop_start()
        # if key == "A":
            # topic = TOPIC + CLIENT_NAMES[-1]
        # else:
            # topic = TOPIC + CLIENT_NAMES[index - 1]
# 
        # mqtt.subscribe(
            # client=clients[key]["client"],
            # client_id=clients[key]["ID"],
            # topic= TOPIC + CLIENT_NAMES[-1],
            # message_list=clients[key]["msgs"]
        # )
        # time.sleep(1)
        # print(f"{clients[key]['ID']} - Subscribed to: {topic}")
        # print(40 * '-')
# 
    # Messaging
    # for index, key in enumerate(clients.keys()):
        # if key == "A":
            # message = "Telefono descompuesto!"
            # mqtt.publish(
                # client=clients[key]["client"],
                # client_id=clients[key]["ID"],
                # topic=TOPIC + key,
                # msg=message,
                # qos=1,
                # repetitions=3
            # )
            # time.sleep(3)
        # else:
            # mqtt.publish(
                # client=clients[key]["client"],
                # client_id=clients[key]["ID"],
                # topic=TOPIC + key,
                # msg=clients[key]["msgs"][0],
                # qos=1
            # )
# 
    # clients["A"]["client"].loop_start()
    # mqtt.subscribe(
        # client=clients["A"]["client"],
        # client_id=clients["A"]["ID"],
        # topic= TOPIC + list(clients.keys())[-1],
        # message_list=clients["A"]["msgs"]
    # )

    # for client in clients_obj_list:
        # client.loop_stop()

    # mqtt.show_received_messages(MESSAGE_LISTS)