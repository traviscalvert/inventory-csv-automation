
# Inventory CSV Automation Tool

A Python utility for cleaning, validating, and preparing retail inventory data for import into business systems.

## Business Problem

Retailers frequently receive inventory files containing duplicate products, inconsistent formatting, invalid prices, and incorrect inventory quantities.

Manually reviewing these files is time-consuming and prone to errors.

This tool automates common validation and cleanup tasks, producing import-ready records and a separate report identifying data that requires attention.

## Features

- Import inventory data from CSV files
- Normalize SKU formatting
- Remove unnecessary whitespace
- Detect duplicate SKUs
- Validate product prices
- Identify negative or invalid quantities
- Flag missing required information
- Generate clean inventory exports
- Generate detailed error reports
- Process different input files without modifying code

## Requirements

- Python 3.10 or newer
- No external Python packages required

## Usage

Place your inventory CSV inside the `input` folder.

The CSV must contain these columns:

SKU, Product Name, Price, Quantity, Category

Run:

    python inventory_cleaner.py sample_inventory.csv

Or process the default sample file:

    python inventory_cleaner.py

## Output

Processing `sample_inventory.csv` generates:

- `output/sample_inventory_clean.csv`
- `output/sample_inventory_errors.csv`

The clean file contains validated inventory records.

The error report identifies rejected records and explains why they require review.

## Demonstration

The included fictional sample inventory contains 10 records.

Results:

- 6 valid records
- 4 records requiring review

Detected issues include duplicate SKUs, invalid prices, negative quantities, and missing SKUs.

## Technologies

Python, CSV processing, data validation, command-line automation.

## Project Status

Functional portfolio demonstration.

Developed to illustrate practical business automation, data cleanup, and Python scripting capabilities.

The tool can be adapted to customer-specific inventory formats and validation requirements.
