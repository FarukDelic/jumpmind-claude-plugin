---
name: foundation-data-schema
description: Understand and validate JMC Commerce foundation data schema relationships, foreign keys, and dependencies. Use when adding, modifying, or validating foundation CSV data files to ensure referential integrity and generate coherent test data across related tables.
allowed-tools: read_file, grep, search_replace
---

# Foundation Data Schema & Validation

Comprehensive understanding of JMC Commerce foundation data relationships, constraints, and dependencies. This skill enables Claude to generate valid, coherent test data that respects all foreign key relationships and business rules.

## When to Use

Use this skill when you need to:

-   **Add foundation data** - Ensure new records have valid parent references
-   **Generate test data** - Create realistic, coherent data sets across multiple tables
-   **Validate data** - Check referential integrity before committing changes
-   **Understand relationships** - Map dependencies between CSV files
-   **Debug data issues** - Trace foreign key violations or orphaned records

## Core Principles

### 1. Parent-Before-Child Rule

Always create parent records before child records:

-   Create **ITM_PRODUCT** before **ITM_ITEM**
-   Create **ITM_ITEM** before **ITM_SELLING_PRICE**
-   Create **CUST_CUSTOMER** before **SLS_ORDER**
-   Create **SLS_ORDER** before **SLS_ORDER_LINE_ITEM**

### 2. Foreign Key Validation

All foreign key values MUST reference existing records in parent tables.

### 3. Audit Fields

All tables include standard audit fields:

-   `CREATE_TIME` - Timestamp when record was created
-   `CREATE_BY` - User who created (usually "system" for foundation data)
-   `LAST_UPDATE_TIME` - Timestamp of last update
-   `LAST_UPDATE_BY` - User who last updated

**Standard values for foundation data:**

```csv
CREATE_TIME,2024-02-20 15:19:05.701
CREATE_BY,system
LAST_UPDATE_TIME,2024-02-20 15:19:05.701
LAST_UPDATE_BY,system
```

## Table Relationships

See [SCHEMA_MAP.md](SCHEMA_MAP.md) for complete relationship diagrams and field mappings.

## Validation Workflow

### Step 1: Identify Required Parent Records

Before adding data, determine what parent records must exist:

**Example - Adding a new item:**

```
New Item: ITEM_ID="NEW-ITEM-001"
└── Requires: PRODUCT_ID="NEW-PROD-001" (must exist in ITM_PRODUCT)
└── Requires: TAX_GROUP_ID="111" (must exist in TAX_GROUP)
```

### Step 2: Verify Parent Records Exist

Check if required parents exist:

```bash
# Check if product exists
grep "NEW-PROD-001" headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-product.csv

# Check if tax group exists
grep "^111," headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_tax-group.csv
```

### Step 3: Create Missing Parents

If parents don't exist, create them first (in correct order).

### Step 4: Add Child Record

Only after all parents exist, add the child record.

### Step 5: Validate Addition

Verify the new record and confirm no orphaned references.

## Common Validation Patterns

### Validating Item Data

```bash
# 1. Check PRODUCT_ID exists
grep "^\"${PRODUCT_ID}\"" post_01_itm-product.csv

# 2. Check TAX_GROUP_ID exists
grep "^${TAX_GROUP_ID}," post_01_tax-group.csv

# 3. Add item
# Add to post_01_itm-item.csv

# 4. Add selling price (references ITEM_ID + PRODUCT_ID)
# Add to post_01_itm-selling-price.csv
```

### Validating Order Data

```bash
# 1. Check CUSTOMER_ID exists
grep "^\"${CUSTOMER_ID}\"" post_01_cust-customer.csv

# 2. Add order (references CUSTOMER_ID)
# Add to post_01_sls-order.csv

# 3. Check ITEM_ID exists for line items
grep "^${ITEM_ID}," post_01_itm-item.csv

# 4. Add order line items (references ORDER_ID + ITEM_ID + PRODUCT_ID)
# Add to post_01_sls-order-line-item.csv
```

## Data Generation Guidelines

