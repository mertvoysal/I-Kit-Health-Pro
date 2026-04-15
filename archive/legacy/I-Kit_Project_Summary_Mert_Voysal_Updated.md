# I-Kit Health Pro: Updated Executive Summary

**Primary Use:** Data Science MSc Application Portfolio  
**Project Origin:** TÜBİTAK 2209-A University Students Research Projects Support Program  
**Project Lead:** Mert Voysal  
**Role:** Project Manager & Lead Developer  
**Date:** 14 April 2026

---

## 1) Project Overview

I-Kit Health Pro is an AI-assisted thyroid decision-support system designed to improve early screening quality and specialist routing.  
The system analyzes core laboratory indicators (`TSH`, `FTI`, `T3/TT3`, `TT4`, `T4U`) together with demographic fields to estimate thyroid status and recommend suitable specialists.

The solution is designed as a **clinical support interface**, not as an autonomous diagnosis engine.

---

## 2) Technical Architecture

### Backend
- **Framework:** Flask
- **Core Libraries:** CatBoost, Scikit-learn, Pandas, NumPy
- **Endpoints:** prediction, model metadata/info
- **Model Lifecycle:** load-from-disk or train-and-save flow with metadata tracking

### Frontend
- **Stack:** Vanilla HTML/CSS/JS
- **UI Style:** Apple-inspired glassmorphism design system
- **UX Features:** loading overlay, toast notifications, responsive layout, interactive gauges

### Decision Layer Design
The engine combines:
1. **Probabilistic ML output** (CatBoost class probabilities),
2. **Deterministic medical guardrails** for biologically extreme values,
3. **Safety-first input validation** and threshold limits.

This hybrid setup reduces outlier-driven misclassification risk and improves practical reliability.

---

## 3) Data Processing & Model Workflow

- Missing numerical values are imputed with median values.
- Categorical values are encoded for model compatibility.
- Data is split into train/test with fixed random state.
- A CatBoost classifier is trained for 3-class thyroid outcome prediction:
  - Hyperthyroidism
  - Hypothyroidism
  - Healthy

---

## 4) Evaluation Results (Current Build)

Evaluation artifacts are generated via `evaluate_2209a.py` and stored in `artifacts/`.

### Holdout Test Metrics
- **Accuracy:** `0.9858`
- **Precision (macro):** `0.9341`
- **Recall (macro):** `0.8823`
- **F1 (macro):** `0.9055`

### 5-Fold Stratified Cross-Validation
- **Accuracy (mean ± std):** `0.9855 ± 0.0025`
- **Precision (macro, mean):** `0.9268`
- **Recall (macro, mean):** `0.9095`
- **F1 (macro, mean):** `0.9170`

### Generated Validation Files
- `artifacts/2209a_metrics.json`
- `artifacts/2209a_metrics.md`
- `artifacts/2209a_confusion_matrix.csv`

---

## 5) Specialist Routing Module

The recommendation layer ranks specialists by:
- clinical relevance (department),
- experience/title score,
- patient satisfaction,
- distance.

Distance mode supports:
- district-based fallback matrix,
- live location routing with road-distance API integration,
- automatic fallback if route service is unavailable.

---

## 6) Safety, Ethics, and Clinical Responsibility

The application explicitly communicates that:
- it is a **decision-support** tool,
- it does **not** establish medical diagnosis independently,
- final clinical responsibility belongs to licensed healthcare professionals.

Safety controls include:
- strict payload validation,
- laboratory bounds/threshold checks,
- deterministic safeguards for extreme endocrine patterns.

---

## 7) Personal Contribution Summary

As project lead, I designed and delivered:
- the end-to-end model + API architecture,
- deterministic safety guardrails,
- route-aware specialist recommendation logic,
- model reproducibility/evaluation pipeline,
- production-style UI/UX integration for real-world demo use.

---

## 8) Relevance to Data Science MSc Track

This project demonstrates:
- applied supervised learning in healthcare,
- hybrid ML + rule-based system design,
- model evaluation rigor (holdout + cross-validation),
- reproducibility and artifact management,
- practical productization from model to interactive end-user interface.

It reflects both **research discipline** and **deployment-oriented data science execution**.
