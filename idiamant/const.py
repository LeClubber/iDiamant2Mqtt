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
    idiamantUser = os.getenv("IDIAMANT_USER")
    idiamantPassword = os.getenv("IDIAMANT_PASSWORD")
    idiamantClientId = os.getenv("IDIAMANT_CLIENT_ID")
    idiamantClientSecret = os.getenv("IDIAMANT_CLIENT_SECRET")
    idiamantPullStatus = int(os.getenv("IDIAMANT_PULL_STATUS", 5))