### Realistic IDs

Generate IDs that follow existing patterns:

**Items:**

-   Format: Numeric (e.g., `1210000251`) or SKU-based (e.g., `517212AGX0`)
-   Must be unique within ITM_ITEM

**Products:**

-   Format: Numeric (e.g., `432685`) or formatted (e.g., `0000-0001-01`)
-   Must be unique within ITM_PRODUCT

**Customers:**

-   Format: 16-digit numeric (e.g., `1052430130500000`)
-   Must be unique within CUST_CUSTOMER

**Orders:**

-   Format: Numeric string (e.g., `"8765309"`)
-   Must be unique within SLS_ORDER

### Realistic Values

**Prices:**

-   Use 2-3 decimal places: `59.950`, `31.190`
-   Reasonable ranges: $1.00 - $500.00 for most retail items

**Dates:**

-   Format: `YYYY-MM-DD HH:MM:SS.mmm`
-   Business dates: `YYYYMMDD`
-   Use realistic dates (not year 2000 for new data)

**Names and Descriptions:**

-   Use realistic product names from similar items
-   Include size/color/variant details in descriptions
-   Match naming conventions of existing records

**Quantities:**

-   Typically `1.000` for unit items
-   Use decimals with 3 places: `1.000`, `2.000`

**Tax Groups:**

-   Common values: `111`, `145`, `155`
-   Verify exists in TAX_GROUP table

## Field Validation Rules

### Required Fields

Most tables require:

-   Primary Key field (ITEM_ID, PRODUCT_ID, CUSTOMER_ID, ORDER_ID)
-   Audit fields (CREATE_TIME, CREATE_BY, LAST_UPDATE_TIME, LAST_UPDATE_BY)

### Optional Fields

Many fields can be empty (`""` or omitted), including:

-   LONG_DESCRIPTION
-   CLASSIFIER\_\* fields
-   TARE_WEIGHT
-   FAMILY_CODE
-   EXPIRATION_DATE

### Constrained Fields

**Boolean-like:**

-   `"0"` or `"1"` (not true/false)
-   Example: VOIDED, GIFT_RECEIPT, ITEM_RETURNABLE

**Enums/Codes:**

-   TYPE_CODE: `"STOCK"`, `"WARRANTY"`, `"SERVICE"`
-   SELLING_CHANNEL_CODE: `"STORE"`, `"ONLINE"`
-   ORDER_TYPE_CODE: `"BOPIS"`, `"SHIP_TO_HOME"`, `"IN_STORE"`
-   ITEM_TYPE: `"STOCK"`, `"SERVICE"`, `"FEE"`

## Common Errors and Fixes

### Error: Foreign Key Violation

**Symptom:** Child record references non-existent parent

```
ITEM_ID="NEW-001" references PRODUCT_ID="MISSING-PROD"
```

**Fix:** Create parent record first:

1. Add PRODUCT_ID="MISSING-PROD" to post_01_itm-product.csv
2. Then add ITEM_ID="NEW-001" to post_01_itm-item.csv

### Error: Duplicate Primary Key

**Symptom:** ID already exists in table

```
ITEM_ID="1210000251" already exists
```

**Fix:** Generate unique ID:

-   Check highest existing ID: `tail -1 post_01_itm-item.csv`
-   Increment or use different pattern

### Error: Missing Required Field

**Symptom:** Required field is empty

```
ITEM_ID is required but empty
```

**Fix:** Provide value for all required fields

### Error: Invalid Data Format

**Symptom:** Field value doesn't match expected format

```
CREATE_TIME="2024-01-01" (missing time component)
```

**Fix:** Use correct format: `2024-01-01 00:00:00.000`

## Integration vs IntelliJ Data

### Integration Profile

**Path:** `data/foundation/integration/`

**Purpose:** Integration test data, mock external system data

**When to use:**

-   Testing integrations
-   Simulating external system responses
-   Pre-populated store data

**Characteristics:**

-   Larger data sets
-   Realistic production-like data
-   Multiple customers, products, orders

