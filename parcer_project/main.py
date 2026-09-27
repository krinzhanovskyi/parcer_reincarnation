import argparse
import json
from dataclasses import asdict
from pathlib import Path

from logger import logger
from processor import parse_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Консольный валидатор и парсер транзакций")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Путь к исходному CSV")
    parser.add_argument("-o", "--output", required=True, type=Path, help="Путь для сохранения JSON")
    args = parser.parse_args()

    if not args.input.exists():
        logger.error("Входной файл не найден: %s", args.input)
        return

    logger.info("Старт обработки файла: %s", args.input)
    transactions, metrics = parse_csv(args.input)

    output_data = {
        "summary": metrics,
        "transactions": [asdict(tx) for tx in transactions],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    logger.info("Успешно сохранено в %s", args.output)


if __name__ == "__main__":
    main()