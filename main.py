from mistralai import Mistral
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
from psycopg2.extras import NamedTupleCursor
import db

app = Flask(__name__)
app.secret_key = 'secret_key'


client = Mistral(api_key="sGu26YVHlUKMcXZGtDS4wSizHR240tpi")


# Base de FAQ du site
FAQ_QUESTIONS = [
    "comment créer un compte sur le site",
    "comment m'inscrire sur le site",
    "où se trouve le formulaire d'inscription",
    "comment devenir adhérent",
    "comment me connecter à mon compte",
    "je n'arrive pas à me connecter",
    "où est la page de connexion",
    "comment me déconnecter du site",
    "comment voir la liste des sorties",
    "comment m'inscrire à une sortie",
    "je veux participer à une sortie",
    "comment savoir s'il reste des places",
    "comment voir les sorties passées",
    "comment filtrer les sorties par thème",
    "combien coûte la cotisation",
    "comment payer la cotisation",
    "comment savoir si j'ai payé ma cotisation",
    "quels sont les moyens de paiement",
    "comment consulter les espèces",
    "où trouver la liste des espèces",
    "comment rechercher une espèce par ses caractéristiques",
    "comment voir la liste des nichoirs",
    "comment ajouter une observation de nichoir",
    "quelles informations saisir pour une observation",
    "que puis je voir dans mon espace adhérent",
    "quel est le but de ce site",
    "que fait l'association nature et environnement",
    "quels sont les types d'activités proposées",
    "comment adhérer",
    "comment devenir adhérent",
    "comment s'inscrire",
    "je veux m'inscrire",
    "comment s'inscrire à une sortie",
    "comment participer à une sortie",
]

FAQ_REPONSES = [
    "Pour créer un compte, utilise la page d'inscription du site et remplis le formulaire avec ton nom, prénom, adresse mail, numéro de téléphone et mot de passe.",
    "Pour t'inscrire sur le site, clique sur le lien d'inscription dans le menu puis remplis tous les champs du formulaire.",
    "Le formulaire d'inscription est accessible via le menu du site, généralement sous le nom Inscription ou Créer un compte.",
    "Pour devenir adhérent, il suffit de créer un compte sur le site puis de payer la cotisation correspondant à ton statut.",
    "Pour te connecter, va sur la page de connexion et saisis l'adresse mail et le mot de passe que tu as utilisés lors de l'inscription.",
    "Si tu n'arrives pas à te connecter, vérifie ton adresse mail et ton mot de passe. Si le problème persiste, contacte un gestionnaire.",
    "La page de connexion est accessible depuis le menu principal du site, sous le nom Connexion ou Espace adhérent.",
    "Pour te déconnecter, utilise le lien de déconnexion qui vide ta session et te renvoie vers la page d'accueil.",
    "Tu peux voir la liste des sorties depuis la page Sorties, qui affiche toutes les sorties proposées par l'association.",
    "Pour t'inscrire à une sortie, va sur la page Sorties, clique sur Détails pour la sortie choisie puis utilise le bouton d'inscription si des places sont disponibles.",
    "Si tu veux participer à une sortie, consulte la page Sorties, choisis une activité et utilise le bouton d'inscription après t'être connecté.",
    "Le nombre de places restantes est affiché pour chaque sortie, en comparant l'effectif maximal et le nombre d'inscrits.",
    "Ton historique de sorties est visible dans ton espace adhérent, où sont listées les sorties auxquelles tu es inscrit.",
    "Tu peux filtrer les sorties par thème grâce au formulaire de filtres présent sur la page Sorties.",
    "La cotisation annuelle dépend du statut de l'adhérent, par exemple étudiant, personnel de l'université ou extérieur.",
    "La cotisation est enregistrée par le gestionnaire via la page de saisie des paiements, à partir des informations de l'adhérent.",
    "Pour savoir si ta cotisation a été payée, tu peux contacter le gestionnaire ou consulter les informations de paiement si elles sont affichées dans ton espace.",
    "Les moyens de paiement acceptés typiquement sont le chèque ou les espèces, tels qu'enregistrés dans la base de données.",
    "Les espèces répertoriées sont consultables dans la page dédiée aux espèces, qui affiche les animaux et plantes observés par l'association.",
    "La liste des espèces est disponible dans la page Espèces du site.",
    "Pour rechercher une espèce par ses caractéristiques, tu peux utiliser la fonction de recherche inversée qui filtre les espèces en fonction des critères choisis.",
    "La liste des nichoirs est consultable dans la page Nichoirs, qui affiche les informations de localisation et de type pour chaque nichoir.",
    "Pour ajouter une observation de nichoir, connecte-toi puis utilise le formulaire prévu pour saisir le nombre d'oeufs, le type d'occupation et la période de nidification.",
    "Lors d'une observation de nichoir, tu dois saisir au minimum le nombre d'oeufs, le type d'occupation, la période de nidification et le nichoir concerné.",
    "Dans ton espace adhérent, tu peux voir les sorties auxquelles tu as participé et accéder à des statistiques liées aux activités.",
    "Le but de ce site est de diffuser les informations sur les activités de l'association et de simplifier la gestion des adhérents et des sorties.",
    "L'association Nature et environnement propose des sorties thématiques et des activités de protection et d'observation de la faune et de la flore locales.",
    "L'association propose notamment des sorties nature, l'observation d'espèces locales et le suivi de nichoirs installés sur différents sites."
"Pour adhérer, cliquez sur « S'inscrire » dans le menu ou sur la carte Adhésion de la page d'accueil, puis remplissez le formulaire en ligne. Une fois validé, vous avez directement accès à votre espace adhérent.",
    "Pour devenir adhérent, utilisez le bouton « S'inscrire » sur la page d'accueil ou dans le menu, complétez le formulaire et validez. Votre compte est immédiatement actif.",
    "Pour vous inscrire, allez dans la rubrique « Inscription », remplissez le formulaire et validez. Vous pourrez ensuite accéder à votre espace adhérent.",
    "Pour vous inscrire, utilisez la page « Inscription » du site, complétez le formulaire demandé puis validez. L’accès est instantané.",
    "Pour vous inscrire à une sortie, allez dans « Sorties », choisissez une sortie et cliquez sur le bouton d'inscription correspondant.",
    "Pour participer à une sortie, consultez la liste des sorties puis utilisez le bouton d'inscription de la sortie qui vous intéresse.",
    ]
