import pandas as pd
from typing import Dict, Any


def analyze_transactions(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Runs basic statistical and behavioral analysis on transaction data.

    Args:
        df (pd.DataFrame): Transaction dataset.

    Returns:
        Dict[str, Any]: Summary metrics and aggregates.
    """
    summary = {
        "total_transactions": len(df),
        "total_amount": df["amount"].sum(),
        "average_amount": df["amount"].mean(),
        "median_amount": df["amount"].median(),
        "transactions_by_status": df["status"].value_counts().to_dict(),
        "transactions_per_day": (
            df["timestamp"]
            .dt.date
            .value_counts()
            .sort_index()
            .to_dict()
        ),
        "top_active_cards": (
            df["card_number"]
            .value_counts()
            .head(10)
            .to_dict()
        )
    }

    return summary
