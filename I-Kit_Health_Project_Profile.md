# I-Kit Health Pro - Project Profile

**Applicant:** Mert Voysal  
**Target Use:** Academic and Professional Applications  
**Project Origin:** TUBITAK 2209-A (University Students Research Projects Support Program)  
**Role:** Project Manager and Lead Developer  
**Date:** April 2026
**One-Line Summary:** End-to-end AI-assisted thyroid decision-support platform with clinician-oriented safety, evaluation, and deployment design.

---

## Executive Overview

I-Kit Health Pro is an AI-assisted thyroid decision-support system developed to support early risk assessment and specialist routing in endocrine workflows.  
The platform combines machine learning inference with deterministic safety constraints to reduce outlier-driven errors and improve practical clinical usability.

The system is explicitly positioned as a **decision-support tool**, not an autonomous diagnostic authority.

### Live Demo
- Hugging Face Space: `https://huggingface.co/spaces/mertvoysal/I-Kit-Health-Pro`

---

## Problem Context

Thyroid disorders often require multi-parameter interpretation and careful threshold handling. In early-stage screening scenarios, this creates risk for delayed referral or inconsistent triage quality.  
I-Kit Health Pro addresses this by integrating:

- core lab markers (`TSH`, `FTI`, `TT3/T3`, `TT4`, `T4U`),
- demographic features,
- model-based classification,
- and route-aware specialist recommendation.

---

## Technical Architecture

### Backend and ML
- Flask API architecture for end-to-end inference and routing.
- CatBoost classifier for tabular thyroid outcome prediction.
- Scikit-learn based evaluation pipeline (holdout + cross-validation).
- Model artifact versioning and metadata tracking.

### Frontend and Productization
- Interactive web interface (HTML/CSS/JS), responsive for desktop/mobile.
- Decision-focused outputs: diagnosis category, confidence, and specialist ranking.
- Practical UX features: loading states, validation guardrails, and route-based recommendation display.

### Hybrid Safety Design
The system does not rely on a single black-box prediction layer.  
It uses:

1. probabilistic ML outputs, and  
2. deterministic medical guardrails for extreme endocrine cases.

This design improves reliability under biological outliers and incomplete panels.

---

## Evaluation and Validation

The evaluation framework is structured to support transparent and repeatable assessment.

### Holdout Test
- **Accuracy:** 0.9858
- **Precision (macro):** 0.9341
- **Recall (macro):** 0.8823
- **F1 (macro):** 0.9055

### Stratified 5-Fold Cross-Validation
- **Accuracy (mean +/- std):** 0.9855 +/- 0.0025
- **Precision (macro, mean):** 0.9268
- **Recall (macro, mean):** 0.9095
- **F1 (macro, mean):** 0.9170

---

## Routing and Real-World Utility

Specialist recommendation prioritizes:
- clinical department relevance,
- title/experience contribution,
- patient satisfaction,
- and distance.

Distance mode supports:
- district-based fallback,
- live location route calculation,
- and automatic fallback when external route services are unavailable.

---

## Ethics and Clinical Responsibility

The product includes explicit safety communication:
- it does not provide definitive medical diagnosis,
- it supports physician decision-making,
- final responsibility remains with licensed healthcare professionals.

Input range checks and threshold constraints are enforced before model inference.

---

## Personal Contribution

My direct contribution includes:
- project scoping and architecture,
- ML model integration and optimization,
- deterministic guardrail design,
- specialist ranking and routing logic,
- reproducibility and evaluation artifact pipeline,
- and final interface productization.

---

## Relevance

This project demonstrates:
- applied healthcare machine learning,
- robust evaluation discipline,
- hybrid model/rule system design,
- reproducible experimentation,
- and end-to-end deployment thinking from data to user-facing decision support.

It reflects both research rigor and engineering execution expected in a graduate-level data science track.

