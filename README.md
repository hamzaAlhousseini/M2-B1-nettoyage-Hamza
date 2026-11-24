# Escale Atlantique — Fiabiliser les données de réservation

> Squelette de départ du brief **M2-B1** (FastIA).

## Le contexte

Le modèle d'annulation v2 (M1-B1) a été entraîné sur des données jamais vérifiées. Ce projet audite la base de réservations, nettoie les anomalies avec des règles testées, et réentraîne le modèle (v2.1) pour mesurer ce que le nettoyage change.

## Structure

```
docker-compose.yml      # base PostgreSQL locale (la même qu'en M1-B1), sur le port 5433
.env.example            # à copier en .env
db/init/                # schéma + historique (juillet 2015 → décembre 2016)
notebooks/
  01_audit.ipynb        # audit de qualité (tâches 2-3) et comparaison des modèles (tâche 6)
nettoyage.py            # règles de nettoyage : une règle d'exemple, les autres à écrire (tâche 4)
tests/
  test_nettoyage.py     # le test de la règle d'exemple, les autres à écrire
train.py                # entraînement de référence (corrigé de M1-B1) : à brancher sur le nettoyage (tâche 5)
features.py             # variables calculées du modèle
model/
  cancellation_model_v2.0.0.joblib   # le modèle v2, entraîné sur les données brutes : la référence
  model_info_v2.0.0.json
  train_baseline.py                  # recette de la v1, pour mémoire
FICHE_DONNEES.md        # gabarit de la fiche du jeu de données (tâche 7)
NOTE_CLIENT.md           # gabarit de la note (tâche 7)
```

## Démarrage

```bash
cp .env.example .env
```

```bash
docker compose up -d
```

```bash
python -m venv .venv
```

```bash
.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
```

Vérifications :
- `python train.py` produit un modèle (version 2.0.0) : la chaîne d'entraînement fonctionne ;
- `pytest -v` : les 2 tests fournis passent ;
- le notebook `notebooks/01_audit.ipynb` s'ouvre avec le noyau `.venv` et sa première cellule affiche le nombre de réservations.

## Pièges de connexion (vus en M1-B1)

- **Mot de passe** : uniquement des lettres, des chiffres et `_`. Les caractères `@ : / % # ?` cassent l'URL de connexion.
- **Mot de passe modifié** après le premier démarrage : la base garde l'ancien. `docker compose down -v` puis `docker compose up -d`.
- **Port 5433 et `127.0.0.1`** : déjà réglés dans `.env.example`, pour éviter un PostgreSQL installé sur le poste et le passage par l'IPv6.
- **Après une modification du `.env`** : redémarrer le noyau du notebook.

## Données

Extrait de *Hotel Booking Demand* — N. Antonio, A. de Almeida, L. Nunes (2019), *Data in Brief* 22, 41-49. Licence CC BY 4.0. Les noms des établissements sont fictifs.