import re

def normaliser(texte: str) -> str:
    texte = texte.lower()
    texte = re.sub(r"[^\w\s]", " ", texte)  # enlever la ponctuation
    texte = re.sub(r"\s+", " ", texte).strip()
    return texte


def repondre_gemini(question: str) -> str:
    """Répond avec FAQ d'abord, puis Mistral pour nature + association"""
    try:
        # 1️⃣ NORMALISATION
        q_norm = normaliser(question)
        faq_norm = [normaliser(q) for q in FAQ_QUESTIONS]

        # 2️⃣ CHERCHE DANS LA FAQ
        vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3)).fit([q_norm] + faq_norm)
        question_vec = vectorizer.transform([q_norm])
        faq_vecs = vectorizer.transform(faq_norm)
        similarities = cosine_similarity(question_vec, faq_vecs)[0]
        best_match_idx = similarities.argmax()
        best_similarity = similarities[best_match_idx]

        # seuil un peu plus bas pour matcher plus facilement
        if best_similarity > 0.3:
            return FAQ_REPONSES[best_match_idx]

        # 3️⃣ SINON MISTRAL, avec domaine élargi
        message = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "user",
                    "content": f"""Tu es l'assistant de l'association Nature et Environnement.

Tu peux répondre sur :
- Nature et environnement
- Espèces animales et végétales
- Sorties nature et activités de l'association
- Protection de l'environnement
- Écosystèmes
- Adhésion et fonctionnement de l'association (inscription, compte adhérent, sorties, observations)
- Zoo
- Paysages naturels (montagnes, forêts, mers, déserts, lacs, rivières...)
- La Faune 
- La Flore

On te fournit parfois un texte appelé "Contexte base de données de l'association"
qui contient la liste des sorties (thème, lieu, date) et la liste des espèces du site.

Quand la question parle de sorties (proposer une sortie, type de sortie, voir un animal, où aller, etc.),
utilise EN PRIORITÉ ce contexte pour :
- dire s'il existe une sortie qui correspond,
- ou proposer un type de sortie parmi celles de la base (par thème ou lieu).

Quand la question parle d'espèces, utilise EN PRIORITÉ la liste d'espèces donnée dans le contexte.

Ne réponds pas sur des sujets qui n'ont vraiment aucun rapport avec ces thèmes
(ex : jeux vidéo, politique, vie privée de personnes, etc.).





Question : {question}

Si la question n'a aucun lien avec ces thèmes, répond : "Je peux seulement répondre sur la nature, l'environnement et le fonctionnement de l'association."

Réponse courte (max 300 caractères) :
"""
                }
            ]
        )

        return message.choices[0].message.content

    except Exception as e:
        return f"Erreur : {str(e)}"


