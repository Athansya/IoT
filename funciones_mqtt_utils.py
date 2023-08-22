"""
File: funciones_mqtt_utils.py
Project: IoT
File Created: Friday, 18th August 2023 1:38:12 pm
Author: Alfonso Toriz Vazquez (atoriz98@comunidad.unam.mx)
-----
Last Modified: Friday, 18th August 2023 1:38:37 pm
Modified By: Alfonso Toriz Vazquez (atoriz98@comunidad.unam.mx>)
-----
License: MIT License
-----
Description: Colección de funciones para establecer una conexión MQTT a un broker
y gestionar el envío y la recepción de los mensajes.
"""

# ---------------------------------------------------------------------------- #
#                                  BIBLIOTECAS                                 #
# ---------------------------------------------------------------------------- #

import random
import paho.mqtt.client as mqtt_client
import time

# ---------------------------------------------------------------------------- #
#                                  CONSTANTES                                  #
# ---------------------------------------------------------------------------- #

BROKER = "mqtt-dashboard.com"
PORT = 1883
TOPIC = "iotunam/test"
CLIENT_ID = f"testing-{random.randint(0, 1000)}"

# ---------------------------------------------------------------------------- #
#                                    CLASES                                    #
# ---------------------------------------------------------------------------- #


class FailedConnectionException(Exception):
    "Raised when failed connection"
    pass


class FailedMessageException(Exception):
    "Raised when failed to send message"
    pass


# ---------------------------------------------------------------------------- #
#                                   FUNCIONES                                  #
# ---------------------------------------------------------------------------- #


def connect_mqtt(
    client_id: str=CLIENT_ID,
    broker: str=BROKER,
    port: str=PORT
    ) -> mqtt_client.Client:
    """Inicializa un cliente y lo conecta a la red

    Returns:
        client (mqtt_client.Client): Objeto cliente ya conectado.
    """
    def on_connect(
        client: mqtt_client.Client, 
        userdata, 
        flags: dict, 
        rc: int
    ):
        """Conecta el cliente al internet

        Args:
            client (mqtt_client.Client): Objeto cliente
            userdata (_type_): datos definidos del usuario.
            flags (dict): banderas de respuesta del broker.
            rc (int): resultado de la conexión.

        Raises:
            FailedConnectionException: Error en la conexión.
        """
        if rc == 0:
            print(f"Connected {client_id} to MQTT Broker!")
        else:
            raise FailedConnectionException(
                f"Failed to connect {client_id} with error code: {rc}\n"
            )

    client = mqtt_client.Client(client_id)
    # print(f"client: {client_id}")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(
    client: mqtt_client.Client, 
    client_id: str,
    topic: str, 
    msg: str,
    qos: int = 1,
    repetitions: int = 1
):
    """Manda un mensaje a cierto tópico.

    Args:
        client (mqtt_client.Client): Objeto cliente. 
        topic (str): Tópico al que se mandará el mensaje (remitente). 
        msg (str): Contenido del mensaje. 
        qos (int, optional): Quality of Service. Defaults to 1.
        repetitions (int, optional): número de veces que se mandará el mensaje.
        Defaults to 1.

    Raises:
        ValueError: Valor erróneo para QoS.
        FailedMessageException: Error en el envío del mensaje.
    """
    # QoS
    if qos not in [0, 1, 2]:
        raise ValueError(f"Invalid value for QoS: {qos}")

    for _ in range(repetitions):
        time.sleep(1)
        try:
            result = client.publish(topic, msg, qos)  # [0, 1]
            status = result[0]
            if status != 0:
                raise FailedMessageException("Message failed to send")
            else:
                print(f"'{client_id}' sent '{msg}' to topic '{topic}'")
        except FailedMessageException as e:
            print(f"{e} with status: {status}")


def subscribe(
    client: mqtt_client.Client,
    client_id: str,
    topic: str,
    message_list: list[str]
):
    """Suscribe un cliente a cierto tópico y almacena los mensajes recibidos

    Args:
        client (mqtt_client.Client): Objeto cliente. 
        topic (str): Tópico.
        message_list (list[str]): lista para almacenar mensajes.
    """
    def on_message(client, userdata, msg):
        """Callback cada vez que reciba un mensaje.

        Args:
            client (mqtt_client.Client): Objeto cliente.
            userdata (_type_): Datos definidos del usuario.
            msg (str): Mensaje recibido en formato binario.
        """
        print(f"'{client_id}' recieved '{msg.payload.decode()}' from '{msg.topic}' topic")
        message_list.append(msg.payload.decode())  # Guarda el mensaje
        #TODO INTENTAR UTILIZAR UNA COLA EN LUGAR DE UNA LISTA

    client.subscribe(topic)
    client.on_message = on_message


def show_received_messages(message_list: list[str]):
    """Muestra los mensajes recibidos guardados.

    Args:
        message_list (list[str]): Lista de mensajes guardados. 
    """
    for idx, message in enumerate(message_list):
        print(f"Message #{idx + 1}: {message}")


def run():
    # Lista para almacenar mensajes
    msg_list = []
    # Conectamos el cliente
    client = connect_mqtt()
    # Inicializamos el ciclo
    client.loop_start()
    # Nos suscribimos a un tópico
    subscribe(client, topic=TOPIC, message_list=msg_list)
    # Definimos y mandamos un mensaje
    message = f"Test Merida"
    publish(client, topic=TOPIC, msg=message, qos=1)
    # Cerramos el ciclo
    client.loop_stop()
    # Mostramos los mensajes guardados
    show_received_messages(msg_list)

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    run()
