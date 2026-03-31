# 🔍 Enterprise Hybrid Log Classification Pipeline

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/UI-Gradio-orange.svg)](https://gradio.app/)
[![HuggingFace](https://img.shields.io/badge/LLM-HuggingFace-yellow.svg)](https://huggingface.co/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![HuggingFace](https://img.shields.io/badge/LIVE-HuggingFace-blue.svg)]([https://huggingface.co/](https://huggingface.co/spaces/NOT-OMEGA/log-classification-system))

A highly optimized, production-grade log classification system designed to route enterprise application logs through a **3-Tier Cascade Architecture**. This system strikes the perfect balance between latency, compute cost, and classification accuracy by intelligently routing traffic between Regex, lightweight ML models (BERT), and Heavy LLMs.

---

## 🚀 The Problem & Solution

**The Problem:** Modern enterprises generate millions of logs across varied source systems (Modern CRMs, Legacy APIs, Billing engines). Routing all logs through pure Regex rules is fragile, while sending them to an LLM is extremely slow and cost-prohibitive.

**The Solution:** This pipeline implements a "Smart Bouncer" routing logic:
1. Fast, known patterns are handled instantly with zero compute footprint.
2. Moderate complexities are embedded and classified via a fine-tuned ML model.
3. Unknown anomalies and legacy system logs are dynamically escalated to a Large Language Model (Zero-Shot).

---

## 🏗️ 3-Tier Cascade Architecture

The routing logic automatically evaluates the source system and confidence thresholds to determine the execution path:

| Tier | Engine | Avg. Latency | Coverage | Trigger Condition |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1 🟢** | **Regex Engine** | `< 1 ms` | ~21% | Fixed structural patterns (e.g., standard logins, HTTP status). |
| **Tier 2 🔵** | **BERT + LogReg** | `20 - 80 ms` | ~79% | Complex structural variations. Uses `all-MiniLM-L6-v2`. |
| **Tier 3 🟡** | **LLM (HF API)** | `500 - 2000 ms`| ~0.3% | `LegacyCRM` source, or when Tier 2 confidence falls below **0.5**. |

---

## 📊 Performance Metrics

*Benchmarked on a synthetic dataset of 2,410 enterprise log records.*

* **End-to-End Latency:** `6.6 ms` (Average across all tiers)
* **Overall Accuracy:** `99.8%`
* **Tier 2 (ML) Cross-Validation F1-Score:** `99.4% ± 0.3%`
* **Categories Handled:** 9 functional labels (e.g., Security Alert, Critical Error, Workflow Error)
* **Compute Savings:** >99% reduction in LLM API calls compared to naive LLM routing.

---

## 🛠️ Tech Stack

* **Embeddings & ML:** `sentence-transformers`, `scikit-learn`
* **LLM Inference:** `huggingface-hub` (Inference API)
* **Data Processing:** `pandas`, `numpy`
* **User Interface:** `gradio`

---

### 💻 Usage Guide

1. Single Log Classification
Use the web interface to input a Source System and a Log Message. The system will display the predicted label, the tier used for computation, the confidence score, and the exact latency.

2. Batch CSV Processing
Upload a CSV containing source and log_message columns. The system will process the entire batch and return a classified CSV appending predicted_label, tier_used, and confidence, alongside a distribution summary.


## make log csv file run this code on google colab to generate csv file on google colab 


```

import csv
import random

# Teresystems ke sources
sources = ["ModernCRM", "ModernHR", "BillingSystem", "AnalyticsEngine", "ThirdPartyAPI", "LegacyCRM"]

# Tier 1: Regex logs (Fast & Standard)
regex_logs = [
    "User admin_{id} logged in.",
    "User staff_{id} logged out.",
    "GET /api/v2/data HTTP/1.1 status: 200 len: {length} time: 0.19",
    "Backup for database db_{id} completed successfully."
]

# Tier 2: BERT logs (Complex Errors / Usage)
bert_logs = [
    "System crashed due to disk I/O failure on node-{node}.",
    "Memory usage exceeded 95% on server-{node}.",
    "Multiple login failures occurred on user {id} account.",
    "Security alert: unauthorized access attempt from IP 192.168.1.{ip}.",
    "Database connection timeout after 5000ms."
]

# Tier 3: LLM logs (Legacy / Rare)
legacy_logs = [
    "Case escalation for ticket ID {length} failed — agent offline.",
    "The 'LegacyModule' feature will be deprecated in v5.0.",
    "Synchronization process stalled at step 4. Cannot proceed.",
    "Unknown workflow error encountered during batch processing."
]

data = []
# Generate exactly 200 logs
for i in range(200):
    source = random.choice(sources)
    
    # Routing logic ke hisaab se logs distribute karna
    if source == "LegacyCRM":
        template = random.choice(legacy_logs)
    elif random.random() < 0.3:  # 30% chance for Regex logs
        template = random.choice(regex_logs)
    else:                        # 70% chance for BERT logs
        template = random.choice(bert_logs)
        
    # Variables ko random numbers se replace karna
    msg = template.format(
        id=random.randint(100, 999),
        length=random.randint(1000, 9999),
        node=random.choice(["alpha", "beta", "gamma", "delta"]),
        ip=random.randint(10, 250)
    )
    
    data.append([source, msg])

# CSV file create karna
with open("test_logs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "log_message"])  # Headers jo tera Gradio app expect kar raha hai
    writer.writerows(data)

print("✅ test_logs.csv successfully generated with 200 logs!")

```

## 📂 Project Structure


```

├── app.py                  # Gradio UI and endpoint definitions
├── classify.py             # Core routing logic (The Traffic Police)
├── processor_regex.py      # Tier 1: Regex definitions and matchers
├── processor_bert.py       # Tier 2: MiniLM embeddings and LogReg inference
├── processor_llm.py        # Tier 3: HF API integration and prompt construction
├── requirements.txt        # Python dependencies
└── models/                 # Serialized scikit-learn model and scaler

```
