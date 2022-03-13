# iDiamant2Mqtt

Outil de conversion de l'API du iDiamant (volets Bubendorff) depuis MQTT pour Home Assistant.

## Netatmo
Pour que cela fonctionne, les volets doivent être configurés dans l'application "Home + Control" de Legrand - Netatmo - Bticino.
Rendez-vous ensuite sur la page https://dev.netatmo.com/ et connectez-vous avec les même identifiants que l'application. Il faut enuite cliquer sur son login puis "My apps".
Cliquer ensuite sur "Create" et renseiger les champs suivants :
- app name : le nom de votre application, par exemple "Volets"
- description : une courte descrition, pzr exemple "Gestion des volets depuis HASS"
- data protection officer name : votre nom
- data protection officer email : l'email de votre compte

Cliquer sur "I agree to the terms and conditions" et sur Save.
Dans la partie "App Technical Parameters", conserver les identifiants "client ID" et "client secret" pour le déploiement.


## Déploiement

Il vous faut :

- Home-Assistant (en même temps, vous êtes surtout là pour lui non?)
- Un brocker (serveur) MQTT (sans certificat pour l'instant)
- Le service iDiamant2Mqtt

Il y a deux solutions pour déployer ce service :

- Docker (recommandé)
- Exécuter le script python directement

### Docker

Je préfère cette solution car elle encapsule le processus, contient toutes les dépendances  et facilite le déploiement.

Le service peut être démarré grâce à la commande suivante :

``` sh
docker run -d --name idiamant \
    -e PALAZZETTI_HOST=192.168.1.1 \
    -e PALAZZETTI_PULL_STATUS=5 \
    leclubber/idiamant2mqtt
```

Ou en docker-compose (recommandé) :

``` yaml
version: '3'
services:
  palazzetti:
    container_name: idiamant
    image: leclubber/idiamant2mqtt
    privileged: true
    restart: always
    environment:
      - MQTT_PORT=1883
      - MQTT_HOST=mqtt
      - MQTT_TOPIC=homeassistant
      - IDIAMANT_USER=<votre email>
      - IDIAMANT_PASSWORD=<votre mot de passe>
      - IDIAMANT_CLIENT_ID=<client ID généré>
      - IDIAMANT_CLIENT_SECRET=<client secret généré>
```

Certaines variables d'environnement sont optionnelles, elles possèdent une valeur par défaut. Toutes les variables d'environnement sont les suivantes :

- MQTT_PORT (1883 par défaut)
- MQTT_HOST (mqtt par défaut)
- MQTT_TOPIC (homeassistant par défaut)
- MQTT_USER (vide par défaut)
- MQTT_PASSWORD (vide par défaut)
- IDIAMANT_USER (aucun par défaut)
- IDIAMANT_PASSWORD (aucun par défaut)
- IDIAMANT_CLIENT_ID (aucun par défaut)
- IDIAMANT_CLIENT_SECRET (aucun par défaut)

Un fichier [docker-compose.yml](docker-compose.yml) est disponible pour exemple, avec toutes les variables d'environnement ainsi que les services homeassistant et mqtt.

Une fois votre fichier docker-compose.yml réalisé, il faut lancer la commande suivante pour démarrer le ou les services configurés :

``` sh
docker-compose up -d
```

### Python

Il faut récupérer le contenu du dossier [idiamant](idiamant) et le mettre sur votre futur serveur.

Certaines variables d'environnement sont optionnelles, elles possèdent une valeur par défaut (voir section Docker).
Chaque variable sera définie de cette manière :

``` sh
export ENV_VAR=valeur
```

Exécuter ensuite les lignes suivantes :

``` sh
pip install -r requirements.txt
chmod +x *.py
./server.py
```

## Configuration de Home-Assistant

Le iDiamant dans Home-Assistant fonctionne avec le discovery de MQTT. Il suffit de s'abonner dans Home-Assistant au canal souhaité ("homeassistant" par défaut).

**Optionnel :** On peut également le déclarer via le fichier de configuration [configuration.yaml](configuration.yaml). Il faut ajouter un module "cover" de cette façon :
``` yaml
cover:
  TODO
```

Vous pourrez alors :
- Monter, descendre et arrêter les volets
- Renommer dans Home-Assistant chaque volet

## Todo list

- [x] Initialisation des config dans MQTT
- [x] Discovery MQTT
- [x] Documentation
- [x] Utilisation d'un login/mot de passe pour le broker MQTT
- [x] Publier image Docker en multiple arch
- [ ] Renouvellement du token
- [ ] Attente du serveur MQTT si non disponible
- [ ] Tester les paramètres et gestion d'erreur
- [ ] Utilisation de certificat pour le broker MQTT
