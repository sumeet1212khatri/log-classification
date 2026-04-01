import os
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

# ── Lazy-load models on first use (faster Spaces startup) ──────────────────
_embedding_model = None
_classifier = None

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "log_classifier.joblib")
CONFIDENCE_THRESHOLD = 0.3


def _load_models():
    global _embedding_model, _classifier
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    if _classifier is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. "
                "Run the Colab training notebook first and upload log_classifier.joblib."
            )
        _classifier = joblib.load(MODEL_PATH)


def classify_with_bert(log_message: str) -> tuple[str, float]:
    """
    Tier 2: BERT embedding + Logistic Regression classifier.
    Returns (label, confidence). Returns ('Unclassified', max_prob) if
    no class exceeds CONFIDENCE_THRESHOLD.
    Latency: ~20-80ms on CPU.
    """
    _load_models()

    embedding = _embedding_model.encode([log_message])
    probabilities = _classifier.predict_proba(embedding)[0]
    max_prob = float(np.max(probabilities))

    if max_prob < CONFIDENCE_THRESHOLD:
        return "Unclassified", max_prob

    predicted_label = _classifier.predict(embedding)[0]
    return predicted_label, max_prob


def get_classes() -> list[str]:
    """Return list of classes the BERT classifier knows."""
    _load_models()
    return list(_classifier.classes_)


if __name__ == "__main__":
    test_logs = [
        "GET /v2/servers/detail HTTP/1.1 status: 404 len: 1583 time: 0.19",
        "System crashed due to driver errors when restarting the server",
        "Multiple login failures occurred on user 6454 account",
        "Admin access escalation detected for user 9429",
        "CPU usage at 98% for the last 10 minutes on node-7",
        "Hey bro chill ya!",   # should be Unclassified
    ]
    for log in test_logs:
        label, conf = classify_with_bert(log)
        print(f"[{conf:.0%}] {label:25s} | {log[:70]}")
