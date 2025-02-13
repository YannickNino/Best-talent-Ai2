📝 Outil de Recrutement Intelligent
Best Talent AI est une application Streamlit qui aide les recruteurs à rédiger des offres d'emploi, analyser les CVs des candidats, afficher les meilleurs candidats pour l'offre et générer des questions d'entretien personnalisées. L'application utilise l'API Google Gemini pour l'analyse des textes et la génération de contenu.

Fonctionnalités
Rédaction d'offres d'emploi : Permet aux recruteurs de rédiger une offre d'emploi directement dans l'application.

Analyse des CVs : Chargez les CVs des candidats (format PDF) et obtenez une note sur 10 pour chaque candidat en fonction de l'offre d'emploi.

Top des candidats : Visualisez les  meilleurs candidats sous forme de graphique.

Questions d'entretien : Générez des questions d'entretien personnalisées pour chaque candidat en fonction de son CV et de l'offre d'emploi.

Prérequis
Avant de pouvoir utiliser cette application, assurez-vous d'avoir les éléments suivants :

Clé API Google Gemini :

Obtenez une clé API depuis Google AI Studio.

Ajoutez cette clé dans les secrets de Streamlit (st.secrets) ou dans un fichier .env.

Python 3.8 ou supérieur :

Assurez-vous que Python est installé sur votre machine.

Bibliothèques Python :

Installez les bibliothèques nécessaires en utilisant pip.

Installation
Clonez ce dépôt :

bash
Copy
git clone https://github.com/votre-utilisateur/votre-repo.git
cd votre-repo
Créez un environnement virtuel (optionnel mais recommandé) :

bash
Copy
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
Installez les dépendances :

bash
Copy
pip install -r requirements.txt
Configurez votre clé API :

Créez un fichier secrets.toml dans le dossier .streamlit (si vous utilisez Streamlit en local) :

toml
Copy
GOOGLE_API_KEY = "votre_clé_api_google"
Ou configurez les secrets directement sur Streamlit Sharing si vous déployez l'application.

Utilisation
Lancez l'application en local :

bash
Copy
streamlit run app.py
Suivez les étapes dans l'interface :

Rédigez une offre d'emploi dans la zone de texte.

Chargez les CVs des candidats (format PDF).

Visualisez les résultats des candidats sous forme de graphique.

Consultez les questions d'entretien générées pour chaque candidat.

Déploiement
Vous pouvez déployer cette application sur Streamlit Sharing ou Streamlit Community Cloud :

Créez un compte sur Streamlit Sharing.

Configurez les secrets de l'application avec votre clé API Google.

Déployez l'application en liant votre dépôt GitHub.

Structure du projet
Copy
.
├── app.py                  # Fichier principal de l'application
├── requirements.txt        # Liste des dépendances
├── README.md               # Ce fichier
├── .streamlit/             # Dossier pour les configurations Streamlit
│   └── secrets.toml        # Fichier des secrets (clé API)
└── CV/                     # Dossier pour stocker les CVs (optionnel)
Auteur
Yannick SONE SONE & Willy WAFFO

Contact : yannick.sone@groupe-esigelec.org & willy.waffo@groupe-esigelec.org

GitHub :YannickNino

Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

Remarques
Assurez-vous que les CVs téléchargés sont au format PDF pour une analyse optimale.

L'application utilise l'API Google Gemini, qui peut avoir des limites d'utilisation. Consultez la documentation officielle pour plus d'informations