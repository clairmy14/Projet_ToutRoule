import os
import sqlite3

def f_creerLaBaseDeDonnees():
    if os.path.isfile('database/db_tout_roule.db'):
        print("La base existe déjà.")
    else:
        connexion = sqlite3.connect('database/db_tout_roule.db')
        curseur = connexion.cursor()

        curseur.execute("""
                        CREATE TABLE vehicules (
                            immat_veh TEXT PRIMARY KEY,
                            type_veh TEXT NOT NULL
                        )
                        """)

        curseur.execute("""
                        CREATE TABLE employes (
                            id_emp INTEGER PRIMARY KEY AUTOINCREMENT,
                            nom_emp TEXT NOT NULL,
                            prenom_emp TEXT NOT NULL,
                            genre_emp TEXT NOT NULL,
                            fonction_emp TEXT NOT NULL
                        )
                        """)

        curseur.execute("""
                        CREATE TABLE missions (
                            id_mis INTEGER PRIMARY KEY AUTOINCREMENT,
                            km_depart INTEGER NOT NULL,
                            km_retour INTEGER NOT NULL,
                            immat_mis TEXT NOT NULL,
                            id_emp TEXT NOT NULL,
                            date_depart DATE NOT NULL,
                            date_retour DATE NOT NULL,
                            prenom_emp,s TEXT,
                            FOREIGN KEY(immat_mis) REFERENCES vehicules(immat_veh),
                            FOREIGN KEY(id_emp) REFERENCES employes(id_emp)
                        )
                        """)

        connexion.commit()
        connexion.close()



def inserer_donnees_employes(nom, prenom,genre,fonction):
    try:
        with sqlite3.connect('database/db_tout_roule.db') as connexion:
            curseur = connexion.cursor()
            curseur.execute("INSERT INTO employes (nom_emp, prenom_emp,genre_emp,fonction_emp) VALUES (?, ?, ?, ?)",
                            (nom, prenom,genre,fonction))
            connexion.commit()
    except sqlite3.IntegrityError as e:
        print(e)



def inserer_donnees_vehicules(immat_veh, type_veh):
    try:
        with sqlite3.connect('database/db_tout_roule.db') as connexion:
            curseur = connexion.cursor()
            curseur.execute("INSERT INTO vehicules (immat_veh, type_veh) VALUES (?, ?)",
                            (immat_veh, type_veh))
            connexion.commit()
    except sqlite3.IntegrityError as e:
        print(e)


# Fonction pour insérer des données dans la table missions
def inserer_donnees_missions(id_emp, immat_mis, date_depart, km_depart, date_retour, km_retour, commentaires):
    try:
        with sqlite3.connect('database/db_tout_roule.db') as connexion:
            curseur = connexion.cursor()
            curseur.execute("INSERT INTO missions (id_emp, immat_mis, date_depart, km_depart, date_retour, km_retour, commentaires) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (id_emp, immat_mis, date_depart, km_depart, date_retour, km_retour, commentaires))
            connexion.commit()
    except sqlite3.IntegrityError as e:
        print(e)


def recupere_listes():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('database/db_tout_roule.db')
        cursor = conn.cursor()

        # Récupérer les ID employés depuis la table employes
        cursor.execute("SELECT id_emp FROM employes")
        employes = cursor.fetchall()

        # Récupérer les immatriculations des véhicules depuis la table vehicules
        cursor.execute("SELECT immat_veh FROM vehicules")
        immatriculations = cursor.fetchall()

        # Récupérer le km_retour maximal pour chaque immatriculation
        max_km_retours = {}
        for immat in immatriculations:
            immat_mis = immat[0]
            cursor.execute("SELECT MAX(km_retour) FROM missions WHERE immat_mis = ?", (immat_mis,))
            max_km_retour = cursor.fetchone()[0]
            max_km_retours[immat_mis] = max_km_retour if max_km_retour is not None else 0

        # Fermer la connexion à la base de données
        conn.close()

        return employes, immatriculations, max_km_retours
    except sqlite3.Error as e:
        print(e)
        return [], [], {}