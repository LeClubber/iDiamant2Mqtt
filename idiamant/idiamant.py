#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import json
import requests
import paho.mqtt.client as mqtt
from const import Constantes
from time import sleep

class iDiamant():

    access_token = ""
    refresh_token = ""
    expire_token = 0
    volets = {}

    @staticmethod
    def getToken():
        """ Récupération du token sepuis Netatmo """
        url = "https://api.netatmo.com/oauth2/token"
        data = {'grant_type': 'password', 
            'username': Constantes.idiamantUser,
            'password': Constantes.idiamantPassword,
            'client_id': Constantes.idiamantClientId,
            'client_secret': Constantes.idiamantClientSecret,
            'scope': 'read_bubendorff write_bubendorff'
        }
        response = requests.post(url, data)
        while 200 != response.status_code:
            attente = 20
            print("Problème d'accès au token : attente de " + attente + " secondes")
            sleep(attente)
            response = requests.post(url, data)
            
        jsonStatus = json.loads(response.text)
        iDiamant.access_token = jsonStatus['access_token']
        iDiamant.refresh_token = jsonStatus['refresh_token']
        iDiamant.expire_token = int(jsonStatus['expires_in'])

        url = "https://api.netatmo.com/api/homesdata"
        headers = {"Authorization": "Bearer " + iDiamant.access_token}
        response = requests.get(url, headers=headers)
        jsonStatus = json.loads(response.text)
        homes = jsonStatus['body']['homes']
        for home in homes:
            home_id = home['id']
            modules = home['modules']
            for module in modules:
                if "NBR" == module['type']:
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
    def initDiscovery():
        """ Publication des config pour discovery """
        for volet in iDiamant.volets:
            topic = Constantes.mqttTopic + "/cover/" + volet + "/config"
            payload = '{'
            payload += '"unique_id": "' + volet + '",'
            payload += '"name": "' + iDiamant.volets[volet]['name'] + '",'
            payload += '"command_topic": "' + Constantes.mqttTopic + '/cover/' + volet + '/set"'
            payload += '}'
            iDiamant.publish(topic, payload)
