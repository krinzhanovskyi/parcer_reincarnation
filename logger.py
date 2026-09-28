import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from logger import setup_logger
from processor import parse_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Transaction validator and parser pipeline")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Path to the source CSV")
    parser.add_argument("-o", "--output", required=True, type=Path, help="Path to the target JSON")
    args = parser.parse_args()

    # Initialize logger only when running the actual app, not during test imports
    logger = setup_logger()

    if not args.input.is_file():
        logger.error("Input file not found or is a directory: %s", args.input)
        sys.exit(1)

    logger.info("Starting processing for: %s", args.input)
    
    try:
        transactions, metrics = parse_csv(args.input)
    except Exception as exc:
        logger.error("Critical error during parsing: %s", exc)
        sys.exit(1)

    output_data = {
        "summary": metrics,
        "transactions": [asdict(tx) for tx in transactions],
    }

    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
    except OSError as exc:
        logger.error("Failed to write output file %s: %s", args.output, exc)
        sys.exit(1)

    logger.info("Successfully processed %d valid transactions. Saved to %s", metrics["valid_rows_count"], args.output)


if __name__ == "__main__":
    main()