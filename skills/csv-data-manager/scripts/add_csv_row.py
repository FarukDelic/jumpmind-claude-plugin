#!/usr/bin/env python3
"""
CSV Row Addition Script
Validates CSV structure and appends new rows with proper formatting.
"""

import csv
import sys
import os
from typing import Dict, List, Any
import argparse


def read_csv_headers(csv_path: str) -> List[str]:
    """Read and return CSV headers."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        return headers


def validate_data(headers: List[str], data: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate that data matches CSV structure.
    Returns a dict with values in correct order.
    """
    # Check for extra columns
    extra_cols = set(data.keys()) - set(headers)
    if extra_cols:
        raise ValueError(f"Unknown columns: {', '.join(extra_cols)}")

    # Build row in correct column order
    validated_row = {}
    for header in headers:
        validated_row[header] = str(data.get(header, ""))

    return validated_row


def count_existing_rows(csv_path: str) -> int:
    """Count existing data rows (excluding header)."""
    with open(csv_path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f) - 1  # Subtract header row


def append_csv_row(csv_path: str, data: Dict[str, Any], verbose: bool = True) -> None:
    """
    Append a new row to CSV file with validation.

    Args:
        csv_path: Path to CSV file
        data: Dictionary mapping column names to values
        verbose: Print detailed output
    """
    # Read existing headers
    headers = read_csv_headers(csv_path)

    if verbose:
        print(f"📄 CSV File: {csv_path}")
        print(f"📋 Headers: {', '.join(headers)}")
        print(f"📊 Current rows: {count_existing_rows(csv_path)}")

    # Validate and order data
    validated_row = validate_data(headers, data)

    # Append row
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(validated_row)

    if verbose:
        print(f"✅ Successfully added new row")
        print(f"📊 Total rows now: {count_existing_rows(csv_path)}")
        print("\nAdded data:")
        for key, value in validated_row.items():
            if value:  # Only show non-empty values
                print(f"  {key}: {value}")


def parse_key_value_args(args: List[str]) -> Dict[str, str]:
    """
    Parse key=value arguments into a dictionary.
    Example: ['name=John', 'age=30'] -> {'name': 'John', 'age': '30'}
    """
    data = {}
    for arg in args:
        if "=" not in arg:
            raise ValueError(f"Invalid format: '{arg}'. Use key=value format")
        key, value = arg.split("=", 1)
        data[key] = value
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Add a new row to a CSV file with validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a row with specific columns
  %(prog)s data/products.csv name="Widget" price="19.99" sku="WDG-001"
  
  # Add a row to foundation data
  %(prog)s headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-item.csv \\
    itemId="NEW-ITEM-001" \\
    description="New Product" \\
    price="29.99"
  
  # Quiet mode (no output)
  %(prog)s data/customers.csv name="Alice" email="alice@example.com" --quiet
        """,
    )

    parser.add_argument("csv_file", help="Path to CSV file")
    parser.add_argument(
        "data",
        nargs="*",
        help="Data to add in key=value format (e.g., name=John age=30)",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress output messages"
    )
    parser.add_argument(
        "--show-headers", action="store_true", help="Only show CSV headers and exit"
    )

    args = parser.parse_args()

    try:
        # Show headers mode
        if args.show_headers:
            headers = read_csv_headers(args.csv_file)
            print(f"Headers for {args.csv_file}:")
            for i, header in enumerate(headers, 1):
                print(f"  {i}. {header}")
            print(f"\nTotal columns: {len(headers)}")
            return 0

        # Validate we have data to add
        if not args.data:
            parser.error(
                "No data provided. Use key=value format (e.g., name=John age=30)"
            )

        # Parse key=value arguments
        data = parse_key_value_args(args.data)

        # Add row
        append_csv_row(args.csv_file, data, verbose=not args.quiet)

        return 0

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"❌ Validation Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
