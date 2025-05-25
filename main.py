from modules.data_loader import load_data
from modules.analyzer import analyze_transactions
from modules.anomaly_detector import detect_anomalies
from modules.report_generator import generate_report
from modules.logger import setup_logger
from modules.errors import DataValidationError


def main():
    logger = setup_logger()
    data_path = "data/transactions.csv"

    try:
        df = load_data(data_path)
        logger.info("Data loaded successfully.")
    except FileNotFoundError:
        logger.error("Input file not found.")
        return
    except DataValidationError as e:
        logger.error(f"Validation error: {e}")
        return
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return

    summary = analyze_transactions(df)
    logger.info("Transaction analysis completed.")

    anomalies = detect_anomalies(df)
    logger.info(f"Anomaly detection finished. Found {len(anomalies)} suspicious records.")

    generate_report(summary, anomalies)
    logger.info("Report generated and saved to /output.")


if __name__ == "__main__":
    main()
