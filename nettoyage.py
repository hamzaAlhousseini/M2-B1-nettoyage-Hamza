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

def supprimer_reservations_sans_adulte(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Supprime les réservations avec un nombre d'adultes hors de [1, 10].

    Les valeurs nulles ne sont pas concernées ; les bornes retenues sont celles de l'audit.
    """
    hors_bornes = df["adults"].lt(1) | df["adults"].gt(10)
    out = df.loc[~hors_bornes].copy()
    return out, int(hors_bornes.sum())


def supprimer_sans_occupant_et_sans_nuit(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Supprime les réservations sans adulte, enfant, bébé ni nuitée."""
    nuits = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    occupants = df["adults"].fillna(0) + df["children"].fillna(0) + df["babies"].fillna(0)
    sans_occupant_ni_nuit = occupants.eq(0) & nuits.eq(0)
    out = df.loc[~sans_occupant_ni_nuit].copy()
    return out, int(sans_occupant_ni_nuit.sum())


def supprimer_checkout_sans_nuit(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Supprime les séjours marqués Check-Out qui ne comportent aucune nuitée."""
    nuits = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    checkout_sans_nuit = df["reservation_status"].eq("Check-Out") & nuits.eq(0)
    out = df.loc[~checkout_sans_nuit].copy()
    return out, int(checkout_sans_nuit.sum())

def supprimer_reservations_enfant_seul(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Supprime les réservations indiquant 0 adulte et au moins 1 enfant.

    Une réservation avec des enfants mais sans adulte n'est pas cohérente pour ce jeu de données.
    """
    enfant_seul = df["adults"].eq(0) & df["children"].gt(0)
    out = df.loc[~enfant_seul].copy()
    return out, int(enfant_seul.sum())

# Ordre d'application. Ajoute tes règles ici.
REGLES = [
    imputer_enfants_manquants,
    supprimer_sans_occupant_et_sans_nuit,
    supprimer_checkout_sans_nuit,
    supprimer_reservations_sans_adulte,
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
