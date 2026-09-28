from pathlib import Path
import pytest

from models import Transaction
from processor import parse_csv
from validator import validate_and_clean_row


def test_validate_and_clean_row_valid():
    raw_row = {
        "timestamp": "2026-03-01T12:00:00",
        "user_id": "10",
        "type": "deposit",
        "amount": "100.0",
        "status": "SUCCESS",
    }
    tx = validate_and_clean_row(raw_row, line_num=2)
    assert isinstance(tx, Transaction)
    assert tx.user_id == 10


def test_parse_csv_integration(tmp_path: Path):
    csv_content = (
        "timestamp,user_id,type,amount,status\n"
        "2026-03-01T10:00:00,1,deposit,500.0,SUCCESS\n"
        "2026-03-01T11:00:00,1,withdrawal,100.0,SUCCESS\n"
    )
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content, encoding="utf-8")

    txs, metrics = parse_csv(file_path)
    assert len(txs) == 2
    assert metrics["net_successful_balance"] == 400.0