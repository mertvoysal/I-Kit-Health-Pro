# I-Kit Health Pro - 2209-A Readiness

This document maps the current software to the 2209-A project goals and lists completion criteria.

## 1) Scope Alignment

- Project goal: AI-assisted early prediction of thyroid disease + specialist routing.
- Implemented in product:
  - Thyroid prediction endpoint (`/predict`) with CatBoost-based classification.
  - Input validation and medical threshold controls.
  - Specialist recommendation by specialty, distance and title score.
  - Live-location routing with road-distance fallback logic.

## 2) Method & Evaluation Outputs

- Evaluation script: `evaluate_2209a.py`
- Generated artifacts:
  - `artifacts/2209a_metrics.json`
  - `artifacts/2209a_metrics.md`
  - `artifacts/2209a_confusion_matrix.csv`
- Included metrics:
  - Holdout test: Accuracy, Precision (macro), Recall (macro), F1 (macro)
  - 5-fold stratified CV: mean/std summaries
  - Classification report and confusion matrix

## 3) Reproducibility

- Model metadata file:
  - `artifacts/model_metadata.json`
  - includes `model_version`, `trained_at`, and source metadata
- Model binary:
  - `artifacts/catboost_thyroid_model.cbm`
- Regeneration command:
  - `python evaluate_2209a.py`

## 4) Risk & B Plan (Technical)

- Risk: live route service unavailable
  - B plan: automatic fallback to haversine distance (`distance_source = live_location_fallback`)
- Risk: invalid/partial location payload
  - B plan: strict validation + district-based routing fallback
- Risk: metric drift over time
  - B plan: rerun `evaluate_2209a.py` on updated dataset and compare reports

## 5) Ethics & Safety Notes

- Product is a decision-support prototype, not a medical diagnosis authority.
- Input thresholds and laboratory range guards are enforced in backend.
- Recommendation output should be presented with advisory language in presentation/report.

## 6) Submission Checklist

- [x] Working prototype demo
- [x] Prediction + recommendation flow
- [x] Evaluation metrics (accuracy/precision/recall/F1)
- [x] Cross-validation summary
- [x] Confusion matrix artifact
- [x] Reproducible evaluation script
- [ ] Final narrative mapping software results to 2209-A sections in project report
- [ ] Final screenshots/figures for report appendix
