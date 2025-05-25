import pandas as pd


KNOWN_STATUSES = {"approved", "declined", "reversed"}
MAX_AMOUNT_THRESHOLD = 10000
RAPID_TRANSACTION_THRESHOLD = 5  # More than 5 txns in 1 min = suspicious


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detects suspicious or malformed transactions based on simple heuristics.

    Args:
        df (pd.DataFrame): Transaction dataset.

    Returns:
        pd.DataFrame: Subset of rows flagged as anomalous.
    """
    anomalies = []

    # High-value or negative transactions
    amount_outliers = df[
        (df["amount"] < 0) | (df["amount"] > MAX_AMOUNT_THRESHOLD)
    ]
    anomalies.append(amount_outliers)

    # Invalid status values
    invalid_status = df[~df["status"].isin(KNOWN_STATUSES)]
    anomalies.append(invalid_status)

    # Non-parsable or missing timestamps
    invalid_dates = df[df["timestamp"].isna()]
    anomalies.append(invalid_dates)

    # High-frequency card activity (5+ txns within same minute)
    df["txn_minute"] = df["timestamp"].dt.floor("T")
    burst_activity = (
        df.groupby(["card_number", "txn_minute"])
        .size()
        .reset_index(name="txn_count")
    )
    flagged_minutes = burst_activity[
        burst_activity["txn_count"] > RAPID_TRANSACTION_THRESHOLD
    ]

    if not flagged_minutes.empty:
        suspicious_cards = df[df["card_number"].isin(flagged_minutes["card_number"])]
        anomalies.append(suspicious_cards)

    # Merge all unique flagged rows
    if anomalies:
        result = pd.concat(anomalies).drop_duplicates(subset=["transaction_id"])
        return result.reset_index(drop=True)

    return pd.DataFrame(columns=df.columns)
