# Bibliothèques pour Flask
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField,DateField, SelectField
from wtforms.validators import DataRequired
# Bibliothèques de paramétrage
from dotenv import load_dotenv
# Bibliothèques de data
import pandas as pd
from analyses.analyses import *
from database.f_database import *
import json
from genderize import Genderize
from datetime import date




load_dotenv()
app = Flask(__name__)

app.config["CACHE_TYPE"] = "null"
app.config['SECRET_KEY'] = "Ma super clé !"

# les pages

@app.route("/")
def f_accueil():
   v_titre = "Tout'roule'"
   return render_template("t_accueil.html", 
                          t_titre = v_titre)

# création du formulaire pour la saisie d'une fiche employé

class c_Formulaire_enregistrement_employes(FlaskForm):
    
   wtf_nom = StringField("Nom", validators=[DataRequired()])
   wtf_prenom = StringField("Prénom", validators=[DataRequired()])
   wtf_genre = SelectField("Genre", validators=[DataRequired()],
                            choices=[("female", "Female"),("male", "Male")])
   wtf_fonction = SelectField("Fonction", validators=[DataRequired()],
                               choices=[("Chauffeur", "Chauffeur"), ("Manager", "Manager")])
   wtf_envoyer = SubmitField("Envoyer")

@app.route("/formulaire-employes", methods=["GET", "POST"])

def f_enregistrer_employes():
    f_formulaire = c_Formulaire_enregistrement_employes()
   # Initialize f_nom outside the if block
    f_nom = None

    if f_formulaire.validate_on_submit():
        f_nom = f_formulaire.wtf_nom.data
        f_prenom = f_formulaire.wtf_prenom.data
        f_genre = f_formulaire.wtf_genre.data
        f_fonction = f_formulaire.wtf_fonction.data

        inserer_donnees_employes(f_nom, f_prenom, f_genre, f_fonction)

        f_formulaire.wtf_nom.data = ""
        f_formulaire.wtf_prenom.data = ""
        f_formulaire.wtf_genre.data = ""
        f_formulaire.wtf_fonction.data = ""

    v_titre = "Formulaire employes"
    return render_template("t_formulaire_employes.html",
                           t_nom=f_nom,
                           html_formulaire=f_formulaire,
                           t_titre=v_titre)



# Création du formulaire mission
class c_Formulaire_enregistrement_missions(FlaskForm):
    wtf_id_emp = SelectField("ID empl.", validators=[DataRequired()])

    wtf_immat_mis = SelectField("Immat. véhicule", validators=[DataRequired()])

    wtf_date_depart = DateField("Date départ", default = date.today, validators=[DataRequired()])
    wtf_km_depart = IntegerField("Km départ", validators=[DataRequired()])

    wtf_date_retour = DateField("Date retour", default = date.today, validators=[DataRequired()])
    wtf_km_retour = IntegerField("Km retour", validators=[DataRequired()])
    
    wtf_commentaires = StringField("Commentaires")
    wtf_envoyer = SubmitField("Envoyer")



@app.route("/formulaire-missions", methods=["GET", "POST"])
def f_enregistrer_missions():
    f_formulaire = c_Formulaire_enregistrement_missions()

    # Remplir les listes déroulantes avec les données de la base de données
    employes, immatriculations, max_km_retours = recupere_listes()

    f_formulaire.wtf_id_emp.choices = [(id_emp, id_emp) for id_emp, in employes]
    f_formulaire.wtf_immat_mis.choices = [(immat_veh, immat_veh) for immat_veh, in immatriculations]
    f_formulaire.wtf_km_depart.data = max_km_retours.get(f_formulaire.wtf_immat_mis.data, 0)

   #  f_formulaire.wtf_id_emp.choices = employes
   #  f_formulaire.wtf_immat_mis.choices = immatriculations

    if f_formulaire.validate_on_submit():
        f_employe = f_formulaire.wtf_id_emp.data

        f_immat = f_formulaire.wtf_immat_mis.data

        f_date_depart = f_formulaire.wtf_date_depart.data
        f_km_depart = f_formulaire.wtf_km_depart.data

        f_date_retour = f_formulaire.wtf_date_retour.data
        f_km_retour = f_formulaire.wtf_km_retour.data

        f_commentaires =f_formulaire.wtf_commentaires.data

        # Insérer les données dans la base de données
        inserer_donnees_missions(f_employe, f_immat, f_date_depart, f_km_depart, f_date_retour, f_km_retour, f_commentaires)

        # Réinitialiser le formulaire après l'envoi
        f_formulaire.wtf_id_emp.data = ""
        f_formulaire.wtf_immat_mis.data = ""

        f_formulaire.wtf_date_depart.data = ""
        f_formulaire.wtf_km_depart.data = ""
        
        f_formulaire.wtf_date_retour.data = ""
        f_formulaire.wtf_km_retour.data = ""    
        
        f_formulaire.wtf_commentaires.data = ""

    v_titre = "Formulaire missions"
    return render_template("t_formulaire_missions.html", t_titre=v_titre, form=f_formulaire)









