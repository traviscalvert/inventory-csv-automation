
import csv
import unittest

from inventory_cleaner import (
    BASE_DIR,
    OUTPUT_DIR,
    clean_inventory,
)


class TestInventoryCleaner(unittest.TestCase):

    def test_sample_inventory(self):
        input_file = BASE_DIR / "input" / "sample_inventory.csv"

        clean_inventory(input_file)

        clean_file = OUTPUT_DIR / "sample_inventory_clean.csv"
        error_file = OUTPUT_DIR / "sample_inventory_errors.csv"

        self.assertTrue(clean_file.exists())
        self.assertTrue(error_file.exists())

        with clean_file.open(newline="", encoding="utf-8") as file:
            clean_records = list(csv.DictReader(file))

        with error_file.open(newline="", encoding="utf-8") as file:
            error_records = list(csv.DictReader(file))

        self.assertEqual(len(clean_records), 6)
        self.assertEqual(len(error_records), 4)

        error_messages = " ".join(
            record["Issues"] for record in error_records
        )

        self.assertIn("Duplicate SKU", error_messages)
        self.assertIn("Invalid price", error_messages)
        self.assertIn("Invalid quantity", error_messages)
        self.assertIn("Missing SKU", error_messages)


if __name__ == "__main__":
    unittest.main()