@app.route('/')
@app.route('/accueil')
def accueil():
    return render_template('accueil.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
       nom = request.form['nom']
       email = request.form['email']
       message = request.form['message']
    flash('Votre message a été envoyé avec succès!', 'success')
    return render_template('contact.html')


@app.route('/inscription_sortie/<int:id_sortie>', methods=['POST'])
def inscription_sortie(id_sortie):
    if 'id_adherent' not in session:
        flash('Vous devez être connecté pour vous inscrire à une sortie.', 'danger')
        return redirect(url_for('connexion'))

    with db.connect_to_db() as conn:
        with conn.cursor() as cur:
            #verifier si l'adherent est déja inscrit 
            cur.execute(""" 
                SELECT * FROM inscrit 
                WHERE id_adh = %s AND id_sortie = %s
            """, (session['id_adherent'], id_sortie))
            
            if cur.fetchone():
                flash('Vous êtes déjà inscrit à cette sortie.', 'info')
                return redirect(url_for('details_sortie', id_sortie=id_sortie))        

            # Vérifier le nombre de places disponibles
            cur.execute("""
                SELECT (effectif_max - COUNT(inscrit.id_adh)) AS places_disponibles
                FROM sortie
                LEFT JOIN inscrit ON sortie.id_sortie = inscrit.id_sortie
                WHERE sortie.id_sortie = %s
                GROUP BY sortie.id_sortie;
            """, (id_sortie,))
            places_disponibles = cur.fetchone()

            if places_disponibles and places_disponibles[0] > 0:
                # Inscrire l'adhérent à la sortie
                cur.execute("""
                    INSERT INTO inscrit (id_adh, id_sortie, date_s)
                    VALUES (%s, %s, CURRENT_DATE)
                """, (session['id_adherent'], id_sortie))
                conn.commit()
                flash('Inscription réussie !', 'success')
            else:
                flash('Aucune place disponible pour cette sortie.', 'danger')

    return redirect(url_for('details_sortie', id_sortie=id_sortie))

@app.route('/sorties')
def liste_sorties():
    theme = request.args.get('theme')
    date_min = request.args.get('date_min')
    date_max = request.args.get('date_max')
    places_min = request.args.get('places_min')
    inscrits_min= request.args.get('inscrits_min')

    with db.connect_to_db() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            query = """
            SELECT sortie.*, 
                   (sortie.effectif_max - COUNT(inscrit.id_sortie)) AS places_disponibles,
                   COUNT(inscrit.id_sortie) AS nombre_inscrits
            FROM sortie
            LEFT JOIN inscrit ON sortie.id_sortie = inscrit.id_sortie
            WHERE 1=1
            """
            params = []

            if theme:
                query += " AND sortie.theme ILIKE %s"
                params.append(f'%{theme}%')
            if date_min:
                query += " AND sortie.date_rdv >= %s"
                params.append(date_min)
            if date_max:
                query += " AND sortie.date_rdv <= %s"
                params.append(date_max)
            
            query += " GROUP BY sortie.id_sortie"
            
            if places_min:
                query += " HAVING (sortie.effectif_max - COUNT(inscrit.id_sortie)) >= %s"
                params.append(int(places_min))
            if inscrits_min:
                query += " AND COUNT(inscrit.id_sortie) >= %s"
                params.append(int(inscrits_min))
            
            query += " ORDER BY sortie.date_rdv"

            cur.execute(query, tuple(params))
            sorties = cur.fetchall()

    return render_template('sorties.html', sorties=sorties)


@app.route('/sorties/<int:id_sortie>')
def details_sortie(id_sortie):
    with db.connect_to_db() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            # Récupérer les détails de la sortie
            cur.execute("""
                SELECT sortie.*, 
                       (sortie.effectif_max - COUNT(inscrit.id_adh) FILTER (WHERE inscrit.id_adh IS NOT NULL)) AS places_disponibles,
                       COUNT(inscrit.id_adh) AS nombre_inscrits
                FROM sortie
                LEFT JOIN inscrit ON sortie.id_sortie = inscrit.id_sortie
                WHERE sortie.id_sortie = %s
                GROUP BY sortie.id_sortie;
            """, (id_sortie,))

            sortie = cur.fetchone()
    
    if sortie is None:
        flash('Sortie non trouvée.', 'danger')
        return redirect(url_for('liste_sorties'))

    return render_template('details_sorties.html', sortie=sortie)

@app.route('/statistiques')
def statistiques():
    if 'id_adherent' not in session:
        flash('Vous devez être connecté pour accéder aux statistiques.', 'danger')
        return redirect(url_for('connexion'))

    with db.connect_to_db() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            # Nombre de sorties par mois
            cur.execute("""
                SELECT DATE_TRUNC('month', date_rdv) AS mois, COUNT(*) AS nombre_sorties
                FROM sortie
                GROUP BY DATE_TRUNC('month', date_rdv)
                ORDER BY mois
            """)
            sorties_par_mois = cur.fetchall()

            # Nombre total de kilomètres parcourus
            cur.execute("""
                SELECT SUM(dparcours) AS total_km
                FROM sortie
            """)
            total_km = cur.fetchone().total_km


    return render_template('statistiques.html', 
                           sorties_par_mois=sorties_par_mois, 
                           total_km=total_km)

@app.route('/especes', methods=['GET', 'POST'])
def catalogue_especes():
    with db.connect_to_db() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            # Requête pour récupérer toutes les espèces avec leur groupe
            query = """
                SELECT e.id_especes, e.nom AS nom_espece, g.nomge AS groupe_nom
                FROM especes e
                JOIN groupe_espece g ON e.idge = g.idge
                ORDER BY e.nom;
            """
            cur.execute(query)
            especes = cur.fetchall()

            # Gestion de la recherche inversée
            if request.method == 'POST':
                caracteristique = request.form.get('caracteristiques')
                query_recherche = """
                    SELECT DISTINCT e.id_especes, e.nom AS nom_espece, g.nomge AS groupe_nom
                    FROM especes e
                    JOIN groupe_espece g ON e.idge = g.idge
                    JOIN possede p ON e.id_especes = p.id_especes
                    JOIN caracteristique c ON p.idc = c.idc
                    WHERE c.caracteristique ILIKE %s
                    ORDER BY e.nom;
                """
                cur.execute(query_recherche, (f'%{caracteristique}%',))
                especes = cur.fetchall()

    return render_template('especes.html', especes=especes)

@app.route('/especes/<int:id_espece>')
def details_espece(id_espece):
    with db.connect_to_db() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            query = """
                SELECT e.nom AS nom_espece, g.nomge AS groupe_nom,
                       ARRAY_AGG(c.caracteristique) AS caracteristiques
                FROM especes e
                JOIN groupe_espece g ON e.idge = g.idge
                JOIN possede p ON e.id_especes = p.id_especes
                JOIN caracteristique c ON p.idc = c.idc
                WHERE e.id_especes = %s
                GROUP BY e.nom, g.nomge;
            """
            cur.execute(query, (id_espece,))
            espece = cur.fetchone()

    if not espece:
        flash("Espèce non trouvée.", "danger")
        return redirect(url_for('catalogue_especes'))

    return render_template('details_espece.html', espece=espece)

 
@app.route('/nichoirs')
def liste_nichoirs():
    with db.connect_to_db() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute("""
                SELECT n.idn, n.lat, n.lon, n.hauteur, n.orientation, n.type_nichoir, n.date_pose, n.nom_site
                FROM nichoir n
                ORDER BY n.idn
            """)
            nichoirs = cur.fetchall()
    return render_template('nichoirs.html', nichoirs=nichoirs)


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        # Vérifiez que tous les champs requis sont remplis
        required_fields = ['nom', 'prenom', 'adr_mail', 'num_phone', 'mot_de_passe']
        if not all(field in request.form for field in required_fields):
            flash('Tous les champs sont requis', 'danger')
            return render_template('page_inscription.html')

        # Récupérer les données du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        adr_mail = request.form['adr_mail']
        num_phone = request.form['num_phone']
        mot_de_passe = request.form['mot_de_passe']

        # Connexion à la base de données
        with db.connect_to_db() as conn:
            try:
                with conn.cursor() as cur:
                    # Insérer l'adhérent dans la base de données
                    query = """
                    INSERT INTO adherent (nom, prenom, adr_mail, num_phone, mot_de_passe)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_adh;
                    """
                    cur.execute(query, (nom, prenom, adr_mail, num_phone, mot_de_passe))
                    id_adh = cur.fetchone()[0]  # Récupérer l'ID de l'adhérent nouvellement créé
                    conn.commit()  # Valider la transaction

                session["id_adherent"] = id_adh  # Stocker l'ID dans la session
                flash('Inscription réussie !', 'success')
                return redirect(url_for('espace_adherent'))  # Rediriger vers l'espace adhérent

            except psycopg2.Error as e:
                flash(f'Erreur lors de l\'inscription : {str(e)}', 'danger')
                return render_template('page_inscription.html')

    return render_template('page_inscription.html')  # Affichez le formulaire d'inscription

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        # Récupérer les informations de connexion depuis le formulaire
        email = request.form.get("adr_mail")         # name="adr_mail" dans connexion.html
        password = request.form.get("mot_de_passe")  # name="mot_de_passe" dans connexion.html

        with db.connect_to_db() as conn:
            try:
                with conn.cursor() as cur:
                    # Vérifier les identifiants + récupérer est_gestionnaire
                    cur.execute("""
                        SELECT id_adh, adr_mail, est_gestionnaire
                        FROM adherent 
                        WHERE adr_mail = %s AND mot_de_passe = %s
                    """, (email, password))
                    user = cur.fetchone()

                    if user:
                        id_adh, adr_mail, est_gestionnaire = user
                        session["id_adherent"] = id_adh

                        if est_gestionnaire:
                            # Gestionnaire : accès à l’espace gestionnaire
                            session["id_gestionnaire"] = id_adh
                            flash('Bienvenue dans l’espace gestionnaire.', 'success')
                            return redirect(url_for('espace_gestionnaire'))
                        else:
                            # Adhérent simple
                            session.pop("id_gestionnaire", None)
                            flash('Connexion réussie !', 'success')
                            return redirect(url_for('espace_adherent'))
                    else:
                        flash('Identifiants incorrects.', 'danger')
            except psycopg2.Error as e:
                flash(f'Erreur lors de la connexion : {str(e)}', 'danger')

    # GET ou échec : afficher le formulaire de connexion
    return render_template('connexion.html')



@app.route('/espace-adherent')
def espace_adherent():
    if 'id_adherent' in session:  # Vérifier si l'utilisateur est connecté
        with db.connect_to_db() as conn:
            try:
                with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
                    # Récupérer les informations de l'utilisateur connecté (nom et prénom)
                    cur.execute("SELECT nom, prenom FROM adherent WHERE id_adh = %s", (session['id_adherent'],))
                    user_info = cur.fetchone()  # Récupérer les informations de l'utilisateur
                    
                    # Vérifier si l'utilisateur existe
                    if user_info is None:
                        flash('Utilisateur non trouvé.', 'danger')
                        return redirect(url_for('connexion'))

                    # Récupérer l'historique des sorties de l'adhérent
                    query_historique = """
                    SELECT sortie.theme, sortie.date_rdv, sortie.lieu_rdv
                    FROM inscrit
                    JOIN sortie ON inscrit.id_sortie = sortie.id_sortie
                    WHERE inscrit.id_adh = %s
                    ORDER BY sortie.date_rdv DESC;
                    """
                    cur.execute(query_historique, (session['id_adherent'],))
                    historique = cur.fetchall()  # Récupérer toutes les sorties

                # Passer les données au template (historique, nom et prénom)
                return render_template('espace_adherent.html', historique=historique, nom=user_info.nom, prenom=user_info.prenom)
            except psycopg2.Error as e:
                flash(f'Erreur lors de la récupération des données : {str(e)}', 'danger')
                return redirect(url_for('connexion'))  # Rediriger vers la page de connexion en cas d'erreur
    else:
        return redirect(url_for('connexion'))  # Rediriger vers la page de connexion si non connecté

@app.route('/espace-gestionnaire')
def espace_gestionnaire():
    if 'id_gestionnaire' not in session:
        flash('Accès réservé aux gestionnaires.', 'danger')
        return redirect(url_for('connexion'))
    
    with db.connect_to_db() as conn:
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
                cur.execute("SELECT nom, prenom FROM adherent WHERE id_adh = %s", (session['id_gestionnaire'],))
                user_info = cur.fetchone()
                return render_template('espace_gestionnaire.html', nom=user_info.nom, prenom=user_info.prenom)
        except psycopg2.Error as e:
            flash(f'Erreur lors de la récupération des données : {str(e)}', 'danger')
            return redirect(url_for('connexion'))



@app.route('/ajouter_observation', methods=['GET', 'POST'])
def ajouter_observation():
    if 'id_adherent' not in session:
        flash('Vous devez être connecté pour ajouter une observation.', 'danger')
        return redirect(url_for('connexion'))

    if request.method == 'POST':
        required_fields = ['id_especes', 'idn', 'nbr_oeuf', 'type_occ', 'periode_nid']
        if not all(field in request.form for field in required_fields):
            flash('Tous les champs sont requis', 'danger')
            return render_template('ajouter_observation.html')

        try:
            id_especes = int(request.form['id_especes'])
            idn = int(request.form['idn'])
            nbr_oeuf = int(request.form['nbr_oeuf'])
            type_occ = request.form['type_occ']
            periode_nid = request.form['periode_nid']

            with db.connect_to_db() as conn:
                with conn.cursor() as cur:
                    query = """
                    INSERT INTO observe_nichoir (idn, nbr_oeuf, type_occ, periode_nid, id_adh)
                    VALUES (%s, %s, %s, %s, %s);
                    """
                    cur.execute(query, (idn, nbr_oeuf, type_occ, periode_nid, session['id_adherent']))
                    conn.commit()

            flash('Observation ajoutée avec succès !', 'success')
            return redirect(url_for('espace_adherent'))

        except ValueError:
            flash('Veuillez entrer des valeurs numériques valides pour les champs appropriés.', 'danger')
        except psycopg2.Error as e:
            app.logger.error(f'Erreur lors de l\'ajout de l\'observation : {str(e)}')
            flash(f'Erreur lors de l\'ajout de l\'observation. Veuillez réessayer.', 'danger')

    return render_template('ajouter_observation.html')




@app.route('/inscrire-adherent', methods=['GET', 'POST'])
def inscrire_adherent():
    if 'id_gestionnaire' not in session:
        flash('Accès réservé aux gestionnaires', 'danger')
        return redirect(url_for('connexion'))
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        adr_mail = request.form['adr_mail']
        num_phone = request.form['num_phone']
        mot_de_passe = request.form['mot_de_passe']
        est_gestionnaire = False  # Par défaut, l'adhérent n'est pas un gestionnaire

        with db.connect_to_db() as conn:
            with conn.cursor() as cur:
                try:
                    # Insérer l'adhérent dans la base de données
                    cur.execute("""
                        INSERT INTO adherent (nom, prenom, adr_mail, num_phone, mot_de_passe, est_gestionnaire)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING id_adh;
                    """, (nom, prenom, adr_mail, num_phone, mot_de_passe, est_gestionnaire))
                    
                    id_adh = cur.fetchone()[0]  # Récupérer l'ID de l'adhérent nouvellement créé
                    conn.commit()

                    flash(f'Nouvel adhérent inscrit avec succès (ID: {id_adh})', 'success')
                    return redirect(url_for('espace_gestionnaire'))
                except psycopg2.Error as e:
                    conn.rollback()
                    flash(f'Erreur lors de l\'inscription : {str(e)}', 'danger')

    return render_template('inscrire_adherent.html')


@app.route('/saisir-paiement', methods=['GET', 'POST'])
def saisir_paiement():
    if 'id_gestionnaire' not in session:
        flash('Accès réservé aux gestionnaires', 'danger')
        return redirect(url_for('connexion'))
    
    if request.method == 'POST':
        id_adh = request.form['id_adh']
        id_status = request.form['id_status']
        id_cot = request.form['id_cot']
        moy_p = request.form['moy_p']
        date_pay = request.form['date_pay']
        
        with db.connect_to_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO paye (id_adh, id_status, id_cot, moy_p, date_pay)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_adh, id_status, id_cot, moy_p, date_pay))
                conn.commit()
        
        flash('Paiement enregistré avec succès', 'success')
        return redirect(url_for('espace_gestionnaire'))
    
    return render_template('saisir_paiement.html')

