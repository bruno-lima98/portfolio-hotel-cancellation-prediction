"""
train.py

Trains the final hotel booking cancellation prediction model.

Reproduces the decisions already validated and documented in
work-book-documentation.md (Sections 1-12). This script does NOT recompute
EDA, feature selection, model comparison, or hyperparameter tuning -- those
decisions have already been made and are hardcoded below, with a reference
to the workbook section where each one was justified. The script only
reproduces the training of the final model from those decisions.
"""

import pandas as pd
import numpy as np
from preprocessing import GBMCategoricalPreparer
from sklearn.metrics import roc_auc_score
from catboost import CatBoostClassifier
import joblib
import os

# =============================================================================
# Configuration -- decisions already locked in the workbook, not recomputed here
# =============================================================================

DATA_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-11/hotels.csv"

# Section 6: usable booking_date window, after correcting for selection bias
WINDOW_START = "2015-01-01"
WINDOW_END = "2017-06-30"
OOT_CUTOFF = "2017-01-01"

# Section 6: final feature lists (Section 5 of the workbook -- AUC>=0.52 / IV>=0.02,
# minus assigned_room_type [leakage], arrival_date_year [non-generalization],
# distribution_channel [redundancy with market_segment])
NUMERICAL_COLUMNS_FINAL = [
    "lead_time", "total_of_special_requests", "booking_changes",
    "previous_cancellations", "required_car_parking_spaces", "adr",
    "arrival_date_week_number", "adults", "days_in_waiting_list",
    "stays_in_week_nights",
]
CATEGORICAL_COLUMNS_FINAL = [
    "deposit_type", "agent", "country", "market_segment",
    "customer_type", "company", "hotel", "reserved_room_type",
    "arrival_date_month",
]
FEATURES = NUMERICAL_COLUMNS_FINAL + CATEGORICAL_COLUMNS_FINAL

# Section 7: winning hyperparameters from Optuna tuning (trial #8/30)
BEST_PARAMS = {
    "learning_rate": 0.09435,
    "depth": 7,
    "l2_leaf_reg": 2.85624,
}
# Section 9: number of trees decided via early-stopping probe (85%/15% of Train)
ITERATIONS_FINAL = 128

RANDOM_STATE = 42

ARTIFACTS_DIR = "artifacts/models"
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "catboost_final_v1.cbm")
PREPROCESSOR_PATH = os.path.join(ARTIFACTS_DIR, "preprocessor_catboost_v1.pkl")


# =============================================================================
# Data pipeline -- Sections 3-4 of the workbook
# =============================================================================

def load_data():
    print(f"Loading data from {DATA_URL} ...")
    df = pd.read_csv(DATA_URL)
    print(f"  Raw shape: {df.shape}")
    return df


def clean_data(df):
    print("Cleaning and standardizing data (Section 3)...")

    df["agent"] = df["agent"].astype("string")
    df["company"] = df["company"].astype("string")
    df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"])

    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

    # target leakage -- Section 3/14
    df = df.drop(columns=["reservation_status", "reservation_status_date"])

    categorical_columns = list(df.dtypes[df.dtypes == "object"].index)
    for col in categorical_columns:
        df[col] = df[col].str.lower().str.strip().str.replace(" ", "_")

    # missing values -- Section 3.3: each one treated as its own category/information, not MCAR
    mode_children = df["children"].mode()[0]
    df["children"] = df["children"].fillna(mode_children)
    df["country"] = df["country"].fillna("unknown")
    df["agent"] = df["agent"].fillna("no_agency")
    df["company"] = df["company"].fillna("no_company")

    # outliers -- Section 3.4
    df["adr"] = df["adr"].abs()
    df["adr"] = df["adr"].clip(upper=500)

    df = df[~(df["adults"] > 5)].reset_index(drop=True)
    df = df[~(df["adults"] == 0)].reset_index(drop=True)

    print(f"  Shape after cleaning: {df.shape}")
    return df


def derive_booking_date(df):
    df["arrival_date"] = pd.to_datetime(
        df["arrival_date_year"].astype(str) + "-" +
        df["arrival_date_month"] + "-" +
        df["arrival_date_day_of_month"].astype(str),
        format="%Y-%B-%d",
    )
    df["booking_date"] = df["arrival_date"] - pd.to_timedelta(df["lead_time"], unit="D")
    return df


def filter_window_and_split(df):
    print(f"Filtering usable booking_date window ({WINDOW_START} to {WINDOW_END})...")
    window_mask = df["booking_date"].between(WINDOW_START, WINDOW_END)
    df = df[window_mask].reset_index(drop=True)
    print(f"  Shape after window filter: {df.shape}")

    print(f"OOT split (cutoff = {OOT_CUTOFF})...")
    df_train = df[df["booking_date"] < OOT_CUTOFF].reset_index(drop=True)
    df_test = df[df["booking_date"] >= OOT_CUTOFF].reset_index(drop=True)
    df_train = df_train.sort_values(by="booking_date", ascending=True).reset_index(drop=True)

    print(f"  Train: {df_train.shape} | Cancellation ratio = {df_train['is_canceled'].mean():.4f}")
    print(f"  Test:  {df_test.shape} | Cancellation ratio = {df_test['is_canceled'].mean():.4f}")

    return df_train, df_test


# =============================================================================
# Final model training -- Section 9 of the workbook
# =============================================================================

def train_final_model(X_train, y_train):
    print("Training final model (CatBoost, best_params + fixed iterations)...")

    preprocessor = GBMCategoricalPreparer(
        feature_columns=FEATURES,
        categorical_columns=CATEGORICAL_COLUMNS_FINAL,
        fillna_label="unseen",
    )

    X_train_prep = preprocessor.fit_transform(X_train)

    model = CatBoostClassifier(
        **BEST_PARAMS,
        iterations=ITERATIONS_FINAL,
        cat_features=CATEGORICAL_COLUMNS_FINAL,
        random_state=RANDOM_STATE,
        verbose=0,
        allow_writing_files=False,
    )
    model.fit(X_train_prep, y_train)

    return model, preprocessor


def run_sanity_check(model, preprocessor, X_test, y_test):
    """Quick check -- not the formal evaluation (that already lives in the
    notebook, Section 12), just confirms the training run reproduced a
    coherent result."""
    X_test_prep = preprocessor.transform(X_test)
    probs = model.predict_proba(X_test_prep)[:, 1]
    auc = roc_auc_score(y_test, probs)
    print(f"Sanity check -- Test AUC: {auc:.4f} (expected: ~0.8838)")


def save_artifacts(model, preprocessor):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    model.save_model(MODEL_PATH)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Preprocessor saved to: {PREPROCESSOR_PATH}")


# =============================================================================
# Execution
# =============================================================================

def main():
    df = load_data()
    df = clean_data(df)
    df = derive_booking_date(df)
    df_train, df_test = filter_window_and_split(df)

    y_train = df_train["is_canceled"]
    X_train = df_train.drop(columns="is_canceled")[FEATURES]

    y_test = df_test["is_canceled"]
    X_test = df_test.drop(columns="is_canceled")[FEATURES]

    model, preprocessor = train_final_model(X_train, y_train)
    run_sanity_check(model, preprocessor, X_test, y_test)
    save_artifacts(model, preprocessor)


if __name__ == "__main__":
    main()