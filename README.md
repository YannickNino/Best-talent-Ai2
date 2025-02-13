# 📝 Outil de Recrutement Intelligent

**Best Talent AI** est une application Streamlit qui aide les recruteurs à rédiger des offres d'emploi, analyser les CVs des candidats, afficher les meilleurs candidats pour l'offre et générer des questions d'entretien personnalisées. L'application utilise l'API Google Gemini pour l'analyse des textes et la génération de contenu.

## Fonctionnalités
**Rédaction d'offres d'emploi** : Permet aux recruteurs de rédiger une offre d'emploi directement dans l'application.

**Analyse des CVs** : Chargez les CVs des candidats (format PDF) et obtenez une note sur 10 pour chaque candidat en fonction de l'offre d'emploi.

**Top des candidats** : Visualisez les  meilleurs candidats sous forme de graphique.

**Questions d'entretien** : Générez des questions d'entretien personnalisées pour chaque candidat en fonction de son CV et de l'offre d'emploi.

## Prérequis
Avant de pouvoir utiliser cette application, assurez-vous d'avoir les éléments suivants :

1- **Clé API Google Gemini** :

Obtenez une clé API depuis [Google AI Studio](https://aistudio.google.com/apikey).

Ajoutez cette clé dans les secrets de Streamlit (`st.secrets`) ou dans un fichier `.env`.

2- **Python 3.8 ou supérieur** :

Assurez-vous que Python est installé sur votre machine.

3- **Bibliothèques Python** :

Installez les bibliothèques nécessaires en utilisant `pip`

## Installation
1- Clonez ce dépôt :
```
git clone https://github.com/votre-utilisateur/votre-repo.git
cd votre-repo
```
2 -Créez un environnement virtuel (optionnel mais recommandé) :

```
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```
3- Installez les dépendances :

```
pip install -r requirements.txt
```
4- Configurez votre clé API :

Créez un fichier `secrets.toml` dans le dossier `.streamlit` (si vous utilisez Streamlit en local) :

```
GOOGLE_API_KEY = "votre_clé_api_google"
Ou configurez les secrets directement sur Streamlit Sharing si vous déployez l'application.
```

## Utilisation
1- Lancez l'application en local :
```
streamlit run app.py
```
Suivez les étapes dans l'interface :

**Rédigez une offre d'emploi** dans la zone de texte.

**Chargez les CVs** des candidats (format PDF).

Visualisez les **résultats des candidats** sous forme de graphique.

Consultez les **questions d'entretien** générées pour chaque candidat.

## Déploiement
Vous pouvez déployer cette application sur **Streamlit Sharing** ou **Streamlit Community Cloud** :

1- Créez un compte sur [Streamlit Sharing](https://streamlit.io/).

2- Configurez les secrets de l'application avec votre clé API Google.

3- Déployez l'application en liant votre dépôt GitHub.

## Structure du projet
```
.
├── app.py                  # Fichier principal de l'application
├── requirements.txt        # Liste des dépendances
├── README.md               # Ce fichier
├── .streamlit/             # Dossier pour les configurations Streamlit
│   └── secrets.toml        # Fichier des secrets (clé API)
└── CV/                     # Dossier pour stocker les CVs (optionnel)
```
## Auteurs
Yannick SONE SONE & Willy WAFFO

## Contact : yannick.sone@groupe-esigelec.org & willy.waffo@groupe-esigelec.org

## GitHub :[YannickNino](https://github.com/YannickNino)

## Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

Remarques
Assurez-vous que les CVs téléchargés sont au format PDF pour une analyse optimale.

L'application utilise l'API Google Gemini, qui peut avoir des limites d'utilisation. Consultez la [documentation officielle](https://aistudio.google.com/prompts/new_chat?utm_source=google&utm_medium=cpc&utm_campaign=brand_gemini-eur-sem&utm_id=21341690381&gad_source=1&gclid=CjwKCAiAzba9BhBhEiwA7glbahFTds_jLFfFnt6A09BwExTPc0QBVfCLIaJuB2jTJdZIal5YJx1-HxoCETgQAvD_BwE) pour plus d'informations