@app.route('/ajouter-espece', methods=['GET', 'POST'])
def ajouter_espece():
    if 'id_gestionnaire' not in session:
        flash('Accès réservé aux gestionnaires', 'danger')
        return redirect(url_for('connexion'))

    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']  # Nom de l'espèce
        idge = request.form['idge']  # Groupe de l'espèce
        caracteristiques = request.form.getlist('caracteristiques')  # Liste des caractéristiques sélectionnées

        with db.connect_to_db() as conn:
            with conn.cursor() as cur:
                try:
                    # Insérer l'espèce dans la table `especes`
                    cur.execute("""
                        INSERT INTO especes (nom, idge)
                        VALUES (%s, %s)
                        RETURNING id_especes;
                    """, (nom, idge))
                    id_especes = cur.fetchone()[0]  # Récupérer l'ID de l'espèce nouvellement créée

                    # Insérer les caractéristiques associées dans la table `possede`
                    for idc in caracteristiques:
                        cur.execute("""
                            INSERT INTO possede (idge, id_especes, idc, valeur)
                            VALUES (%s, %s, %s, 1);  -- Valeur par défaut à 1
                        """, (idge, id_especes, idc))

                    conn.commit()
                    flash('Nouvelle espèce ajoutée avec succès avec ses caractéristiques', 'success')
                except psycopg2.Error as e:
                    conn.rollback()
                    flash(f'Erreur lors de l\'ajout de l\'espèce : {str(e)}', 'danger')

        return redirect(url_for('espace_gestionnaire'))

    # Récupérer les groupes et caractéristiques pour le formulaire
    with db.connect_to_db() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute("SELECT idge, nomge FROM groupe_espece ORDER BY nomge;")
            groupes = cur.fetchall()

            cur.execute("SELECT idc, caracteristique FROM caracteristique ORDER BY caracteristique;")
            caracteristiques = cur.fetchall()

    return render_template('ajouter_espece.html', groupes=groupes, caracteristiques=caracteristiques)


