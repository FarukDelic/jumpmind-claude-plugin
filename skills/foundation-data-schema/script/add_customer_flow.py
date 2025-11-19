#!/usr/bin/env python3
"""
Add Complete Customer Purchase Flow to Foundation Data

This script adds a complete test scenario with proper dependency validation:
- Customer with email, address, phone
- 2 Products with items and pricing
- Order with 2 line items
- All totals calculated correctly
- Checks for existing data before adding

Usage:
    python add_customer_flow.py --data-path <path_to_foundation_data>
"""

import csv
import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import random


class FoundationDataManager:
    """Manages adding foundation data with dependency validation."""

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.000")
        self.audit_fields = {
            "CREATE_TIME": self.timestamp,
            "CREATE_BY": "system",
            "LAST_UPDATE_TIME": self.timestamp,
            "LAST_UPDATE_BY": "system",
        }

    def file_path(self, filename: str) -> str:
        """Get full path to CSV file."""
        return os.path.join(self.data_path, filename)

    def record_exists(self, filename: str, key_field: str, key_value: str) -> bool:
        """Check if record with key already exists."""
        filepath = self.file_path(filename)
        if not os.path.exists(filepath):
            return False

        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Handle quoted and unquoted fields
                row_value = row.get(key_field, "").strip('"')
                check_value = key_value.strip('"')
                if row_value == check_value:
                    return True
        return False

    def append_record(self, filename: str, record: Dict[str, str]) -> bool:
        """Append record to CSV file."""
        filepath = self.file_path(filename)

        # Read headers
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)

        # Prepare row in correct order
        row = []
        for header in headers:
            value = record.get(header, "")
            row.append(value)

        # Append row
        with open(filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        return True

    def generate_unique_id(
        self, filename: str, key_field: str, prefix: str, length: int = 10
    ) -> str:
        """Generate unique ID that doesn't exist in the file."""
        attempt = 0
        while attempt < 1000:
            # Generate ID with prefix and random number
            random_part = "".join(
                [str(random.randint(0, 9)) for _ in range(length - len(prefix))]
            )
            new_id = f"{prefix}{random_part}"

            if not self.record_exists(filename, key_field, new_id):
                return new_id

            attempt += 1

        raise Exception(
            f"Could not generate unique ID after 1000 attempts for {filename}"
        )

    def add_customer(self, customer_id: Optional[str] = None) -> str:
        """Add customer with email, address, and phone."""
        filename = "post_01_cust-customer.csv"

        # Generate or use provided customer ID
        if customer_id is None:
            customer_id = self.generate_unique_id(
                filename, "CUSTOMER_ID", "1052430130", 16
            )

        # Check if already exists
        if self.record_exists(filename, "CUSTOMER_ID", customer_id):
            print(f"✓ Customer {customer_id} already exists")
            return customer_id

        # Create customer record
        customer = {
            "CUSTOMER_ID": f'"{customer_id}"',
            "FIRST_NAME": '"Test"',
            "LAST_NAME": '"Customer"',
            "STATUS_CODE": "",
            "LOYALTY_NUMBER": f'"{customer_id[-7:]}"',  # Last 7 digits
            "LOYALTY_POINTS": '"0.000"',
            "BIRTHDAY": "1990-01-01 00:00:00.000",
            "BIRTH_MONTH": '"01"',
            "BIRTH_DAY_OF_MONTH": '"01"',
            "GENDER": "UNSPECIFIED",
            "MEMBER_TIER": "",
            "ORGANIZATION": '"0"',
            "ORGANIZATION_NAME": "",
            "OTHER_IDENTIFICATION": "",
            "PARENT_CUSTOMER_ID": "",
            "OPT_INTO_MARKETING_FLAG": "",
            "ADDITIONAL_INFO_JSON": "",
        }

        self.append_record(filename, customer)
        print(f"✓ Added customer: {customer_id}")

        # Add email
        email_record = {
            "CUSTOMER_ID": f'"{customer_id}"',
            "SEQUENCE_NUMBER": '"0"',
            "EMAIL": f'"test.customer.{customer_id[-6:]}@example.com"',
            "PRIMARY_EMAIL": '"1"',
            "EMAIL_TYPE": '"Personal"',
            "OPT_INTO_MARKETING_FLAG": '"1"',
        }
        self.append_record("post_01_cust-email.csv", email_record)
        print(f"  ✓ Added email")

        # Add address
        address_record = {
            "CUSTOMER_ID": f'"{customer_id}"',
            "SEQUENCE_NUMBER": '"0"',
            "ADDRESS_TYPE": '"SHIPPING_ADDRESS"',
            "ATTENTION": "",
            "LINE1": '"123 Test Street"',
            "LINE2": '""',
            "LINE3": "",
            "LINE4": "",
            "CITY": '"TestCity"',
            "STATE_ID": '"FL"',
            "COUNTRY_ID": '"US"',
            "POSTAL_CODE": '"12345"',
            "PRIMARY_ADDRESS_FLAG": '"1"',
            "LATITUDE": "",
            "LONGITUDE": "",
        }
        self.append_record("post_01_cust-address.csv", address_record)
        print(f"  ✓ Added address")

        # Add phone
        phone_record = {
            "CUSTOMER_ID": f'"{customer_id}"',
            "SEQUENCE_NUMBER": '"0"',
            "PHONE_NUMBER": f'"555{customer_id[-7:]}"',
            "PRIMARY_NUMBER": '"1"',
            "PHONE_NUMBER_TYPE": "",
            "PHONE_NUMBER_LABEL": "",
            "OPT_INTO_MARKETING_FLAG": '"1"',
        }
        self.append_record("post_01_cust-phone.csv", phone_record)
        print(f"  ✓ Added phone")

        return customer_id

    def verify_tax_group(self, tax_group_id: str = "145") -> bool:
        """Verify tax group exists."""
        if self.record_exists("post_01_tax-group.csv", "ID", tax_group_id):
            print(f"✓ Tax group {tax_group_id} exists")
            return True
        else:
            print(f"✗ Tax group {tax_group_id} not found!")
            return False

    def add_product(
        self, product_id: Optional[str] = None, name: str = "Test Product"
    ) -> Tuple[str, str, str]:
        """Add product with item and selling price. Returns (product_id, item_id, price)."""

        # Generate product ID if not provided
        if product_id is None:
            product_id = f"TEST-PROD-{random.randint(10000, 99999)}"

        # Check if product exists
        if self.record_exists("post_01_itm-product.csv", "PRODUCT_ID", product_id):
            print(f"✓ Product {product_id} already exists")
            # Try to find existing item and price
            return (product_id, None, None)

        # Add product
        product_record = {
            "PRODUCT_ID": f'"{product_id}"',
            "DESCRIPTION": f'"{name}"',
            "PRODUCT_COPY_ID": f'"{product_id}"',
            "CREATE_TIME": self.audit_fields["CREATE_TIME"],
            "CREATE_BY": self.audit_fields["CREATE_BY"],
            "LAST_UPDATE_TIME": self.audit_fields["LAST_UPDATE_TIME"],
            "LAST_UPDATE_BY": self.audit_fields["LAST_UPDATE_BY"],
            "CLASSIFIER_CLASS": "",
            "CLASSIFIER_STYLE": "",
            "CLASSIFIER_BRAND": "",
            "CLASSIFIER_DEPARTMENT": "",
        }
        self.append_record("post_01_itm-product.csv", product_record)
        print(f"✓ Added product: {product_id}")

        # Generate item ID
        item_id = f"{product_id}-ITEM"

        # Add item
        item_record = {
            "ITEM_ID": item_id,
            "ITEM_NAME": f'"{name}"',
            "DESCRIPTION": f'"{name}"',
            "LONG_DESCRIPTION": f'"{name}"',
            "TAX_GROUP_ID": "145",
            "TAX_EXEMPT_CODE": "0",
            "TYPE_CODE": "STOCK",
            "TARE_WEIGHT": "",
            "FAMILY_CODE": "",
            "EXPIRATION_DATE": "",
            "PRODUCT_ID": product_id,
            "ITEM_COPY_ID": "",
            "CLASSIFIER_COLOR": "",
            "CREATE_TIME": self.audit_fields["CREATE_TIME"],
            "CREATE_BY": self.audit_fields["CREATE_BY"],
            "LAST_UPDATE_TIME": self.audit_fields["LAST_UPDATE_TIME"],
            "LAST_UPDATE_BY": self.audit_fields["LAST_UPDATE_BY"],
        }
        self.append_record("post_01_itm-item.csv", item_record)
        print(f"  ✓ Added item: {item_id}")

        # Generate price (between $10 and $100)
        price = f"{random.randint(10, 100)}.{random.randint(0, 99):02d}0"

        # Add selling price
        price_record = {
            "SELLING_PRICE_ID": f'"{item_id}"',
            "EFFECTIVE_START_TIME": self.audit_fields["CREATE_TIME"],
            "ITEM_ID": f'"{item_id}"',
            "PRODUCT_ID": f'"{product_id}"',
            "PRICE_TYPE": "P",
            "LIST_PRICE": "0.000",
            "PRICE": price,
            "QUANTITY": "1.000",
            "COST": "",
            "EFFECTIVE_END_TIME": "",
            "CREATE_TIME": self.audit_fields["CREATE_TIME"],
            "CREATE_BY": self.audit_fields["CREATE_BY"],
            "LAST_UPDATE_TIME": self.audit_fields["LAST_UPDATE_TIME"],
            "LAST_UPDATE_BY": self.audit_fields["LAST_UPDATE_BY"],
            "TAG_APP_ID": "*",
            "TAG_BUSINESS_UNIT_ID": "*",
            "TAG_BRAND": "*",
            "TAG_DEVICE_ID": "*",
            "TAG_COUNTRY": "*",
            "TAG_STATE": "*",
            "TAG_STORE_TYPE": "*",
            "TAG_DEVICE_TYPE": "*",
        }
        self.append_record("post_01_itm-selling-price.csv", price_record)
        print(f"  ✓ Added selling price: ${price}")

        return (product_id, item_id, price)

    def add_order(self, customer_id: str, items: List[Tuple[str, str, str]]) -> str:
        """Add order with line items. items = [(product_id, item_id, price), ...]"""

        # Generate order ID
        order_id = f"ORD-TEST-{random.randint(100000, 999999)}"

        # Check if order exists
        if self.record_exists("post_01_sls-order.csv", "ORDER_ID", order_id):
            print(f"✓ Order {order_id} already exists")
            return order_id

        # Calculate totals
        subtotal = sum(float(price) for _, _, price in items)
        tax_rate = 0.10  # 10% tax
        tax_total = round(subtotal * tax_rate, 3)
        total = round(subtotal + tax_total, 3)

        business_date = datetime.now().strftime("%Y%m%d")

        # Add order
        order_record = {
            "ORDER_ID": f'"{order_id}"',
            "BUSINESS_DATE": f'"{business_date}"',
            "BUSINESS_UNIT_ID": '"05243"',
            "DEVICE_ID": "",
            "TAX_TOTAL_FOR_DISPLAY": "",
            "CUSTOMER_ID": f'"{customer_id}"',
            "SELLING_CHANNEL_CODE": '"STORE"',
            "LOYALTY_CARD_NUMBER": f'"{customer_id[-7:]}"',
            "TAX_EXEMPT_CUSTOMER_ID": "",
            "TAX_EXEMPT_CERTIFICATE": "",
            "TAX_EXEMPT_CODE": "",
            "EMPLOYEE_ID_FOR_DISCOUNT": "",
            "ISO_CURRENCY_CODE": '"USD"',
            "LINE_ITEM_COUNT": f'"{len(items)}"',
            "AGE_RESTRICTED_DATE_OF_BIRTH": "",
            "ITEM_COUNT": "",
            "CUSTOMER_NAME": "",
            "TENDER_TYPE_CODES": "",
            "VOIDABLE_FLAG": "",
            "TAX_GEO_CODE_ORIGIN": "",
            "ORDER_CUSTOMER_FIRST_NAME": "Test",
            "ORDER_CUSTOMER_LAST_NAME": "Customer",
            "ORDER_CUSTOMER_EMAIL": f'"test.customer.{customer_id[-6:]}@example.com"',
            "ORDER_CUSTOMER_PHONE_NUMBER": f'"555{customer_id[-7:]}"',
            "ORDER_CUSTOMER_ALTERNATE_NAME": "",
            "TOTAL": f'"{total:.3f}"',
            "PRE_TENDER_BALANCE_DUE": "",
            "SUBTOTAL": f'"{subtotal:.3f}"',
            "TAX_TOTAL": f'"{tax_total:.3f}"',
            "DISCOUNT_TOTAL": '"0.000"',
            "ORDER_TYPE_CODE": '"STORE_ORDER"',
            "PARENT_ORDER_ID": "",
            "ESTIMATED_AVAILABILITY_DATE": "",
            "ACTUAL_AVAILABILITY_DATE": "",
            "ORDER_DUE_DATE": "",
            "AMOUNT_DUE": "0.000",
            "PAYMENT_STATUS_CODE": '"PAID_IN_FULL"',
            "FULFILLING_BUSINESS_UNIT_ID": '"05243"',
            "HANDLING_METHOD_TYPE_CODE": "",
            "HANDLING_COST": "",
            "HANDLING_DATE": "",
            "HANDLING_DESCRIPTION": "",
            "EXPECTED_SHIP_DATE": "",
            "SURCHARGE": "",
            "DELIVERY_GROUP": "",
        }
        self.append_record("post_01_sls-order.csv", order_record)
        print(f"✓ Added order: {order_id}")
        print(
            f"  Subtotal: ${subtotal:.2f}, Tax: ${tax_total:.2f}, Total: ${total:.2f}"
        )

        # Add line items
        for seq, (product_id, item_id, price) in enumerate(items, 1):
            line_tax = round(float(price) * tax_rate, 3)

            line_item_record = {
                "ORDER_ID": f'"{order_id}"',
                "LINE_SEQUENCE_NUMBER": f'"{seq}"',
                "FULFILLING_BUSINESS_UNIT_ID": '"05243"',
                "ASSIGNMENT_STATUS": "",
                "VOIDED": '"0"',
                "OVERRIDE_USER_ID": "",
                "ENTRY_METHOD_CODE": '"SCANNED"',
                "POS_ITEM_ID": f'"{item_id}"',
                "ITEM_ID": f'"{item_id}"',
                "ITEM_DESCRIPTION": f'"Test Item {seq}"',
                "ITEM_TYPE": '"STOCK"',
                "REGULAR_UNIT_PRICE": f'"{price}"',
                "ACTUAL_UNIT_PRICE": f'"{price}"',
                "QUANTITY": '"1.000"',
                "EXTENDED_AMOUNT": f'"{price}"',
                "DISCOUNT_AMOUNT": '"0.000"',
                "EXTENDED_DISCOUNTED_AMOUNT": f'"{price}"',
                "RTN_EXTENDED_DISCOUNTED_AMOUNT": f'"{price}"',
                "TAX_AMOUNT": f'"{line_tax:.3f}"',
                "REASON_CODE_GROUP_ID": "",
                "REASON_CODE": "",
                "DISPOSITION_CODE": "",
                "GIFT_RECEIPT": '"0"',
                "ITEM_RETURNABLE": '"1"',
                "ITEM_TAXABLE": '"1"',
                "QUANTITY_AVAIL_FOR_RETURN": '"0.000"',
                "ITEM_DISCOUNTABLE": '"1"',
                "EMPLOYEE_DISCOUNT_ALLOWED": '"1"',
                "ITEM_PRICE_OVERRIDABLE": '"1"',
                "DISCOUNT_APPLIED": '"0"',
                "DAMAGE_DISCOUNT_APPLIED": '"0"',
                "TAX_INCLUDED_IN_PRICE": '"0"',
                "TAX_GROUP_ID": '"145"',
                "ORIG_LINE_SEQUENCE_NUMBER": "",
                "ORIG_SEQUENCE_NUMBER": "",
                "ORIG_BUSINESS_DATE": "",
                "ORIG_DEVICE_ID": "",
                "ORIG_ORDER_ID": "",
                "ORIG_USERNAME": "",
                "ORIG_BUSINESS_UNIT_ID": "",
                "RETURN_POLICY_ID": "",
                "ITEM_RETURNED": '"0"',
                "ISO_CURRENCY_CODE": '"USD"',
                "TARE_WEIGHT": "",
                "ITEM_WEIGHT": "",
                "ITEM_WEIGHT_PLUS_TARE": "",
                "WEIGHT_UNIT_OF_MEASURE": "",
                "WEIGHT_ENTRY_METHOD_CODE": "",
                "FAMILY_CODE": "",
                "ITEM_LENGTH": "",
                "LENGTH_UNIT_OF_MEASURE": "",
                "QUANTITY_MODIFIABLE": '"1"',
                "SAVE_VALUE": "",
                "SAVE_VALUE_TYPE": "",
                "COUPON_ALLOWED": '"1"',
                "USERNAME": "",
                "EXTERNAL_SYSTEM_ID": "",
                "PRODUCT_ID": f'"{product_id}"',
                "ITEM_NAME": f'"Test Item {seq}"',
                "ITEM_LONG_DESCRIPTION": f'"Test Item {seq}"',
                "ADDITIONAL_CLASSIFIERS": "",
                "TENDER_GROUP": '"IN_STORE"',
                "TENDER_AUTH_METHOD_CODE": '"CARD_PRESENT"',
                "ESTIMATED_AVAILABILITY_DATE": "",
                "ACTUAL_AVAILABILITY_DATE": "",
                "ORDER_ITEM_STATUS_CODE": '"COMPLETED"',
                "PACKAGE_LINE_SEQUENCE_NUMBER": "",
                "HANDLING_COST": "",
            }
            self.append_record("post_01_sls-order-line-item.csv", line_item_record)
            print(f"  ✓ Added line item {seq}: {item_id} - ${price}")

        return order_id


def main():
    parser = argparse.ArgumentParser(
        description="Add complete customer purchase flow to foundation data"
    )
    parser.add_argument(
        "--data-path",
        default="headless/point-of-sale/base/src/main/resources/data/foundation/integration",
        help="Path to foundation data directory",
    )
    parser.add_argument(
        "--customer-id", help="Optional: Specific customer ID to use (16 digits)"
    )
    parser.add_argument(
        "--product1-name", default="Test Product 1", help="Name for first product"
    )
    parser.add_argument(
        "--product2-name", default="Test Product 2", help="Name for second product"
    )

    args = parser.parse_args()

    # Initialize manager
    manager = FoundationDataManager(args.data_path)

    print("=" * 60)
    print("Adding Complete Customer Purchase Flow")
    print("=" * 60)

    try:
        # Step 1: Verify tax group exists
        print("\n[1/4] Verifying tax group...")
        if not manager.verify_tax_group("145"):
            print("✗ Tax group validation failed!")
            return 1

        # Step 2: Add customer with contact info
        print("\n[2/4] Adding customer...")
        customer_id = manager.add_customer(args.customer_id)

        # Step 3: Add products with items and pricing
        print("\n[3/4] Adding products...")
        product1 = manager.add_product(name=args.product1_name)
        product2 = manager.add_product(name=args.product2_name)

        items = [product1, product2]  # (product_id, item_id, price)

        # Step 4: Add order with line items
        print("\n[4/4] Adding order...")
        order_id = manager.add_order(customer_id, items)

        print("\n" + "=" * 60)
        print("✓ Successfully added complete customer flow!")
        print("=" * 60)
        print(f"\nSummary:")
        print(f"  Customer ID: {customer_id}")
        print(
            f"  Product 1: {product1[0]} (Item: {product1[1]}, Price: ${product1[2]})"
        )
        print(
            f"  Product 2: {product2[0]} (Item: {product2[1]}, Price: ${product2[2]})"
        )
        print(f"  Order ID: {order_id}")
        print(f"\nData added to: {args.data_path}")

        return 0

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
