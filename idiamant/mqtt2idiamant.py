#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import paho.mqtt.client as mqtt
import requests
from const import Constantes
from threading import Thread

from idiamant import iDiamant

class Mqtt2iDiamant(Thread):
    """ Thread chargé de la connexion au broker MQTT """

    def __init__(self):
        Thread.__init__(self)

    def on_connect(self, client, userdata, flags, rc):
        """ Abonnement aux topics """
        affichage = "Connected to MQTT with result code " + str(rc)
        print(affichage)
        topic = Constantes.mqttTopic + '/cover/+/set'
        client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        """ Traitement du message recu """
        url = "https://api.netatmo.com/api/setstate"
        headers = {"Authorization": "Bearer " + iDiamant.access_token}
        topic = str(msg.topic)
        id_volet = topic.replace(Constantes.mqttTopic + '/cover/', '').replace('/set', '')
        
        payload = str(msg.payload, encoding="utf-8")
        position = -1
        match payload:
            case 'OPEN':
                position = 100
            case 'CLOSE':
                position = 0
            case _:
                position = -1
        
        data = {
            "home": {
                "id": iDiamant.volets[id_volet]['id_home'],
                "modules": [
                {
                    "id": id_volet,
                    "target_position": position,
                    "bridge": iDiamant.volets[id_volet]['bridge']
                }
                ]
            }
        }

        # Appel de l'API
        response = requests.post(url, json=data, headers=headers)
        if 200 != response.status_code:
            print("Erreur : " + response.content)

    def run(self):
        """ Démarrage du service MQTT """
        client = mqtt.Client()
        if Constantes.mqttUser:
            client.username_pw_set(Constantes.mqttUser, Constantes.mqttPassword)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(Constantes.mqttHost, Constantes.mqttPort, 60)
        client.loop_forever()