@app.route('/ajouter_nichoir', methods=['GET', 'POST'])
def ajouter_nichoir():
    if 'id_gestionnaire' not in session:
        flash('Accès réservé aux gestionnaires', 'danger')
        return redirect(url_for('connexion'))

    if request.method == 'POST':
        # Récupérer les données du formulaire
        date_inst = request.form['date_inst']
        lieu_inst = request.form['lieu_inst']

        with db.connect_to_db() as conn:
            with conn.cursor() as cur:
                try:
                    # Insérer d'abord dans la table nichoir
                    cur.execute("""
                        INSERT INTO nichoir (date_inst, lieu_inst)
                        VALUES (%s, %s)
                        RETURNING idn;
                    """, (date_inst, lieu_inst))
                    idn = cur.fetchone()[0]  # Récupérer l'ID du nichoir nouvellement créé

                    # Récupérer les informations d'observation si fournies
                    nbr_oeuf = request.form.get('nbr_oeuf')
                    type_occ = request.form.get('type_occ')
                    periode_nid = request.form.get('periode_nid')

                    # Insérer dans la table observe_nichoir si des informations d'observation sont fournies
                    if nbr_oeuf and type_occ:
                        cur.execute("""
                            INSERT INTO observe_nichoir (nbr_oeuf, type_occ, periode_nid, idn, id_adh)
                            VALUES (%s, %s, %s, %s, %s);
                        """, (nbr_oeuf, type_occ, periode_nid, idn, session['id_adherent']))

                    conn.commit()
                    flash('Nouveau nichoir ajouté avec succès', 'success')
                except psycopg2.Error as e:
                    conn.rollback()
                    flash(f'Erreur lors de l\'ajout du nichoir : {str(e)}', 'danger')

        return redirect(url_for('espace_gestionnaire'))

    return render_template('ajouter_nichoir.html')



