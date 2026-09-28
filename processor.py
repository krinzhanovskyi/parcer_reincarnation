import csv
from pathlib import Path
from typing import Any, Dict, List, Tuple

from models import Transaction
from validator import validate_and_clean_row


def parse_csv(input_path: Path) -> Tuple[List[Transaction], Dict[str, Any]]:
    valid_transactions: List[Transaction] = []

    total_rows = 0
    invalid_rows = 0

    status_counts: Dict[str, int] = {}
    type_counts: Dict[str, int] = {}
    total_successful_balance = 0.0

    with input_path.open("r", encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)

        for line_num, row in enumerate(reader, start=2):
            total_rows += 1
            tx = validate_and_clean_row(row, line_num)

            if tx is None:
                invalid_rows += 1
                continue

            valid_transactions.append(tx)

            status_counts[tx.status] = status_counts.get(tx.status, 0) + 1
            type_counts[tx.trans_type] = type_counts.get(tx.trans_type, 0) + 1

            if tx.status == "SUCCESS":
                if tx.trans_type == "deposit":
                    total_successful_balance += tx.amount
                elif tx.trans_type in {"withdrawal", "transfer"}:
                    total_successful_balance -= tx.amount

    metrics = {
        "total_rows_processed": total_rows,
        "valid_rows_count": len(valid_transactions),
        "invalid_rows_count": invalid_rows,
        "net_successful_balance": round(total_successful_balance, 2),
        "status_breakdown": status_counts,
        "type_breakdown": type_counts,
    }

    return valid_transactions, metrics