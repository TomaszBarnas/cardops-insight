import pandas as pd
import os
from datetime import datetime

from typing import Dict, Any


def generate_report(summary: Dict[str, Any],
                    anomalies: pd.DataFrame,
                    output_dir: str = "output") -> None:
    """
    Generates a basic report including summary stats and anomalies,
    and saves them to CSV/Markdown files for review.

    Args:
        summary (dict): Result of the transaction analysis.
        anomalies (pd.DataFrame): Detected anomalies.
        output_dir (str): Folder to save the report to.
    """
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save summary to a Markdown file
    summary_path = os.path.join(output_dir, f"summary_{timestamp}.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# CardOps Insight Summary Report\n\n")
        for key, value in summary.items():
            f.write(f"## {key.replace('_', ' ').title()}\n")
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    f.write(f"- {subkey}: {subvalue}\n")
            else:
                f.write(f"{value}\n")
            f.write("\n")

    # Save anomalies to CSV
    if not anomalies.empty:
        anomalies_path = os.path.join(output_dir, f"anomalies_{timestamp}.csv")
        anomalies.to_csv(anomalies_path, index=False)
    else:
        empty_path = os.path.join(output_dir, f"anomalies_{timestamp}_EMPTY.txt")
        with open(empty_path, "w") as f:
            f.write("No anomalies detected.\n")
