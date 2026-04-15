import json
import os
from datetime import datetime, timezone

import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.preprocessing import LabelEncoder


DATA_PATH = "thyroidDF.csv"
ARTIFACTS_DIR = "artifacts"
JSON_REPORT_PATH = os.path.join(ARTIFACTS_DIR, "2209a_metrics.json")
MD_REPORT_PATH = os.path.join(ARTIFACTS_DIR, "2209a_metrics.md")
CONFUSION_PATH = os.path.join(ARTIFACTS_DIR, "2209a_confusion_matrix.csv")


def fix_target(value):
    letter = str(value)[0].upper()
    if letter in ["A", "B", "C", "D"]:
        return 0
    if letter in ["E", "F", "G", "H"]:
        return 1
    return 2


def prepare_dataset():
    df = pd.read_csv(DATA_PATH)
    df = df.drop(["TBG", "patient_id"], axis=1)
    df["target"] = df["target"].apply(fix_target)

    for col in ["TSH", "T3", "TT4", "T4U", "FTI"]:
        df[col] = df[col].fillna(df[col].median())
    df["sex"] = df["sex"].fillna(df["sex"].mode()[0])

    encoder = LabelEncoder()
    categorical_columns = df.select_dtypes(include=["object", "string"]).columns
    for col in categorical_columns:
        df[col] = encoder.fit_transform(df[col].astype(str))

    x = df.drop("target", axis=1)
    y = df["target"]
    return x, y


def evaluate_model(x, y):
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    model = CatBoostClassifier(verbose=0, random_state=42)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test).flatten().astype(int)

    test_metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision_macro": float(precision_score(y_test, y_pred, average="macro", zero_division=0)),
        "recall_macro": float(recall_score(y_test, y_pred, average="macro", zero_division=0)),
        "f1_macro": float(f1_score(y_test, y_pred, average="macro", zero_division=0)),
    }

    class_report = classification_report(
        y_test,
        y_pred,
        target_names=["Hyperthyroidism", "Hypothyroidism", "Healthy"],
        zero_division=0,
        output_dict=True,
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_validate(
        CatBoostClassifier(verbose=0, random_state=42),
        x,
        y,
        cv=cv,
        scoring=["accuracy", "precision_macro", "recall_macro", "f1_macro"],
        n_jobs=1,
    )

    cv_summary = {
        "accuracy_mean": float(cv_scores["test_accuracy"].mean()),
        "accuracy_std": float(cv_scores["test_accuracy"].std()),
        "precision_macro_mean": float(cv_scores["test_precision_macro"].mean()),
        "recall_macro_mean": float(cv_scores["test_recall_macro"].mean()),
        "f1_macro_mean": float(cv_scores["test_f1_macro"].mean()),
    }

    cm = confusion_matrix(y_test, y_pred, labels=[0, 1, 2])
    cm_df = pd.DataFrame(
        cm,
        index=["actual_hyper", "actual_hypo", "actual_healthy"],
        columns=["pred_hyper", "pred_hypo", "pred_healthy"],
    )

    report_payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_size": int(len(x)),
        "feature_count": int(x.shape[1]),
        "model": "CatBoostClassifier(random_state=42)",
        "split": {"test_size": 0.2, "random_state": 42, "stratified": True},
        "test_metrics": test_metrics,
        "cross_validation_5fold": cv_summary,
        "classification_report": class_report,
    }

    return report_payload, cm_df


def write_reports(report_payload, cm_df):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    with open(JSON_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2)

    cm_df.to_csv(CONFUSION_PATH, index=True)

    test_metrics = report_payload["test_metrics"]
    cv_metrics = report_payload["cross_validation_5fold"]
    md = f"""# 2209-A Model Performance Report

Generated (UTC): `{report_payload["generated_at_utc"]}`

## Dataset
- Samples: `{report_payload["dataset_size"]}`
- Features: `{report_payload["feature_count"]}`
- Model: `{report_payload["model"]}`

## Holdout Test Metrics
- Accuracy: `{test_metrics["accuracy"]:.4f}`
- Precision (macro): `{test_metrics["precision_macro"]:.4f}`
- Recall (macro): `{test_metrics["recall_macro"]:.4f}`
- F1 (macro): `{test_metrics["f1_macro"]:.4f}`

## 5-Fold Cross Validation (Stratified)
- Accuracy (mean +/- std): `{cv_metrics["accuracy_mean"]:.4f} +/- {cv_metrics["accuracy_std"]:.4f}`
- Precision (macro, mean): `{cv_metrics["precision_macro_mean"]:.4f}`
- Recall (macro, mean): `{cv_metrics["recall_macro_mean"]:.4f}`
- F1 (macro, mean): `{cv_metrics["f1_macro_mean"]:.4f}`

## Confusion Matrix
Saved at: `{CONFUSION_PATH}`
"""
    with open(MD_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(md)


if __name__ == "__main__":
    features, targets = prepare_dataset()
    report, confusion = evaluate_model(features, targets)
    write_reports(report, confusion)

    print("2209-A evaluation completed.")
    print(f"- JSON report: {JSON_REPORT_PATH}")
    print(f"- Markdown report: {MD_REPORT_PATH}")
    print(f"- Confusion matrix: {CONFUSION_PATH}")
