"""Tests des règles de nettoyage : un petit DataFrame construit à la main par règle."""

import pandas as pd

from nettoyage import imputer_enfants_manquants, nettoyer


def test_imputer_enfants_manquants():
    df = pd.DataFrame({"children": [0, None, 2, None]})

    out, touchees = imputer_enfants_manquants(df)

    assert out["children"].tolist() == [0, 0, 2, 0]
    assert touchees == 2
    assert df["children"].isna().sum() == 2   # l'entrée n'a pas été modifiée


def test_nettoyer_produit_un_compte_rendu():
    df = pd.DataFrame({"children": [None, 1]})

    out, compte_rendu = nettoyer(df)

    assert list(compte_rendu.columns) == ["regle", "lignes_touchees", "lignes_restantes"]
    assert len(compte_rendu) == len(__import__("nettoyage").REGLES)


# TODO (tâche 4) : au moins un test par règle que tu ajoutes
