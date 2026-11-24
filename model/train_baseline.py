"""Recette d'entraînement de la v1 — livrée par l'ancienne équipe data d'Escale Atlantique.

C'est le script qui a produit le modèle exposé en M0-B1. En M1-B1, tu ne le lances pas
tel quel : tu réutilises `build_pipeline()` et `FEATURES` pour « rejouer » la v1 sur
TON découpage (tâche 5), par exemple depuis un notebook :

    from model.train_baseline import build_pipeline, FEATURES, TARGET

À l'origine, la v1 a été entraînée sur un découpage aléatoire de toutes les données
2015-2017 : ses métriques d'origine ne sont donc pas comparables aux tiennes.
"""

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

CATEGORICAL_FEATURES = [
    "hotel",
    "arrival_date_month",
    "market_segment",
    "deposit_type",
    "customer_type",
    "country",
]
NUMERICAL_FEATURES = [
    "lead_time",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "adr",
    "previous_cancellations",
    "total_of_special_requests",
    "required_car_parking_spaces",
]
FEATURES = CATEGORICAL_FEATURES + NUMERICAL_FEATURES
TARGET = "is_canceled"


def build_pipeline() -> Pipeline:
    preprocessing = ColumnTransformer(
        transformers=[
            (
                "cat",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="constant", fill_value="Unknown")),
                        (
                            "encode",
                            OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=50),
                        ),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
            ("num", SimpleImputer(strategy="median"), NUMERICAL_FEATURES),
        ],
        sparse_threshold=0,
    )
    return Pipeline(
        [
            ("preprocessing", preprocessing),
            ("classifier", HistGradientBoostingClassifier(max_iter=200, random_state=42)),
        ]
    )
