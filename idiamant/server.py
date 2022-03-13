#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

from const import Constantes
from idiamant import iDiamant
from mqtt2idiamant import Mqtt2iDiamant
from time import sleep

iDiamant.getToken()
iDiamant.initDiscovery()

# Temps entre chaque pull >= 2
# pullTime = Constantes.idiamantPullStatus
# if pullTime < 2:
#     pullTime = 2

# Envoie des ordres à iDiamant
mqtt2idiamant = Mqtt2iDiamant()
mqtt2idiamant.start()