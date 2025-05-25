import pandas as pd
import os
from .errors import DataValidationError

REQUIRED_COLUMNS = {
    'transaction_id',
    'card_number',
    'amount',
    'currency',
    'timestamp',
    'status'
}


def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads and validates a CSV dataset of transactions.

    Args:
        filepath (str): Path to CSV file.

    Returns:
        pd.DataFrame: Parsed and validated transaction data.

    Raises:
        FileNotFoundError: If file does not exist.
        DataValidationError: If file is empty or missing columns.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        df = pd.read_csv(filepath)
    except Exception as exc:
        raise DataValidationError(f"Invalid or corrupted CSV file: {exc}")

    if df.empty:
        raise DataValidationError("Uploaded file is empty.")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise DataValidationError(f"Missing required columns: {', '.join(missing)}")

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    return df
