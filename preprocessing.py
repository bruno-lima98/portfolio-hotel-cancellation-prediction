"""
preprocessing.py

Custom preprocessing transformer shared between train.py and predict.py.
Kept in its own module (not inline in train.py) so that joblib/pickle
records a stable, importable module path for this class -- regardless of
whether it's executed directly (python train.py), imported by Flask, or
loaded under Gunicorn (gunicorn predict:app). If this class lived inside
train.py, saved objects would reference it as living in "__main__" when
train.py is run directly, which breaks under Gunicorn (where predict.py is
imported as a module, not run as __main__).
"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class GBMCategoricalPreparer(BaseEstimator, TransformerMixin):
    """
    Learns each categorical column's categories only on Train (fit) and
    applies that same vocabulary on transform -- a category never seen in
    production becomes fillna_label instead of breaking the pipeline.
    """
    def __init__(self, feature_columns, categorical_columns, fillna_label=None):
        self.feature_columns = feature_columns
        self.categorical_columns = categorical_columns
        self.fillna_label = fillna_label

    def fit(self, X, y=None):
        self.categories_ = {}
        for col in self.categorical_columns:
            self.categories_[col] = X[col].astype("category").cat.categories
        return self

    def transform(self, X):
        X = X[self.feature_columns].copy()
        for col in self.categorical_columns:
            X[col] = pd.Categorical(X[col], categories=self.categories_[col])
            if self.fillna_label is not None:
                X[col] = X[col].astype("object").fillna(self.fillna_label)
        return X