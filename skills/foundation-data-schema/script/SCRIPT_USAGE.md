# Python Script: Add Customer Flow

This Python script automates adding a complete customer purchase scenario to foundation data with full dependency validation.

## What It Does

Adds a complete test scenario in the correct dependency order:

1. **Verifies TAX_GROUP exists** (145)
2. **Adds CUSTOMER** with:
   - Email address
   - Shipping address
   - Phone number
3. **Adds 2 PRODUCTS** each with:
   - ITM_PRODUCT record
   - ITM_ITEM record
   - ITM_SELLING_PRICE record
4. **Adds ORDER** with:
   - 2 line items (one for each product)
   - Correct totals calculated
   - All foreign keys valid

## Features

✅ **Dependency validation** - Verifies parents exist before adding children
✅ **Duplicate detection** - Checks if data already exists
✅ **Unique ID generation** - Generates IDs that don't conflict
✅ **Total calculation** - Automatically calculates order totals
✅ **Audit fields** - Adds proper CREATE_TIME, CREATE_BY fields
✅ **Format compliance** - Follows all CSV format rules

## Usage

### Basic Usage (Integration Data)

```bash
cd /Users/farukdelic/LocalDev/projects/jumpind/commerce

python .claude/skills/foundation-data-schema/add_customer_flow.py
```

This adds data to the default integration data path:
```
headless/point-of-sale/base/src/main/resources/data/foundation/integration/
```

### Custom Data Path

```bash
python .claude/skills/foundation-data-schema/add_customer_flow.py \
  --data-path headless/point-of-sale/base/src/main/resources/data/foundation/intellij
```

### Specify Customer ID

```bash
python .claude/skills/foundation-data-schema/add_customer_flow.py \
  --customer-id "1052430130599999"
```

### Custom Product Names

```bash
python .claude/skills/foundation-data-schema/add_customer_flow.py \
  --product1-name "Premium Widget" \
  --product2-name "Deluxe Gadget"
```

### Full Example

```bash
python .claude/skills/foundation-data-schema/add_customer_flow.py \
  --data-path headless/point-of-sale/base/src/main/resources/data/foundation/integration \
  --customer-id "1052430130599999" \
  --product1-name "Test Laptop" \
  --product2-name "Test Mouse"
```

## Output Example

```
============================================================
Adding Complete Customer Purchase Flow
============================================================

[1/4] Verifying tax group...
✓ Tax group 145 exists

[2/4] Adding customer...
✓ Added customer: 1052430130599999
  ✓ Added email
  ✓ Added address
  ✓ Added phone

[3/4] Adding products...
✓ Added product: TEST-PROD-12345
  ✓ Added item: TEST-PROD-12345-ITEM
  ✓ Added selling price: $45.990
✓ Added product: TEST-PROD-67890
  ✓ Added item: TEST-PROD-67890-ITEM
  ✓ Added selling price: $32.500

[4/4] Adding order...
✓ Added order: ORD-TEST-123456
  Subtotal: $78.49, Tax: $7.85, Total: $86.34
  ✓ Added line item 1: TEST-PROD-12345-ITEM - $45.990
  ✓ Added line item 2: TEST-PROD-67890-ITEM - $32.500

============================================================
✓ Successfully added complete customer flow!
============================================================

Summary:
  Customer ID: 1052430130599999
  Product 1: TEST-PROD-12345 (Item: TEST-PROD-12345-ITEM, Price: $45.990)
  Product 2: TEST-PROD-67890 (Item: TEST-PROD-67890-ITEM, Price: $32.500)
  Order ID: ORD-TEST-123456

Data added to: headless/point-of-sale/base/src/main/resources/data/foundation/integration
```

## What Gets Created

### Files Modified

- `post_01_cust-customer.csv` - Customer master record
- `post_01_cust-email.csv` - Customer email
- `post_01_cust-address.csv` - Customer address
- `post_01_cust-phone.csv` - Customer phone
- `post_01_itm-product.csv` - 2 product records
- `post_01_itm-item.csv` - 2 item records
- `post_01_itm-selling-price.csv` - 2 price records
- `post_01_sls-order.csv` - Order record
- `post_01_sls-order-line-item.csv` - 2 line item records

### Data Generated

**Customer:**
- 16-digit ID (auto-generated or specified)
- Email: `test.customer.XXXXXX@example.com`
- Address: `123 Test Street, TestCity, FL 12345`
- Phone: `555XXXXXXX`

**Products:**
- Product IDs: `TEST-PROD-XXXXX`
- Item IDs: `TEST-PROD-XXXXX-ITEM`
- Prices: Random between $10.00 - $100.00

**Order:**
- Order ID: `ORD-TEST-XXXXXX`
- Type: IN_STORE
- Status: PAID_IN_FULL
- Totals: Calculated from line items (10% tax)

## Validation

The script performs these validations:

### Before Adding

- ✓ Tax group 145 exists
- ✓ Customer ID is unique
- ✓ Product IDs are unique
- ✓ Item IDs are unique
- ✓ Order ID is unique

### After Adding

- ✓ All foreign keys reference existing records
- ✓ Product IDs match between item and selling price
- ✓ Tax group IDs match between item and line item
- ✓ Order totals calculated correctly
- ✓ Line item extended amounts = price × quantity

## Troubleshooting

### Error: Tax Group Not Found

```
✗ Tax group 145 not found!
```

**Solution:** Add tax group to `post_01_tax-group.csv` or verify the file exists.

### Error: Could Not Generate Unique ID

```
Could not generate unique ID after 1000 attempts
```

**Solution:** Too many test records exist. Consider cleaning up test data or using a different prefix.

### Error: File Not Found

```
FileNotFoundError: post_01_cust-customer.csv
```

**Solution:** Verify the `--data-path` points to a valid foundation data directory with all required CSV files.

## Run Multiple Times

The script is safe to run multiple times:

1. **First run:** Adds all new data
2. **Subsequent runs:** 
   - Generates new IDs for customer/products/order
   - Checks for conflicts
   - Only adds new data, never modifies existing

## Integration with Build

After running the script:

1. **Verify data:**
   ```bash
   tail -1 headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_sls-order.csv
   ```

2. **Build application:**
   ```bash
   ./gradlew build
   ```

3. **Run application:**
   - Use IntelliJ run configuration "Commerce Base (H2)"
   - New customer/products/order will be available

## Customization

To customize the script:

1. **Edit `add_customer_flow.py`**
2. **Modify generation logic:**
   - Customer data format
   - Product naming
   - Price ranges
   - Tax calculations
3. **Add more validation:**
   - Business rules
   - Field constraints
   - Cross-table validation

## Dependencies

**Python 3.6+** (no external libraries required - uses only standard library)

## Related

- **foundation-data-schema skill** - Understanding dependencies and validation
- **EXAMPLES.md** - Real data examples to reference
- **SCHEMA_MAP.md** - Field-by-field dependency mappings

This script implements the patterns and validations defined in the foundation-data-schema skill!