### IntelliJ Profile

**Path:** `data/foundation/intellij/`

**Purpose:** Local development in IDE

**When to use:**

-   Quick local testing
-   Developer-specific test scenarios
-   Minimal data for fast startup

**Characteristics:**

-   Smaller, focused data sets
-   Developer test users
-   Minimal product catalog

## Best Practices

### 1. Plan Data Dependencies

Before adding data, map the full dependency chain:

```
Order → Customer (must exist)
Order Line Item → Order (must exist)
                → Item (must exist)
                → Product (must exist)
```

### 2. Generate Coherent Data Sets

When creating test scenarios, ensure all related data is coherent:

-   Order totals match line item sums
-   Dates are logically ordered
-   Customer data is internally consistent

### 3. Use Realistic Timestamps

Don't reuse ancient timestamps (year 2000). Use current/recent dates:

```csv
CREATE_TIME,2025-01-15 10:30:00.000
```

### 4. Maintain ID Uniqueness

Generate IDs that:

-   Follow existing patterns
-   Are guaranteed unique
-   Are memorable for testing (e.g., `TEST-ITEM-001`)

### 5. Document Custom Data

When adding custom test data, document the purpose in commit messages:

```
feat: Add test customer CUST-TEST-001 for loyalty testing
- Customer with Gold tier
- 5000 points balance
- Complete address and contact info
```

## Quick Reference

### Essential Tables

| Table                | Primary Key      | Common Foreign Keys           | Purpose                  |
| -------------------- | ---------------- | ----------------------------- | ------------------------ |
| ITM_PRODUCT          | PRODUCT_ID       | -                             | Product catalog (parent) |
| ITM_ITEM             | ITEM_ID          | PRODUCT_ID, TAX_GROUP_ID      | Sellable items/SKUs      |
| ITM_SELLING_PRICE    | SELLING_PRICE_ID | ITEM_ID, PRODUCT_ID           | Pricing rules            |
| ITM_SELLING_RULE     | -                | ITEM_ID                       | Selling constraints      |
| CUST_CUSTOMER        | CUSTOMER_ID      | -                             | Customer records         |
| CUST_EMAIL           | -                | CUSTOMER_ID                   | Customer emails          |
| CUST_ADDRESS         | -                | CUSTOMER_ID                   | Customer addresses       |
| CUST_LOYALTY_ACCOUNT | -                | CUSTOMER_ID                   | Loyalty program data     |
| SLS_ORDER            | ORDER_ID         | CUSTOMER_ID                   | Orders/transactions      |
| SLS_ORDER_LINE_ITEM  | -                | ORDER_ID, ITEM_ID, PRODUCT_ID | Order details            |
| TAX_GROUP            | TAX_GROUP_ID     | -                             | Tax categories           |
| TAX_JURISDICTION     | -                | -                             | Tax regions              |
| PRM_PROMOTION        | PROMOTION_ID     | -                             | Promotions               |
| PRM_REWARD           | REWARD_ID        | PROMOTION_ID                  | Promotion rewards        |

### File Naming Convention

```
post_01_{table-name}.csv
```

Examples:

-   `post_01_itm-item.csv` → ITM_ITEM table
-   `post_01_cust-customer.csv` → CUST_CUSTOMER table
-   `post_01_sls-order.csv` → SLS_ORDER table

The `post_01` prefix means:

-   `post` - Run after database schema updates
-   `01` - Execution order (lower numbers first)

## Examples

See [EXAMPLES.md](EXAMPLES.md) for complete examples of generating coherent test data with all dependencies.

## Validation Checklist

Before adding data, verify:

-   [ ] All parent records exist
-   [ ] All foreign keys are valid
-   [ ] Primary key is unique
-   [ ] Required fields are populated
-   [ ] Data formats match existing records
-   [ ] Timestamps use correct format
-   [ ] Audit fields are included
-   [ ] Enum values are valid
-   [ ] Related records are coherent (e.g., order totals match line items)
-   [ ] IDs follow existing patterns
