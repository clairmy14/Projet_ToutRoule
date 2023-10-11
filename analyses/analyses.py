import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

def connecter():
    """
    :name : connecter
    :param : 
    :return : curseur et connexion nécessaires à d'autres fonctions
    :desc : se connecter à la base et activer le curseur
    """

    try:
        connexion_connecter = sqlite3.connect("database/db_tout_roule.db")
        curseur_connecter = connexion_connecter.cursor()
        return curseur_connecter, connexion_connecter

    except sqlite3.Error as e:
        print(e, "\n\n=====> La connexion ne s'est pas établie")


def deconnecter(curseur,connexion):
    
    """
    :name : deconnecter
    :param : curseur et connexion retournés par la fonction connecter()
    :return : 
    :desc : désactiver le curseur et se déconnecter de la base
    """ 
    
    try:
        curseur.close()
        connexion.close()
    except sqlite3.Error as e:
        print(e, "\n\n=====> La déconnexion ne s'est pas réalisée")


def afficher_tables():
    
    """
    :name : afficher_employe
    :param : identifiant de l'employé
    :return : la fiche de l'employé
    :desc : afficher simplement la fiche de l'employé. 
            cette fonction est utile aux fonctions modifier_employe et supprimer_employe
    """
    
    try:
        curseur_afficher, connexion_afficher = connecter()
        
        curseur_afficher.execute(f"SELECT name  FROM sqlite_schema WHERE type='table'  ")
        verification = curseur_afficher.fetchall()
        # print(verification)
        connexion_afficher.close()
        return verification


    except sqlite3.Error as e:
        print(e,"\n\n=====> L'affichage de votre employé a échoué.")


def nb_emp_repondu():
    ### le nombre de salariés ayant répondu


    conn = sqlite3.connect('database/db_tout_roule.db')
    cursor = conn.cursor()
    # cursor.execute('SELECT * FROM missions')
    # data = cursor.fetchall()
    # Exécutez la requête SQL pour compter les valeurs uniques dans la colonne id_emp
    cursor.execute('SELECT COUNT(DISTINCT id_emp) FROM missions')

    # Récupérez le résultat de la requête
    count_unique_id_emp = cursor.fetchone()[0]

    # Fermez la connexion à la base de données
    conn.close()

    # Affichez le résultat en tant que KPI
    # print(f'Nombre d\'id_emp uniques dans la table missions : {count_unique_id_emp}')

    # return f'Nombre d\'id_emp uniques dans la table missions : {count_unique_id_emp}'

    return f'{count_unique_id_emp} empl.'