# création du formulaire pour la modification d'une fiche mission

class c_Formulaire_enregistrement_missions2(FlaskForm):
  wtf_employe = IntegerField("ID empl.", validators=[DataRequired()])
  wtf_km_depart = IntegerField("Km départ", validators=[DataRequired()])
  wtf_km_retour = IntegerField("Km retour", validators=[DataRequired()])
  wtf_date_depart = DateField("Date départ", validators=[DataRequired()])
  wtf_date_retour = DateField("Date retour", validators=[DataRequired()])
  wtf_immat = StringField("Immat. véhicule", validators=[DataRequired()])
  wtf_envoyer = SubmitField("Envoyer")


@app.route("/formulaire-missions2", methods=["GET", "POST"])
def f_enregistrer_missions2():
   f_formulaire = c_Formulaire_enregistrement_missions2()

   if f_formulaire.validate_on_submit():
      f_employe = v_formulaire.wtf_employe.data
      f_km_depart = v_formulaire.wtf_km_depart.data
      f_km_retour = v_formulaire.wtf_km_retour.data
      f_date_depart = v_formulaire.wtf_date_depart.data
      f_date_retour = v_formulaire.wtf_date_retour.data
      f_immat = v_formulaire.wtf_immat.data
      f_formulaire.wtf_employe.data = ""
      f_formulaire.wtf_km_depart.data = ""
      f_formulaire.wtf_km_retour.data = ""
      f_formulaire.wtf_date_depart.data = ""
      f_formulaire.wtf_date_retour.data = ""
      f_formulaire.wtf_immat.data = ""
      
   v_titre = "Formulaire missions"
   return render_template("t_formulaire_missions2.html" ,
                          t_titre = v_titre,
                          html_formulaire = f_formulaire)



# Création du formulaire pour la saisie d'un véhicule
class c_Formulaire_enregistrement_vehicules(FlaskForm):

   wtf_type_veh = SelectField("Type véhicule", validators=[DataRequired()],
                              choices=[("benne", "benne"),("citerne", "citerne"),("fourgon", "fourgon"),("frigorifique", "frigorifique")])        
   wtf_immat_veh = StringField("Immatriculation véhicule", validators=[DataRequired()])
   
  # Bouton de soumission du formulaire 
   wtf_envoyer = SubmitField("Envoyer")


# Route pour afficher et traiter le formulaire de saisie des véhicules
@app.route("/formulaire_vehicules", methods=["GET", "POST"])

def f_enregistrer_vehicules():
    # Crée une instance du formulaire
    f_formulaire = c_Formulaire_enregistrement_vehicules()

    f_nom = None

    if f_formulaire.validate_on_submit():
        # Récupère les données saisies dans les champs du formulaire
        f_immat_veh = f_formulaire.wtf_immat_veh.data
        f_type_veh = f_formulaire.wtf_type_veh.data

        inserer_donnees_vehicules(f_immat_veh, f_type_veh)

        # Effacez les champs du formulaire après la soumission
        f_formulaire.wtf_immat_veh.data = ""
        f_formulaire.wtf_type_veh.data = ""

    # Titre de la page
    v_titre = "Formulaire vehicules"
    # Renvoyer le modèle HTML correspondant avec le formulaire et le titre
    return render_template("t_formulaire_vehicules.html",
                           t_nom=f_nom,
                           html_formulaire=f_formulaire,
                           t_titre=v_titre)


@app.route("/rgpd")
def f_rgpd():
   return render_template("t_rgpd.html")


@app.route("/mentions")
def f_mentions():
   return render_template("t_mentions.html")

@app.errorhandler(404)
def page_introuvable(e):
   return render_template("t_404.html"), 404





@app.route("/kpi")
def f_nb_emp_repondu():
   v_reponse1 = nb_emp_repondu() 
   v_reponse2 = list_emp_repondu()
   v_reponse3 = total_parcouru()
   v_reponse4 = total_parcouru_type()
   v_reponse5 = tableau_employes()

   return render_template("t_kpi.html", 
                          t_reponse1 = v_reponse1, 
                          t_reponse2 = v_reponse2,
                          t_reponse3 = v_reponse3,
                          t_reponse4 = v_reponse4,
                          t_reponse5 = v_reponse5)
                          
                          

@app.route("/kpi2")
def f_nb_emp_repondu2():
   
   v_reponse5 = tableau_employes()

   return render_template("t_kpi2.html", t_reponse5 = v_reponse5)
                          
