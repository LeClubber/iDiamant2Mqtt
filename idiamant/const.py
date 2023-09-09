#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import os

class Constantes():
    
    # Recuperation des variables d'environnement
    mqttPort = int(os.getenv('MQTT_PORT', 1883))
    mqttHost = os.getenv('MQTT_HOST', "localhost")
    mqttTopic = os.getenv('MQTT_TOPIC', "homeassistant")
    mqttUser = os.getenv('MQTT_USER')
    mqttPassword = os.getenv('MQTT_PASSWORD')
    idiamantClientId = os.getenv("IDIAMANT_CLIENT_ID")
    idiamantClientSecret = os.getenv("IDIAMANT_CLIENT_SECRET")
    idiamantAccessToken = os.getenv("IDIAMANT_ACCESS_TOKEN")
    idiamantRefreshToken = os.getenv("IDIAMANT_REFRESH_TOKEN")
    idiamantExpireToken = 60