def list_emp_repondu():
   ### la liste des salariés ayant répondu. Si le salarié est un homme, affichez son nom/prénom de couleur bleu. Si c’est une femme, de couleur verte.

    # Établissez la connexion à votre base de données
    conn = sqlite3.connect('database/db_tout_roule.db')

    # Créez un curseur
    cursor = conn.cursor()

    # Exécutez une requête pour obtenir les employés uniques avec leurs noms, prénoms et genres
    cursor.execute('''
        SELECT DISTINCT nom_emp, prenom_emp, genre_emp
        FROM employes 
        
        INNER JOIN missions ON employes.id_emp = missions.id_emp
        
    ''')

    # Récupérez les résultats de la requête
    result = cursor.fetchall()

    # Fermez la connexion à la base de données
    conn.close()

    # Affichez la liste des employés uniques et leurs informations
    for row in result:
        nom_emp, prenom_emp, genre_emp = row
        print(f"Nom: {nom_emp}, Prénom: {prenom_emp}, Genre: {genre_emp}")

    #### une graphique montre la réparation homme femme 


    # Comptez le nombre d'employés de chaque genre (male/female)
    nombre_hommes = sum(1 for row in result if row[2] == 'male')
    nombre_femmes = sum(1 for row in result if row[2] == 'female')

    # Créez un graphique en camembert
    labels = ['Hommes', 'Femmes']
    sizes = [nombre_hommes, nombre_femmes]
    colors = ['orange', 'green']
    explode = (0.1, 0)  # pour faire ressortir une portion du camembert

    fig2 = plt.figure(figsize=(6, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140, textprops={'fontsize': 14})
    plt.title('Répartition des employés par genre', fontsize = 14)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    

    fig2.savefig('static/figure2.png')
    # Affichez le graphique
    # plt.show()

    return fig2






def total_parcouru():
    #### le total de kilomètres parcourus tout véhicule confondu


    # Connexion à la base de données
    conn = sqlite3.connect('database/db_tout_roule.db')
    cursor = conn.cursor()

    # Requête SQL pour récupérer les kilomètres de toutes les missions
    cursor.execute('SELECT SUM(km_retour - km_depart) FROM missions')

    # Récupération du résultat
    total_kilometres = cursor.fetchone()[0]

    # Fermeture de la connexion
    conn.close()

    # Affichage du total de kilomètres parcourus
    # print(f'Total de kilomètres parcourus : {total_kilometres} km')

    # return f'Total de kilomètres parcourus : {total_kilometres} km'

    return f'{total_kilometres} km'

def total_parcouru_type():
    ### le total de kilomètres parcourus tout véhicule confondu



    # Connexion à la base de données
    conn = sqlite3.connect('database/db_tout_roule.db')
    cursor = conn.cursor()

    # Requête SQL pour calculer le total des kilomètres par type de véhicule
    cursor.execute('''SELECT v.type_veh, SUM(m.km_retour - m.km_depart) 
                    FROM vehicules v 
                    INNER JOIN missions m ON v.immat_veh = m.immat_mis 
                    GROUP BY v.type_veh''')

    # Récupération des résultats
    data = cursor.fetchall()

    # Fermeture de la connexion
    conn.close()

    # Préparation des données pour le graphique
    types_vehicules = [row[0] for row in data]
    total_kilometres = [row[1] for row in data]

    # Création du graphique avec des couleurs dégradées
    fig, ax = plt.subplots(figsize=(10, 6))

    # Créez un dégradé de couleurs à partir du bleu (plus foncé) au bleu (plus clair)
    cmap = plt.get_cmap('Blues', len(types_vehicules))

    # Créez une plage de couleurs de 0 à 1 pour les barres
    color_range = np.linspace(0, 1, len(types_vehicules))

    # Créez des barres individuelles avec des couleurs dégradées
    bars = []
    for i, (vehicule, km) in enumerate(zip(types_vehicules, total_kilometres)):
        bar = ax.bar(vehicule, km, color=cmap(color_range[i]))
        bars.append(bar)
        
        # Ajout du chiffre (total des kilomètres avec " km") à l'intérieur de chaque barre
        ax.text(bar[0].get_x() + bar[0].get_width() / 2, km + 2, f'{total_kilometres[i]} km', 
                ha='center', va='bottom', fontsize=14)

    plt.xlabel('Type de Véhicule', fontsize=14)
    plt.ylabel('Total des Kilomètres Parcourus', fontsize=14)
    plt.title('Total des Kilomètres par Type de Véhicule', fontsize=14)
    # plt.xticks(rotation=45)

    # ax.set_xticklabels(ax.get_xticks(), fontsize=12)  # Taille de police pour l'axe x
    ax.set_yticklabels(ax.get_yticks(), fontsize=12)  # Taille de police pour l'axe y
    
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)))
    

    fig.savefig('static/figure4.png')
    # Affichez le graphique
    # plt.show()

    return fig


def tableau_employes():
    # Établir la connexion à la base de données
    conn = sqlite3.connect('database/db_tout_roule.db')
    cursor = conn.cursor()
    # Exécuter la requête pour obtenir les employés uniques avec leurs noms, prénoms et genres
    cursor.execute('''
        SELECT DISTINCT nom_emp, prenom_emp, genre_emp
        FROM employes
        INNER JOIN missions ON employes.id_emp = missions.id_emp
        GROUP BY nom_emp, prenom_emp
    ''')
    # Récupérer les résultats de la requête
    data = cursor.fetchall()
    # Fermer la connexion à la base de données
    conn.close()
    # Rendre le modèle HTML avec les données
    # return render_template('tableau.html', data=data)


    return data

# print(tableau_employes())

