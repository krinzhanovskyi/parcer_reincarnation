import logging
from datetime import datetime
from typing import Dict, Optional

from models import Transaction

# Get logger by name to avoid importing from logger.py and triggering side-effects
logger = logging.getLogger("transaction_parser")

def validate_and_clean_row(row: Dict[str, str], line_num: int) -> Optional[Transaction]:
    try:
        required_fields = ["timestamp", "user_id", "type", "amount", "status"]
        
        for field in required_fields:
            val = row.get(field)
            # val can be None if CSV structure is completely broken / missing commas
            if val is None or not str(val).strip():
                raise ValueError(f"Missing or empty required field: '{field}'")

        # Now it's safe to cast and strip
        raw_time = str(row.get("timestamp")).strip()
        raw_user_id = str(row.get("user_id")).strip()
        raw_type = str(row.get("type")).strip().lower()
        raw_amount = str(row.get("amount")).strip()
        raw_status = str(row.get("status")).strip().upper()

        parsed_dt = datetime.fromisoformat(raw_time)
        clean_time = parsed_dt.isoformat()

        user_id = int(raw_user_id)
        if user_id <= 0:
            raise ValueError(f"user_id must be positive, got: {user_id}")

        amount = float(raw_amount)

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

    # Catch only data validation/casting errors. 
    # Real code bugs (like KeyError, AttributeError) will crash the app as they should.
    except (ValueError, TypeError) as exc:
        logger.warning("Line %d skipped: %s (Data: %s)", line_num, exc, row)
        return None