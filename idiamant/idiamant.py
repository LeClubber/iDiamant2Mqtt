#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import json
import requests
import paho.mqtt.client as mqtt
from const import Constantes
from time import sleep

class iDiamant():

    access_token = Constantes.idiamantAccessToken
    refresh_token = Constantes.idiamantRefreshToken
    expire_token = 120
    volets = {}

    @staticmethod
    def initDiscovery():
        """ Récupération de tous les volets depuis l'API Netatmo """
        url = "https://api.netatmo.com/api/homesdata"
        headers = {"Authorization": "Bearer " + iDiamant.access_token}
        response = requests.get(url, headers=headers)
        jsonStatus = json.loads(response.text)
        homes = jsonStatus['body']['homes']
        for home in homes:
            if 'modules' in home:
                home_id = home['id']
                modules = home['modules']
                for module in modules:
                    if "NBR" == module['type'] or "NBO" == module['type']:
                        iDiamant.volets[module['id']] = {
                            'name':module['name'],
                            'bridge':module['bridge'],
                            'id_home':home_id
                        }

    @staticmethod
    def updateToken():
        """ Update d'un token en fin de vie """
        url = "https://api.netatmo.com/oauth2/token"
        data = {'grant_type': 'refresh_token', 
            'refresh_token': iDiamant.refresh_token,
            'client_id': Constantes.idiamantClientId,
            'client_secret': Constantes.idiamantClientSecret
        }
        response = requests.post(url, data)
        while 200 != response.status_code:
            attente = 20
            print("Problème d'accès au renouvellement de token : attente de " + attente + " secondes")
            sleep(attente)
            response = requests.post(url, data)

        jsonStatus = json.loads(response.text)
        iDiamant.access_token = jsonStatus['access_token']
        iDiamant.refresh_token = jsonStatus['refresh_token']
        iDiamant.expire_token = int(jsonStatus['expires_in'])

    @staticmethod
    def publish(topic, playload, retain=True):
        """ Publication des messages MQTT """
        client = mqtt.Client()
        if Constantes.mqttUser:
            client.username_pw_set(Constantes.mqttUser, Constantes.mqttPassword)
        client.connect(Constantes.mqttHost, Constantes.mqttPort, 60)
        client.publish(topic, playload, retain=retain)
        client.disconnect()

    @staticmethod
    def initMqtt():
        """ Publication des config sur Mqtt """
        for volet in iDiamant.volets:
            topic = Constantes.mqttTopic + "/cover/" + volet + "/config"
            payload = '{'
            payload += '"unique_id": "' + volet + '",'
            payload += '"name": "' + iDiamant.volets[volet]['name'] + '",'
            payload += '"command_topic": "' + Constantes.mqttTopic + '/cover/' + volet + '/set"'
            payload += '}'
            iDiamant.publish(topic, payload)
