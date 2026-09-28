import argparse
import json
from dataclasses import asdict
from pathlib import Path

from logger import logger
from processor import parse_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="console validator and parcer")
    parser.add_argument("-i", "--input", required=True, type=Path, help="path to the CSV")
    parser.add_argument("-o", "--output", required=True, type=Path, help="path to the JSON")
    args = parser.parse_args()

    if not args.input.exists():
        logger.error("file not found: %s", args.input)
        return

    logger.info("start: %s", args.input)
    transactions, metrics = parse_csv(args.input)

    output_data = {
        "summary": metrics,
        "transactions": [asdict(tx) for tx in transactions],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    logger.info("successfully saved to   %s", args.output)


if __name__ == "__main__":
    main()