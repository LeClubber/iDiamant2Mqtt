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
    liste_home_id = list()

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

        url = "https://api.netatmo.com/api/homesdata"
        headers = {"Authorization": "Bearer " + iDiamant.access_token}
        response = requests.get(url, headers=headers)
        jsonStatus = json.loads(response.text)
        homes = jsonStatus['body']['homes']
        for home in homes:
            iDiamant.liste_home_id.append(home['id'])


    @staticmethod
    def updateToken():
        """ Update d'un token en fin de vie """

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
        for home_id in iDiamant.liste_home_id:
            url = "https://api.netatmo.com/api/homestatus?home_id=" + home_id
            headers = {"Authorization": "Bearer " + iDiamant.access_token}
            response = requests.get(url, headers=headers)
            jsonStatus = json.loads(response.text)
            modules = jsonStatus['body']['home']['modules']
            for module in modules:
                if "NBR" == module['type']:
                    id_volet = module['id']
                    topic = Constantes.mqttTopic + "/cover/" + id_volet + "/config"
                    payload = '{'
                    payload += '"command_topic": "' + Constantes.mqttTopic + '/cover/' + id_volet + '/set",'
                    payload += '"unique_id": "' + id_volet + '"'
                    payload += '}'
                    iDiamant.publish(topic, payload)
