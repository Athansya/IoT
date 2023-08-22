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
import time

# ---------------------------------------------------------------------------- #
#                                  CONSTANTES                                  #
# ---------------------------------------------------------------------------- #
BROKER = "mqtt-dashboard.com"
PORT = 1883
TOPIC = "iotunam/"
CLIENT_NAMES = ["A", "B", "C", "D"]
CLIENT_IDS = [f"Client-{name}" for name in CLIENT_NAMES]
MESSAGE_LISTS = [[] for _ in CLIENT_NAMES]  # Una lista por cliente

if __name__ == "__main__":
    # Creamos lista de objetos
    clients_obj_list = [
        mqtt.connect_mqtt(client_id=client, broker=BROKER, port=PORT)
        for client in CLIENT_IDS
    ]

    # Suscribimos clientes a topicos
    print("SUBSCRIBING CLIENTS")
    for index, client in enumerate(clients_obj_list):
        client.loop_start()
        time.sleep(1)
        if index == 0:  # Si soy el primer cliente
            topic_sub = TOPIC + CLIENT_NAMES[-1]
            print(f"{index=}")
            print(f"{topic_sub=}")
            message = "Telefono descompuesto!"
            mqtt.subscribe(client, CLIENT_IDS[index], topic=topic_sub, message_list=MESSAGE_LISTS[index])
        else:
            if index < len(CLIENT_NAMES):
                topic_sub = TOPIC + CLIENT_NAMES[index - 1]
            print(f"{index=}")
            print(f"{topic_sub=}")
            mqtt.subscribe(client, CLIENT_IDS[index], topic=topic_sub, message_list=MESSAGE_LISTS[index])
            time.sleep(1)
        time.sleep(1)
        print(50 * '-')

    # Publicamos mensajes en topicos
    print("PUBLISHING MESSAGES")
    for index, client in enumerate(clients_obj_list):
        client.loop_start()
        time.sleep(1)
        if index == 0:  # Si soy el primer cliente
            topic_pub = TOPIC + CLIENT_NAMES[1]
            print(f"{index=}")
            print(f"{topic_pub=}")
            message = "Telefono descompuesto!"
            mqtt.publish(client, CLIENT_IDS[index], topic_pub, message, qos=1)
            time.sleep(1)
        else:
            if index < len(CLIENT_NAMES) - 1:
                topic_pub = TOPIC + CLIENT_NAMES[index + 1]
            else:
                topic_pub = TOPIC + CLIENT_NAMES[0]
            print(f"{index=}")
            print(f"{topic_pub=}")
            mqtt.publish(client, CLIENT_IDS[index], topic_pub, message, qos=1)
            time.sleep(1)
        time.sleep(1)
        print(50 * '-')


    # Mostramos mensajes recibidos por cada cliente
    for index, msg_list in enumerate(MESSAGE_LISTS):
        time.sleep(1)
        print(f"Mensajes recibidos por {CLIENT_NAMES[index]}")
        mqtt.show_received_messages(msg_list)

    # Cerramos las conexiones
    for client in clients_obj_list:
        client.loop_stop