@app.route('/creer-sortie', methods=['GET', 'POST'])
def creer_sortie():
    if 'id_gestionnaire' not in session:
        flash('Accès réservé aux gestionnaires', 'danger')
        return redirect(url_for('connexion'))
    
    if request.method == 'POST':
        theme = request.form['theme']
        lieu_rdv = request.form['lieu_rdv']
        date_rdv = request.form['date_rdv']
        dparcours = request.form['dparcours']
        effectif_max = request.form['effectif_max']
        
        with db.connect_to_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO sortie (theme, lieu_rdv, date_rdv, dparcours, effectif_max)
                    VALUES (%s, %s, %s, %s, %s)
                """, (theme, lieu_rdv, date_rdv, dparcours, effectif_max))
                conn.commit()
        
        flash('Nouvelle sortie créée avec succès', 'success')
        return redirect(url_for('espace_gestionnaire'))
    
    return render_template('creer_sortie.html')


@app.route('/deconnexion')
def deconnexion():
    session.pop('id_adherent', None)
    flash('Vous êtes déconnecté.', 'info')
    return redirect(url_for('accueil'))

def reponse_especes_depuis_bdd(especes, max_especes=10, max_car=450):
    """
    Construit une réponse courte listant quelques espèces de l'association.
    especes : rows avec (nom_espece, groupe_nom)
    """
    especes = list(especes[:max_especes])
    if not especes:
        return "Aucune espèce n'est actuellement enregistrée dans la base de données."

    lignes = []
    for e in especes:
        lignes.append(f"- {e.nom_espece} ({e.groupe_nom})")
        texte_temp = " ".join(lignes)
        if len(texte_temp) > max_car:
            lignes.pop()
            break

    return (
        "Voici quelques espèces répertoriées par l'association :\n"
        + "\n".join(lignes)
        + "\nTu peux voir la liste complète dans la page « Espèces » du site."
    )


def reponse_sorties_depuis_bdd(sorties, max_sorties=10, max_car=450):
    """
    Construit une réponse courte listant quelques sorties de l'association.
    sorties : rows avec (theme, lieu_rdv, date_rdv)
    """
    sorties = list(sorties[:max_sorties])
    if not sorties:
        return "Aucune sortie n'est actuellement enregistrée dans la base de données."

    lignes = []
    for s in sorties:
        lignes.append(f"- {s.theme} à {s.lieu_rdv} le {s.date_rdv.strftime('%d/%m/%Y')}")
        texte_temp = " ".join(lignes)
        if len(texte_temp) > max_car:
            lignes.pop()
            break

    return (
        "Voici quelques sorties actuellement proposées par l'association :\n"
        + "\n".join(lignes)
        + "\nConsulte la page « Sorties » du site pour plus de détails ou t'inscrire."
    )


@app.route('/agent_faq', methods=['GET', 'POST'])
def agent_faq():
    if 'id_adherent' not in session:
        flash('Vous devez être connecté pour utiliser agent IA.', 'danger')
        return redirect(url_for('connexion'))

    question = None
    reponse = None

    if request.method == 'POST':
        question = request.form.get('question', '').strip()

        # mémoire courte
        if len(question.split()) <= 3 and 'derniere_question' in session:
            question_base = session['derniere_question'] + " " + question
        else:
            question_base = question

        q_lower = question_base.lower()

        # 1️⃣ Cas spécial : demande de sorties proposées
        if (
            ("quelles" in q_lower or "quels" in q_lower or "liste" in q_lower)
            and "sorties" in q_lower
        ) or (
            "sorties" in q_lower and "proposez" in q_lower
        ) or (
            "sorties" in q_lower and "propose" in q_lower
        ):
            with db.connect_to_db() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
                    cur.execute("""
                        SELECT theme, lieu_rdv, date_rdv
                        FROM sortie
                        ORDER BY date_rdv ASC
                        LIMIT 20
                    """)
                    sorties = cur.fetchall()

            reponse = reponse_sorties_depuis_bdd(sorties)

        # 2️⃣ Cas spécial : demande des espèces proposées
        elif (
            ("quelles" in q_lower or "quels" in q_lower or "liste" in q_lower)
            and ("espèces" in q_lower or "especes" in q_lower)
        ) or (
            ("espèces" in q_lower or "especes" in q_lower) and "propose" in q_lower
        ):
            with db.connect_to_db() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
                    cur.execute("""
                        SELECT e.nom AS nom_espece, g.nomge AS groupe_nom
                        FROM especes e
                        JOIN groupe_espece g ON e.idge = g.idge
                        ORDER BY e.nom
                        LIMIT 30
                    """)
                    especes = cur.fetchall()

            reponse = reponse_especes_depuis_bdd(especes)

        else:
            # 3️⃣ Tous les autres cas : FAQ + Mistral
            question_complete = question_base
            if question_complete:
                reponse = repondre_gemini(question_complete)

        # Mémoriser la question si elle est assez détaillée
        if len(question.split()) >= 3:
            session['derniere_question'] = question

    return render_template(
        'agent_faq.html',
        question=question,
        reponse=reponse
    )


@app.route('/agent_sortie', methods=['GET', 'POST'])
def agent_sortie():
    if 'id_adherent' not in session:
        flash('Vous devez être connecté pour utiliser l’agent de suggestion.', 'danger')
        return redirect(url_for('connexion'))

    suggestions = []
    message_agent = None

    if request.method == 'POST':
        theme = request.form.get('theme_pref', '').strip()
        distance = request.form.get('distance_pref')   # 'courte' ou 'longue'
        dispo = request.form.get('dispo_pref')         # 'proche' ou 'plus_tard'

        query = """
            SELECT s.*,
                   (s.effectif_max - COUNT(i.id_sortie)) AS places_disponibles,
                   COUNT(i.id_sortie) AS nombre_inscrits
            FROM sortie s
            LEFT JOIN inscrit i ON s.id_sortie = i.id_sortie
            WHERE s.date_rdv >= CURRENT_DATE
        """
        params = []

        if theme:
            query += " AND s.theme ILIKE %s"
            params.append(f'%{theme}%')

        if distance == 'courte':
            query += " AND s.dparcours <= 5"
        elif distance == 'longue':
            query += " AND s.dparcours > 5"

        if dispo == 'proche':
            query += " AND s.date_rdv <= CURRENT_DATE + INTERVAL '30 days'"
        elif dispo == 'plus_tard':
            query += " AND s.date_rdv > CURRENT_DATE + INTERVAL '30 days'"

        query += """
            GROUP BY s.id_sortie
            HAVING (s.effectif_max - COUNT(i.id_sortie)) > 0
            ORDER BY s.date_rdv
            LIMIT 5
        """

        with db.connect_to_db() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
                cur.execute(query, tuple(params))
                suggestions = cur.fetchall()

        if suggestions:
            message_agent = "Voici des sorties qui correspondent à tes préférences."
        else:
            message_agent = "Je n’ai trouvé aucune sortie avec ces critères. Essaie avec d’autres préférences."

    return render_template('agent_sortie.html',
                           suggestions=suggestions,
                           message_agent=message_agent)



if __name__ == '__main__':
    app.run(debug=True)
