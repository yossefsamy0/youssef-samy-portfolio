import csv
import json
import tempfile
import unittest
from pathlib import Path

from main import process_csv


class ProcessCsvTests(unittest.TestCase):
    def test_processes_valid_invalid_and_duplicate_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "input.csv"
            output = root / "output"
            source.write_text(
                "name,email,amount\n"
                "Sara Ali,SARA@example.com,10\n"
                "Bad Email,not-an-email,20\n"
                "Sara Duplicate,sara@example.com,30\n",
                encoding="utf-8",
            )

            summary = process_csv(source, output)

            self.assertEqual(summary["input_rows"], 3)
            self.assertEqual(summary["accepted_rows"], 1)
            self.assertEqual(summary["rejected_rows"], 2)
            self.assertEqual(summary["duplicate_rows"], 1)
            self.assertTrue((output / "cleaned.csv").exists())
            self.assertTrue((output / "rejected.csv").exists())
            self.assertEqual(
                json.loads((output / "summary.json").read_text())["accepted_rows"],
                1,
            )

            with (output / "cleaned.csv").open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["email"], "sara@example.com")


if __name__ == "__main__":
    unittest.main()
