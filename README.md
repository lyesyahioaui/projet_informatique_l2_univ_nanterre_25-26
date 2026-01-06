# Site Nature – Application Flask + PostgreSQL

Projet de site web de gestion d’une association de protection de la nature, développé avec **Flask** (Python) et **PostgreSQL**.  
Le site permet la gestion des adhérents, des sorties, des espèces, et un espace dédié aux gestionnaires.

---

## 1. Prérequis

- Python 3.x installé
- PostgreSQL installé et en cours d’exécution
- Un utilisateur PostgreSQL avec droits sur une base (ex. `lyesyahiaoui`)
- `pip` disponible

---

## 2. Installation du projet

1. **Cloner le dépôt** :

```bash
git clone <URL_DU_DEPOT>
cd <NOM_DU_DOSSIER>

Créer et activer un environnement virtuel (recommandé) :

bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate


Installer les dépendances Python :

bash
pip install flask psycopg2-binary
3. Configuration de la base de données
Créer la base (si nécessaire) :

bash
createdb nature_db
Importer le schéma et les données (si un dump.sql est fourni) :

bash
psql -h localhost -U <utilisateur_pg> -d nature_db -f dump.sql
Vérifier la configuration dans db.py :

Le fichier db.py doit contenir les bons paramètres de connexion, par exemple :

python
import psycopg2
import psycopg2.extras

def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",
        dbname="nature_db",
        user="<utilisateur_pg>",
        password="<mot_de_passe>",
        cursor_factory=psycopg2.extras.NamedTupleCursor,
    )
    return conn
Adapte user et password à ta configuration PostgreSQL.

4. Lancer l’application
Depuis le dossier du projet (avec l’environnement virtuel activé) :

bash
# Linux / macOS
export FLASK_APP=main.py
export FLASK_ENV=development

# Windows (cmd)
set FLASK_APP=main.py
set FLASK_ENV=development

flask run
Par défaut, l’application sera accessible à l’adresse :

text
http://127.0.0.1:5000/
5. Comptes de test
Des comptes de test sont déjà présents dans la table adherent pour faciliter la démonstration.

Utilisateur (notre enseignant ):
Email : francois.delbot@gmail.com

Mot de passe : françoisdelbot

Gestionnaire 1

Email : lyesyahiaoui1007@gmail.com

Mot de passe : lyesyahiaoui

est_gestionnaire = TRUE

Gestionnaire 2

Email : redouanehamma06@gmail.com

Mot de passe : redouanehamma

est_gestionnaire = TRUE

Ces comptes permettent d’accéder à l’espace gestionnaire et aux fonctionnalités réservées (création de sorties, inscription d’adhérents, saisie des paiements, ajout d’espèces, etc.).

Comptes adhérent simples
Les autres lignes de la table adherent (Alice Martin, Louis Bernard, etc.) sont des adhérents classiques (est_gestionnaire = FALSE) permettant de tester l’espace adhérent et l’inscription à des sorties.

6. Structure principale du projet
main.py : routes Flask et logique principale

db.py : connexion à la base PostgreSQL

templates/ :

accueil.html : page d’accueil

connexion.html : page de connexion

page_inscription.html : inscription adhérent

espace_adherent.html : espace membre

espace_gestionnaire.html : espace gestionnaire

sorties.html, details_sorties.html : gestion des sorties

especes.html, details_espece.html : catalogue des espèces

ajouter_espece.html, creer_sortie.html, saisir_paiement.html, etc.

7. Remarques
L’application fonctionne en local pour la démonstration du projet.

Les mots de passe sont stockés en clair uniquement pour simplifier les tests dans le cadre pédagogique (en production, il faudrait les hasher).
