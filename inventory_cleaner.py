import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation
import argparse

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "input" / "sample_inventory.csv"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

FIELDS = ["SKU", "Product Name", "Price", "Quantity", "Category"]


def clean_inventory(input_file):
    valid_records = []
    errors = []
    seen_skus = set()
    CLEAN_FILE = OUTPUT_DIR / f"{input_file.stem}_clean.csv"
    ERROR_FILE = OUTPUT_DIR / f"{input_file.stem}_errors.csv"

    with input_file.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not set(FIELDS).issubset(reader.fieldnames):
            raise ValueError("Input file is missing required columns.")

        for row_number, row in enumerate(reader, start=2):
            record = {
                field: (row.get(field) or "").strip()
                for field in FIELDS
            }

            record["SKU"] = record["SKU"].upper()
            issues = []

            sku = record["SKU"]

            if not sku:
                issues.append("Missing SKU")
            elif sku in seen_skus:
                issues.append("Duplicate SKU")
            else:
                seen_skus.add(sku)

            try:
                price = Decimal(record["Price"])
                if not price.is_finite() or price < 0:
                    raise ValueError
                record["Price"] = f"{price:.2f}"
            except (InvalidOperation, ValueError):
                issues.append("Invalid price")

            try:
                quantity = int(record["Quantity"])
                if quantity < 0:
                    raise ValueError
                record["Quantity"] = str(quantity)
            except ValueError:
                issues.append("Invalid quantity")

            if not record["Product Name"]:
                issues.append("Missing product name")

            if issues:
                errors.append({
                    "Row": row_number,
                    **record,
                    "Issues": "; ".join(issues)
                })
            else:
                valid_records.append(record)

    with CLEAN_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(valid_records)

    with ERROR_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Row", *FIELDS, "Issues"]
        )
        writer.writeheader()
        writer.writerows(errors)

    print("Inventory processing complete!")
    print(f"Valid records: {len(valid_records)}")
    print(f"Records requiring review: {len(errors)}")
    print(f"Clean file: {CLEAN_FILE}")
    print(f"Error report: {ERROR_FILE}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean and validate inventory CSV files."
    )

    parser.add_argument(
        "filename",
        nargs="?",
        default="sample_inventory.csv",
        help="Name of the CSV file inside the input folder."
    )

    args = parser.parse_args()
    input_file = BASE_DIR / "input" / args.filename

    if not input_file.is_file():
        parser.error(f"Input file not found: {input_file}")

    clean_inventory(input_file)
