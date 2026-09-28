# Transaction Parser

A Python-based CLI utility for parsing, validating, and cleaning financial transaction records from CSV files.
It ensures data integrity, skips broken records gracefully, and calculates summary financial metrics.

## Features

- **Strict Data Validation**: Enforces rules for user IDs, transaction types (`deposit`, `withdrawal`, `transfer`), and statuses (`SUCCESS`, `FAILED`, `PENDING`).
- **Graceful Error Handling**: Safely handles missing fields, broken CSV lines, and incorrect data types without crashing the application.
- **Metrics Aggregation**: Computes the net successful balance and provides data breakdowns by transaction type and status.
- **JSON Export**: Exports the strictly validated data and computed metrics into a structured JSON file.
- **Audit Logging**: Keeps track of skipped rows and systemic errors in `app.log`.

## Project Structure

```
parser_reincarnation/
├── .gitignore # Git ignore rules
├── __init__.py # Package marker
├── LICENCE # Project license
├── logger.py # Logging config
├── main.py # CLI entry point
├── models.py # Data models
├── processor.py # Parsing & metrics logic
├── README.md # Documentation
├── requirements.txt # Dependencies
├── test_parser.py # Test suite
└── validator.py # Validation logic
```

## Installation

The core application uses the Python 3 standard library and requires no external dependencies.
However, `pytest` is required to run the test suite.

1. Clone the repository:
   ```bash
   git clone [https://github.com/krinzhanovskyi/parсer_reincarnation.git](https://github.com/krinzhanovskyi/parсer_reincarnation.git)
   cd parсer_reincarnation
   ```
2. Install test dependencies:
   Bash
   ```
   pip install -r requirements.txt
   ```

## How to use parser

Run the script via the command line by specifying the input CSV file and the desired output JSON file path.
Bash

```
python main.py -i dirty_data/dirty_data.csv -o output/clean_result.json
```

**Arguments:**

- `-i`, `--input` : Path to the source CSV file.
- `-o`, `--output`: Path where the cleaned JSON file will be saved.

## Testing

The project includes parameterized automated tests to verify business logic against valid data, missing fields, and incorrect formats.
To execute the test suite with verbose output:
Bash

```
pytest test_parser.py -v
```
