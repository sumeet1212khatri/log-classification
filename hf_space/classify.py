from __future__ import annotations
import pandas as pd
from processor_regex import classify_with_regex
from processor_bert import classify_with_bert
from processor_llm import classify_with_llm

LEGACY_SOURCE = "LegacyCRM"


def classify_log(source: str, log_msg: str) -> dict:
    """
    Route a single log through the 3-tier hybrid pipeline.

    Routing logic:
      - LegacyCRM  → Tier 3 (LLM) directly  [too few training samples for ML]
      - Others     → Tier 1 (Regex) first
                  → Tier 2 (BERT) if regex misses
                  → Tier 3 (LLM) if BERT confidence < 0.5

    Returns dict with keys: label, tier, confidence
    """
    if source == LEGACY_SOURCE:
        label = classify_with_llm(log_msg)
        return {"label": label, "tier": "LLM", "confidence": None}

    # Tier 1 — Regex
    label = classify_with_regex(log_msg)
    if label:
        return {"label": label, "tier": "Regex", "confidence": 1.0}

    # Tier 2 — BERT + LogReg
    label, confidence = classify_with_bert(log_msg)
    if label != "Unclassified":
        return {"label": label, "tier": "BERT", "confidence": confidence}

    # Tier 3 — LLM fallback (low-confidence BERT)
    label = classify_with_llm(log_msg)
    return {"label": label, "tier": "LLM (fallback)", "confidence": None}


def classify(logs: list[tuple[str, str]]) -> list[dict]:
    """Classify a list of (source, log_message) tuples."""
    return [classify_log(source, msg) for source, msg in logs]


def classify_csv(input_path: str, output_path: str = "output.csv") -> tuple[str, pd.DataFrame]:
    """
    Read a CSV with 'source' and 'log_message' columns,
    classify each row, write results to output_path.
    Returns (output_path, result_dataframe).
    """
    df = pd.read_csv(input_path)

    required = {"source", "log_message"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required}. Got: {set(df.columns)}")

    results = classify(list(zip(df["source"], df["log_message"])))
    df["predicted_label"] = [r["label"] for r in results]
    df["tier_used"]        = [r["tier"]  for r in results]
    df["confidence"]       = [
        f"{r['confidence']:.1%}" if r["confidence"] is not None else "N/A"
        for r in results
    ]

    df.to_csv(output_path, index=False)
    return output_path, df


if __name__ == "__main__":
    sample_logs = [
        ("ModernCRM",       "IP 192.168.133.114 blocked due to potential attack"),
        ("BillingSystem",   "User User12345 logged in."),
        ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
        ("ModernHR",        "GET /v2/servers/detail HTTP/1.1 status: 200 len: 1583 time: 0.19"),
        ("ModernHR",        "Admin access escalation detected for user 9429"),
        ("LegacyCRM",       "Case escalation for ticket ID 7324 failed because the assigned agent is no longer active."),
        ("LegacyCRM",       "The 'ReportGenerator' module will be retired in v4.0. Migrate to 'AdvancedAnalyticsSuite'."),
    ]

    print(f"{'Source':<20} {'Tier':<15} {'Conf':>6}  {'Label':<25} Log")
    print("─" * 110)
    for (source, log), result in zip(sample_logs, classify(sample_logs)):
        conf = f"{result['confidence']:.0%}" if result['confidence'] else " N/A"
        print(f"{source:<20} {result['tier']:<15} {conf:>6}  {result['label']:<25} {log[:45]}")
