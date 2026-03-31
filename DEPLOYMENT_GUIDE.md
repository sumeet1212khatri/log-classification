# 🚀 Deployment Guide — Log Classification System

## What's in this package

```
deploy/
├── hf_space/                  ← Upload entire folder to HuggingFace Space
│   ├── app.py                 ← Gradio UI (main app)
│   ├── classify.py            ← 3-tier routing logic
│   ├── processor_regex.py     ← Tier 1: Regex
│   ├── processor_bert.py      ← Tier 2: BERT + LogReg
│   ├── processor_llm.py       ← Tier 3: LLM via HF Inference API
│   ├── requirements.txt       ← Python dependencies
│   ├── README.md              ← HF Space metadata + docs
│   ├── synthetic_logs.csv     ← Dataset (for reference)
│   ├── test.csv               ← Sample test file
│   └── models/
│       └── log_classifier.joblib  ← Trained model (retrain in Colab first)
└── colab_training.ipynb       ← Run this first to get fresh model + metrics
```

---

## Step 1: Train in Google Colab (20 min)

1. Go to https://colab.research.google.com
2. File → Upload notebook → select `colab_training.ipynb`
3. Runtime → Change runtime type → T4 GPU
4. Run All cells (Ctrl+F9)
5. Cell 13 will auto-download:
   - `log_classifier.joblib` ← you need this
   - `confusion_matrix.png`  ← for README
   - `dataset_overview.png`  ← for README

---

## Step 2: Create HuggingFace Space (5 min)

1. Go to https://huggingface.co/new-space
2. Fill in:
   - **Space name**: `log-classification-system`
   - **SDK**: Gradio
   - **Visibility**: Public (for portfolio)
3. Click "Create Space"

---

## Step 3: Upload Files (5 min)

In your new Space, click "Files" tab → "Add file" → Upload files:

Upload ALL files from `hf_space/` folder:
- `app.py`
- `classify.py`
- `processor_regex.py`
- `processor_bert.py`
- `processor_llm.py`
- `requirements.txt`
- `README.md`
- `test.csv`
- `models/log_classifier.joblib`  ← use the one from Colab, not the original

---

## Step 4: Add HF Token Secret (2 min)

This is needed for LLM tier (LegacyCRM logs):

1. Space → Settings → Variables and secrets
2. Click "New secret"
3. Name: `HF_TOKEN`
4. Value: your HuggingFace token from https://huggingface.co/settings/tokens
5. Click Save

---

## Step 5: Verify Deployment

Your Space should be live at:
`https://huggingface.co/spaces/YOUR_USERNAME/log-classification-system`

Test with these logs:

| Source | Log | Expected |
|--------|-----|----------|
| ModernCRM | `User User123 logged in.` | User Action (Regex 🟢) |
| BillingSystem | `Multiple login failures occurred on user 6454` | Security Alert (BERT 🔵) |
| LegacyCRM | `Case escalation for ticket ID 7324 failed` | Workflow Error (LLM 🟡) |

---

## Troubleshooting

**Space shows "Building"**: Normal, takes 3-5 min on first deploy.

**Model not found error**: Make sure `models/log_classifier.joblib` is uploaded.

**LLM returns Unclassified**: Check HF_TOKEN secret is set correctly.

**Rate limit error**: HF Inference API has free tier limits. For production, upgrade or use Groq API key instead (set `GROQ_API_KEY` secret and update `processor_llm.py`).

---

## Resume Line (fill in your actual numbers from Colab)

```
Built a 3-tier hybrid log classification system (Regex → BERT + LogReg → LLM)
achieving XX% weighted F1 on 2,410 enterprise logs across 9 categories;
Regex tier routes ~21% of traffic at <1ms with 100% accuracy on fixed patterns,
reducing LLM API cost by 4x. Deployed on HuggingFace Spaces with Gradio UI
and CSV batch inference endpoint. Inspired by production system built at atck Technologies.
```
