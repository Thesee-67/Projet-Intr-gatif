import csv
import pyodbc

# Informations de connexion à la base de données SQL Server
server = '10.252.18.79'
database = 'nom_de_la_base_de_donnees'
username = 'nom_utilisateur'
password = 'mot_de_passe'
driver = 'Nom_du_pilote_ODBC'  # Remplacez par le nom du pilote ODBC approprié

# Chemin vers le fichier CSV
fichier_csv = '/home/yulei/messages.csv'

# Chaîne de connexion à la base de données SQL Server
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Fonction pour extraire les valeurs à partir de la chaîne de données
def extract_values(data):
    values = {}
    elements = data.split(',')
    for element in elements:
        key, value = element.split('=')
        values[key] = value
    return values

# Connexion à la base de données SQL Server
conn = pyodbc.connect(conn_str)

# Lecture du fichier CSV et insertion des données dans la base de données
with open(fichier_csv, 'r') as csvfile:
    reader = csv.reader(csvfile)
    cursor = conn.cursor()
    for row in reader:
        # Récupération des valeurs du fichier CSV
        id_val = row[0]
        piece_val = row[1]
        date_val = row[2]
        heure_val = row[3]
        temp_val = row[4]

        # Requête d'insertion des données dans la table
        query = "INSERT INTO Collecte (id, piece, date, heure, temp) VALUES (?, ?, ?, ?, ?)"
        params = (id_val, piece_val, date_val, heure_val, temp_val)

        # Exécution de la requête d'insertion
        cursor.execute(query, params)

# Validation des modifications dans la base de données
conn.commit()

# Fermeture de la connexion
conn.close()
