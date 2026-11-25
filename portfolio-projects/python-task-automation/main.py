#!/usr/bin/env python3
"""Clean a customer CSV export and generate validation reports."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS = {"name", "email", "amount"}
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def normalize_row(row: dict[str, Any]) -> dict[str, str]:
    return {
        key.strip().lower(): (value or "").strip()
        for key, value in row.items()
        if key is not None
    }


def validate_row(row: dict[str, str]) -> tuple[dict[str, str] | None, str | None]:
    missing = [column for column in REQUIRED_COLUMNS if not row.get(column)]
    if missing:
        return None, "Missing required field(s): " + ", ".join(sorted(missing))

    email = row["email"].lower()
    if not EMAIL_RE.match(email):
        return None, "Invalid email address"

    try:
        amount = Decimal(row["amount"].replace(",", ""))
    except InvalidOperation:
        return None, "Amount is not numeric"

    if not amount.is_finite():
        return None, "Amount must be a finite number"

    cleaned = dict(row)
    cleaned["email"] = email
    cleaned["amount"] = f"{amount:.2f}"
    cleaned["name"] = " ".join(row["name"].split())
    return cleaned, None


def process_csv(input_path: Path, output_dir: Path) -> dict[str, int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    accepted: list[dict[str, str]] = []
    rejected: list[dict[str, str]] = []
    seen_emails: set[str] = set()
    counts: Counter[str] = Counter()

    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        headers = {header.strip().lower() for header in (reader.fieldnames or [])}
        missing_columns = REQUIRED_COLUMNS - headers
        if missing_columns:
            raise ValueError(
                "Input CSV is missing required columns: "
                + ", ".join(sorted(missing_columns))
            )

        for line_number, raw_row in enumerate(reader, start=2):
            counts["input_rows"] += 1
            row = normalize_row(raw_row)
            cleaned, error = validate_row(row)

            if error:
                rejected.append({
                    "line_number": str(line_number),
                    "reason": error,
                    **row,
                })
                counts["rejected_rows"] += 1
                continue

            assert cleaned is not None
            if cleaned["email"] in seen_emails:
                rejected.append({
                    "line_number": str(line_number),
                    "reason": "Duplicate email address",
                    **cleaned,
                })
                counts["duplicate_rows"] += 1
                counts["rejected_rows"] += 1
                continue

            seen_emails.add(cleaned["email"])
            accepted.append(cleaned)
            counts["accepted_rows"] += 1

    output_columns = sorted(
        {key for row in accepted for key in row}
        | {key for row in rejected for key in row if key not in {"line_number", "reason"}}
    )

    with (output_dir / "cleaned.csv").open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=output_columns)
        writer.writeheader()
        writer.writerows(accepted)

    rejected_columns = ["line_number", "reason"] + output_columns
    with (output_dir / "rejected.csv").open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=rejected_columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rejected)

    summary = {
        "input_rows": counts["input_rows"],
        "accepted_rows": counts["accepted_rows"],
        "rejected_rows": counts["rejected_rows"],
        "duplicate_rows": counts["duplicate_rows"],
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean a customer CSV and create validation reports."
    )
    parser.add_argument("input_csv", type=Path, help="Path to the input CSV file")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("output"),
        help="Directory for generated files (default: output)",
    )
    args = parser.parse_args()

    if not args.input_csv.is_file():
        parser.error(f"Input file does not exist: {args.input_csv}")

    try:
        summary = process_csv(args.input_csv, args.output_dir)
    except (OSError, ValueError, csv.Error) as exc:
        parser.error(str(exc))

    print(json.dumps(summary, indent=2))
    print(f"\nReports saved to: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
