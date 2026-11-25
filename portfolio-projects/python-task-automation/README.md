# Python Task Automation — Customer Data Cleaner

A small, reproducible Python automation project that cleans a customer CSV export, validates records, removes duplicate email addresses, and produces a JSON summary.

## What it does

- Reads a CSV file supplied by the user.
- Trims whitespace and normalizes email addresses.
- Validates required fields and email format.
- Converts the amount field to a numeric value.
- Keeps the first valid record for each email address.
- Writes `cleaned.csv`, `rejected.csv`, and `summary.json`.

## Run

Requires Python 3.10+ and uses only the Python standard library.

```bash
python main.py sample_data.csv --output-dir output
```

## Output files

- `cleaned.csv`: valid, normalized, unique records.
- `rejected.csv`: records that failed validation, with a reason.
- `summary.json`: input, accepted, rejected, and duplicate counts.

## Example

The included `sample_data.csv` is synthetic demonstration data. It contains no real customer information.

## Limitations

This is a local batch-processing utility, not a production CRM integration. Before using it with real data, confirm the required columns and validation rules with the data owner, and handle personal data according to the applicable privacy requirements.

## Skills demonstrated

Python, CSV processing, data validation, error handling, command-line interfaces, JSON reporting, and automation.
