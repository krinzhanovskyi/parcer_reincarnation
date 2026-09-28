from datetime import datetime
from typing import Dict, Optional

from logger import logger
from models import Transaction


def validate_and_clean_row(row: Dict[str, str], line_num: int) -> Optional[Transaction]:
    try:
        required_fields = ["timestamp", "user_id", "type", "amount", "status"]
        for field in required_fields:
            if field not in row or not row[field].strip():
                raise ValueError(f"required field is missing '{field}'")

        raw_time = row["timestamp"].strip()
        raw_user_id = row["user_id"].strip()
        raw_type = row["type"].strip().lower()
        raw_amount = row["amount"].strip()
        raw_status = row["status"].strip().upper()

        # dates
        parsed_dt = datetime.fromisoformat(raw_time)
        clean_time = parsed_dt.isoformat()

        # ID
        user_id = int(raw_user_id)
        if user_id <= 0:
            raise ValueError(f"user_id must be more then 0: {user_id}")

        # summ
        amount = float(raw_amount)

        # rules
        if raw_type not in {"deposit", "withdrawal", "transfer"}:
            raise ValueError(f"Unknown transaction type: '{raw_type}'")

        if raw_status not in {"SUCCESS", "FAILED", "PENDING"}:
            raise ValueError(f"Unknown status: '{raw_status}'")

        return Transaction(
            timestamp=clean_time,
            user_id=user_id,
            trans_type=raw_type,
            amount=amount,
            status=raw_status,
        )

    except Exception as exc:
        logger.warning("Line %d was skipped: %s (Data: %s)", line_num, exc, row)
        return None