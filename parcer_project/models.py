from dataclasses import dataclass


@dataclass
class Transaction:
    timestamp: str
    user_id: int
    trans_type: str
    amount: float
    status: str