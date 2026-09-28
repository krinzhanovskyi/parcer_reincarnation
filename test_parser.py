from pathlib import Path
import pytest

from models import Transaction
from processor import parse_csv
from validator import validate_and_clean_row

# A valid baseline row for testing
VALID_ROW = {
    "timestamp": "2026-03-01T12:00:00",
    "user_id": "10",
    "type": "deposit",
    "amount": "100.0",
    "status": "SUCCESS",
}

def test_validate_and_clean_row_valid():
    tx = validate_and_clean_row(VALID_ROW, line_num=2)
    
    assert isinstance(tx, Transaction)
    assert tx.user_id == 10
    assert tx.amount == 100.0
    assert tx.trans_type == "deposit"

# Testing all the dirty data cases requested by the coach
@pytest.mark.parametrize("mutations, expected_error_type", [
    ({"user_id": None}, "missing field"),                 # NoneType simulation from CSV
    ({"timestamp": "   "}, "empty field"),                 # Empty string simulation
    ({"amount": "НЕ_ЧИСЛО"}, "bad float cast"),           # Invalid type cast
    ({"user_id": "-5"}, "negative id not allowed"),       # Business logic violation
    ({"type": "unknown_type"}, "bad transaction type"),   # Invalid enum
    ({"status": "DONE"}, "bad status"),                   # Invalid enum
])
def test_validate_and_clean_row_invalid(mutations, expected_error_type):
    # Create a broken row by updating the valid baseline with mutated data
    broken_row = VALID_ROW.copy()
    broken_row.update(mutations)
    
    # The validator should gracefully return None instead of crashing
    tx = validate_and_clean_row(broken_row, line_num=2)
    assert tx is None, f"Validator should fail on {expected_error_type}"

def test_parse_csv_integration(tmp_path: Path):
    # Testing both valid and invalid rows in the CSV
    csv_content = (
        "timestamp,user_id,type,amount,status\n"
        "2026-03-01T10:00:00,1,deposit,500.0,SUCCESS\n"
        "2026-03-01T11:00:00,1,withdrawal,100.0,SUCCESS\n"
        "2026-03-01T12:00:00,1,transfer,50.0,SUCCESS\n"
        "bad_date_format,1,deposit,100.0,SUCCESS\n"  # This line should be skipped
    )
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content, encoding="utf-8")

    txs, metrics = parse_csv(file_path)
    
    assert len(txs) == 3
    assert metrics["invalid_rows_count"] == 1
    assert metrics["valid_rows_count"] == 3
    # 500 (deposit) - 100 (withdrawal) - 50 (transfer) = 350.0
    assert metrics["net_successful_balance"] == 350.0