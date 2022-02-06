# Brief_CSV_to_DB
D'un CSV vers une base de données et l'affichage de ses données par requête.

Vous commencez votre mission, travail dans une nouvelle entreprise et on vous demande de créer une base données relationnelle à partir d'archive existante ainsi que de mettre en place un système d'affichage desdites données. Dans le brief actuel les archives sont simulées par un fichier CSV. Vous êtes libre d'utiliser la technologie que vous souhaitez pour créer la base de données et faire l'affichage des données. Le fichier CSV vous sera transmis en privé. Vous devez mettre en place tout le pipeline de la lecture du fichier CSV, de son nettoyage vers la création de la base de données relationel puis de l'affichage des données, récupérer par requête, en fonction des options disponibles par votre interface web.

## Installation

```bash
git clone https://github.com/julienbosse/Brief_CSV_to_DB.git
```

Il faut ensuite idéalement créer un environnement virtuel, puis installer les librairies nécessaires :

```bash
cd Brief_CSV_to_DB
python -m venv venv
```

Pour activer l'environnement : sur Windows
```bash
venv/Scripts/activate
```

ou sur Linux/MacOS :
```bash
source venv/bin/activate
```

Et terminer par :
```bash
pip install -r requirements.txt
```

## Explications

Le repo contient 3 dossiers :

- Data : contient les données sous forme de csv.
- Exploration : contient le notebook créé au début du brief pour explorer les données (nettoyage, tests...).
- Application : contient l'application web Flask qui une fois lancée crée la base de données et permet de faire des requêtes.

### Application

Pour créer la base de données, il est nécessaire de modifier le fichier 'Application/app/static/sql_credentials.json' qui renseigne les identifiants pour se connecter à MySQL.

```json

{
    "user":"yourUser",
    "password":"yourPassword",
    "host":"localhost"
}

```

Ensuite on peut lancer l'application :

```bash
cd Application
python app.py
```
