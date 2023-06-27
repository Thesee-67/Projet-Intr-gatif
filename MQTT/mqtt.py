import paho.mqtt.client as mqtt
import mysql.connector
from datetime import datetime
import json

broker = "test.mosquitto.org"
topics = ["IUT/Colmar2023/SAE2.04/Maison1", "IUT/Colmar2023/SAE2.04/Maison2"]

db_host = "localhost"
db_user = "root"
db_password = "04/11/17"
db_name = "sae24"

# Variable de données temporaires
fichier_temporaire = "MQTT/donnees_temporaires.json"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion établie avec succès")
        # Souscription aux topics
        for topic in topics:
            client.subscribe(topic)
    else:
        print("Échec de la connexion. Code de retour =", rc)


def on_message(client, userdata, msg):
    retransmettre_donnees_temporaires()
    print("Message reçu. Topic =", msg.topic, " | Payload =", msg.payload.decode())
    db_connection = None
    cursor = None

    # Séparation des valeurs du payload
    payload_parts = msg.payload.decode().split(",")
    values = {}
    for part in payload_parts:
        if "=" in part:
            key, value = part.split("=")
            values[key.strip()] = value.strip()

    try:
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        cursor = db_connection.cursor()

        # Insertion du capteur s'il n'existe pas déjà
        sql_query_capteur = "INSERT IGNORE INTO capteur (id_capteur, PIECE) VALUES (%s, %s)"
        cursor.execute(sql_query_capteur, (values.get("Id"), values.get("piece")))
        db_connection.commit()

        # Conversion de la date au format anglais
        date_str = values.get("date")
        if date_str is not None:
            try:
                date = datetime.strptime(date_str, "%d/%m/%Y").date()
                date_en = date.strftime("%Y-%m-%d")
            except ValueError:
                print("Erreur: Format de date incorrect. Utilisez le format 'jour/mois/année' (par exemple, '22/06/2023').")
                return
        else:
            print("Erreur: La valeur de date est manquante.")
            return
        
        # Ajout de date_str et date_en dans le dictionnaire values
        values["date_str"] = date_str
        values["date_en"] = date_en

        # Insertion des données dans la table "details"
        sql_query_details = "INSERT INTO Donnees (id_capteur_id, date, time, temps) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_query_details, (values.get("Id"), values.get("date_en"), values.get("time"), values.get("temp")))
        db_connection.commit()

        print("Données insérées avec succès dans la base de données.")

    except mysql.connector.Error as error:
        print("Erreur lors de la connexion à la base de données:", error)
        # Stocker temporairement les données dans un fichier
        donnees_temporaires = []
        try:
            with open(fichier_temporaire, "r") as file:
                donnees_temporaires = json.load(file)
        except FileNotFoundError:
            pass
        donnees_temporaires.append(values)
        with open(fichier_temporaire, "w") as file:
            json.dump(donnees_temporaires, file)

    finally:
        if cursor is not None:
            cursor.close()
        if db_connection is not None and db_connection.is_connected():
            db_connection.close()


def retransmettre_donnees_temporaires():
    try:
        with open(fichier_temporaire, "r") as file:
            donnees_temporaires = json.load(file)
            if donnees_temporaires:
                client.publish("IUT/Colmar2023/SAE2.04/Maison1", json.dumps(donnees_temporaires))
    except FileNotFoundError:
        pass


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker MQTT
client.connect(broker, 1883, 60)

# Retransmettre les données temporaires au redémarrage
retransmettre_donnees_temporaires()

client.loop_forever()
