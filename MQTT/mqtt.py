import paho.mqtt.client as mqtt
import csv

# Configuration de la connexion MQTT
broker = "test.mosquitto.org"
port = 1883
topic = "IUT/Colmar2023/SAE2.04/Maison1"



# Fonction de rappel pour la connexion au broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Connecté au broker MQTT")
    client.subscribe(topic)

# Fonction de rappel pour la réception des messages
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print("Message reçu: ", message)

    # Écriture du message dans un fichier CSV
    with open("messages.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([message])

# Création d'une instance du client MQTT
client = mqtt.Client()

# Configuration des rappels
client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker MQTT
client.connect(broker, port)

# Boucle de gestion du réseau MQTT
client.loop_forever()
