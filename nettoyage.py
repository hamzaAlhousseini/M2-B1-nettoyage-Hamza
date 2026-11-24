"""Règles de nettoyage des réservations — Escale Atlantique (mission FastIA).

Une fonction par règle : elle reçoit un DataFrame, renvoie un NOUVEAU DataFrame (jamais modifié en place)
et le nombre de lignes qu'elle a touchées. `nettoyer()` les enchaîne et produit un compte rendu.

⚠️ `train.py` ne charge que les colonnes utiles au modèle (voir sa requête SQL). Une règle qui a besoin
d'une autre colonne impose de l'ajouter à la requête.
"""

import pandas as pd


# --- Exemple fourni : une règle, sa justification, son test (tests/test_nettoyage.py) -------------------

def imputer_enfants_manquants(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """`children` manquant → 0.

    Justification : quelques lignes seulement, et une réservation sans enfant renseigné est,
    de loin, le cas le plus fréquent. Décision réversible : la valeur d'origine est perdue,
    mais le compte rendu garde la trace du nombre de lignes concernées.
    """
    manquants = df["children"].isna()
    out = df.copy()
    out.loc[manquants, "children"] = 0
    return out, int(manquants.sum())


# --- TODO (tâche 4) : tes règles, une fonction chacune, sur le même modèle -------------------------------


# Ordre d'application. Ajoute tes règles ici.
REGLES = [
    imputer_enfants_manquants,
]


def nettoyer(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Applique toutes les règles dans l'ordre.

    Renvoie le DataFrame nettoyé et un compte rendu : une ligne par règle,
    avec le nombre de lignes touchées et le nombre de lignes restantes.
    """
    compte_rendu = []
    for regle in REGLES:
        df, touchees = regle(df)
        compte_rendu.append({"regle": regle.__name__, "lignes_touchees": touchees, "lignes_restantes": len(df)})
    return df, pd.DataFrame(compte_rendu)
