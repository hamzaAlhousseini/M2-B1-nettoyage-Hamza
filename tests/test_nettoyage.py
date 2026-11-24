"""Tests des règles de nettoyage : un petit DataFrame construit à la main par règle."""

import pandas as pd

from nettoyage import (
    REGLES,
    imputer_enfants_manquants,
    nettoyer,
    supprimer_checkout_sans_nuit,
    supprimer_reservations_sans_adulte,
    supprimer_sans_occupant_et_sans_nuit,
)


def test_imputer_enfants_manquants():
    df = pd.DataFrame({"children": [0, None, 2, None]})

    out, touchees = imputer_enfants_manquants(df)

    assert out["children"].tolist() == [0, 0, 2, 0]
    assert touchees == 2
    assert df["children"].isna().sum() == 2   # l'entrée n'a pas été modifiée


def test_nettoyer_produit_un_compte_rendu():
    df = pd.DataFrame(
        {
            "reservation_id": [1, 2],
            "children": [None, 1],
            "adults": [1, 2],
            "babies": [0, 0],
            "stays_in_weekend_nights": [0, 1],
            "stays_in_week_nights": [1, 0],
            "reservation_status": ["Check-Out", "Check-Out"],
        }
    )

    out, compte_rendu = nettoyer(df)

    assert list(compte_rendu.columns) == ["regle", "lignes_touchees", "lignes_restantes"]
    assert len(compte_rendu) == len(REGLES)


def test_supprimer_reservations_sans_adulte_supprime_toutes_les_valeurs_hors_bornes():
    df = pd.DataFrame({"reservation_id": [1, 2, 3, 4], "adults": [0, 1, 10, 11]})

    out, touchees = supprimer_reservations_sans_adulte(df)

    assert out["reservation_id"].tolist() == [2, 3]
    assert out["adults"].tolist() == [1, 10]
    assert touchees == 2
    assert df["adults"].tolist() == [0, 1, 10, 11]


def test_supprimer_sans_occupant_et_sans_nuit():
    df = pd.DataFrame(
        {
            "reservation_id": [1, 2, 3],
            "adults": [0, 0, 1],
            "children": [0, 0, 0],
            "babies": [0, 0, 0],
            "stays_in_weekend_nights": [0, 0, 0],
            "stays_in_week_nights": [0, 0, 1],
        }
    )

    out, touchees = supprimer_sans_occupant_et_sans_nuit(df)

    assert out["reservation_id"].tolist() == [3]
    assert touchees == 2
    assert len(df) == 3


def test_supprimer_checkout_sans_nuit_ne_supprime_pas_annulations_ni_sejours_avec_nuit():
    df = pd.DataFrame(
        {
            "reservation_id": [1, 2, 3],
            "reservation_status": ["Check-Out", "Canceled", "Check-Out"],
            "stays_in_weekend_nights": [0, 0, 1],
            "stays_in_week_nights": [0, 0, 0],
        }
    )

    out, touchees = supprimer_checkout_sans_nuit(df)

    assert out["reservation_id"].tolist() == [2, 3]
    assert touchees == 1


def test_nettoyer_conserve_les_lignes_identiques_hors_reservation_id():
    df = pd.DataFrame(
        {
            "reservation_id": [10, 11, 12],
            "hotel": ["City", "City", "Resort"],
            "adults": [2, 2, 2],
            "children": [0, 0, 0],
            "babies": [0, 0, 0],
            "stays_in_weekend_nights": [0, 0, 0],
            "stays_in_week_nights": [1, 1, 1],
            "reservation_status": ["Check-Out", "Check-Out", "Check-Out"],
        }
    )

    out, compte_rendu = nettoyer(df)

    assert out["reservation_id"].tolist() == [10, 11, 12]
    assert len(compte_rendu) == len(REGLES)
