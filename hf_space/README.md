---
title: Log Classification System
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 🔍 Log Classification System

A **production-inspired hybrid log classification pipeline** that routes enterprise logs through 3 tiers — Regex → BERT + Logistic Regression → LLM — based on pattern confidence and source system.

## Architecture

```
Input Log
    │
    ├─► [Tier 1] Regex Classifier      → Fixed patterns (sub-ms latency)
    │         │ No match?
    │         ▼
    ├─► [Tier 2] BERT + LogReg         → High-confidence ML (conf > 0.5)
    │         │ Low confidence?
    │         ▼
    └─► [Tier 3] LLM (HF Inference)   → LegacyCRM / rare patterns
```

## Categories

| Category | Tier Used |
|---|---|
| User Action | Regex |
| System Notification | Regex |
| HTTP Status | BERT |
| Security Alert | BERT |
| Critical Error | BERT |
| Error | BERT |
| Resource Usage | BERT |
| Workflow Error | LLM |
| Deprecation Warning | LLM |

## Setup

### HuggingFace Spaces Secrets Required
- `HF_TOKEN` — your HuggingFace token (for LLM inference on LegacyCRM logs)

### Local Setup
```bash
pip install -r requirements.txt
python app.py
```

## Source Systems
- `ModernCRM`, `ModernHR`, `BillingSystem`, `AnalyticsEngine`, `ThirdPartyAPI` → Regex → BERT
- `LegacyCRM` → LLM directly (too few training samples for ML)

## Tech Stack
`sentence-transformers` · `scikit-learn` · `huggingface-hub` · `gradio` · `fastapi` · `pandas`
