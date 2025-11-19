# Foundation Data Schema Skill

A comprehensive Claude Code Agent Skill for understanding, validating, and generating JMC Commerce foundation data with full referential integrity.

## Overview

This skill enables Claude to:
- **Understand table relationships** - Map parent-child dependencies and foreign keys
- **Validate data before adding** - Check foreign key constraints and required fields
- **Generate coherent test data** - Create realistic, production-ready data sets
- **Maintain referential integrity** - Ensure all cross-references are valid
- **Follow best practices** - Use correct formats, patterns, and conventions

## Key Difference from csv-data-manager

| Aspect | csv-data-manager | foundation-data-schema |
|--------|------------------|------------------------|
| **Focus** | Mechanical CSV row addition | Schema understanding & validation |
| **Approach** | Python script automation | Claude-driven validation & generation |
| **Validation** | Column name matching only | Full foreign key & business rule validation |
| **Data Generation** | Manual data provision | Intelligent, coherent data generation |
| **Dependencies** | Python script | Pure Claude knowledge |

**Use foundation-data-schema when:**
- Adding data that references other tables
- Creating complete test scenarios (customer + order + items)
- Need to validate foreign key relationships
- Want Claude to generate realistic test data
- Building coherent data sets across multiple files

**Use csv-data-manager when:**
- Simple, single-table additions
- All dependencies already verified
- Need automated script execution
- Adding bulk data programmatically

## Quick Start

### Ask Claude Naturally

Claude automatically uses this skill when you mention foundation data:

```
I need to add a new product with pricing to the integration data
```

```
Create a test customer with a BOPIS order for 2 items
```

```
Validate that ITEM_ID "NEW-001" has all required parent records
```

### Key Concepts

#### 1. Parent-Before-Child Rule

Always create parent records before children:

```
✅ Correct Order:
1. Create ITM_PRODUCT
2. Create ITM_ITEM (references product)
3. Create ITM_SELLING_PRICE (references item + product)

❌ Wrong Order:
1. Create ITM_ITEM
2. Create ITM_PRODUCT ← Too late! Item already created without valid parent
```

#### 2. Foreign Key Validation

Before adding a child record, verify parent exists:

```bash
# Adding item with PRODUCT_ID="PROD-001"
# First verify product exists:
grep "^\"PROD-001\"" post_01_itm-product.csv

# If not found → Create product first
# If found → Proceed with item
```

#### 3. Coherent Data Generation

Related data should be internally consistent:

```
✅ Coherent:
Order TOTAL = $100.00
Line Item 1: $60.00
Line Item 2: $40.00
Sum: $100.00 ← Matches!

❌ Incoherent:
Order TOTAL = $100.00
Line Item 1: $75.00
Line Item 2: $50.00
Sum: $125.00 ← Doesn't match!
```

## Files

```
.claude/skills/foundation-data-schema/
├── SKILL.md         # Skill definition (Claude reads this)
├── SCHEMA_MAP.md    # Complete table relationships & field specs
├── EXAMPLES.md      # Real-world generation examples
└── README.md        # This file
```

## Core Knowledge Areas

### Table Relationships

The skill provides complete understanding of:

**Product/Item Schema:**
- ITM_PRODUCT → ITM_ITEM → ITM_SELLING_PRICE
- Tax group references
- Image and option relationships

**Customer Schema:**
- CUST_CUSTOMER → CUST_EMAIL, CUST_ADDRESS, CUST_LOYALTY_ACCOUNT

**Order Schema:**
- CUST_CUSTOMER → SLS_ORDER → SLS_ORDER_LINE_ITEM
- Line item references to items and products

**Tax Schema:**
- TAX_GROUP, TAX_JURISDICTION, TAX_AUTHORITY

**Promotion Schema:**
- PRM_PROMOTION → PRM_QUALIFICATION, PRM_REWARD

See [SCHEMA_MAP.md](SCHEMA_MAP.md) for complete details.

### Validation Rules

**Foreign Keys:**
- All FK values must reference existing parent records
- Multi-FK records (e.g., line items) must have ALL parents valid

**Primary Keys:**
- Must be unique within table
- Should follow existing ID patterns

**Required Fields:**
- All PK fields
- Audit fields (CREATE_TIME, CREATE_BY, LAST_UPDATE_TIME, LAST_UPDATE_BY)
- Business-critical fields (varies by table)

**Data Formats:**
- Timestamps: `YYYY-MM-DD HH:MM:SS.mmm`
- Business dates: `YYYYMMDD`
- Decimals: 3 decimal places (e.g., `1.000`, `59.950`)
- Booleans: `"0"` or `"1"` (not true/false)

### Data Generation Patterns

**Realistic IDs:**
- Items: Numeric or SKU patterns (`1210000251`, `517212AGX0`)
- Products: Formatted strings (`"0000-0001-01"`, `"432685"`)
- Customers: 16-digit numbers (`"1052430130500000"`)
- Orders: Numeric strings (`"8765309"`)

**Realistic Values:**
- Prices: $1.00 - $500.00 for most items
- Names: Follow existing product naming conventions
- Dates: Use current/recent dates, not year 2000
- Descriptions: Include size/color/variant details

## Common Workflows

### Workflow 1: Add New Product

```
1. Verify TAX_GROUP exists (usually 111, 145, or 155)
2. Create ITM_PRODUCT record
3. Create ITM_ITEM record (references product + tax group)
4. Create ITM_SELLING_PRICE record (references item + product)
5. Validate complete chain
```

### Workflow 2: Create Customer Order

```
1. Verify CUST_CUSTOMER exists (or create)
2. Verify ITM_ITEM(s) exist for purchase
3. Calculate order totals (subtotal + tax)
4. Create SLS_ORDER record
5. Create SLS_ORDER_LINE_ITEM record(s)
6. Validate totals match
```

### Workflow 3: Complete Test Scenario

```
1. Create customer with email + loyalty account
2. Create product with item + pricing
3. Create order referencing customer
4. Create line items referencing order + items
5. Validate entire chain end-to-end
```

See [EXAMPLES.md](EXAMPLES.md) for complete, copy-paste examples.

## Integration vs IntelliJ Profiles

### Integration (`data/foundation/integration/`)

**Purpose:** Integration testing, simulated external data

**Characteristics:**
- Larger data sets (1000+ items, 50+ customers)
- Production-like data
- Multiple business scenarios

**When to use:**
- Testing integrations with external systems
- Load testing
- Realistic store simulation

### IntelliJ (`data/foundation/intellij/`)

**Purpose:** Local IDE development

**Characteristics:**
- Minimal data sets (10-20 items, 5-10 customers)
- Fast application startup
- Developer-specific test users

**When to use:**
- Quick local testing
- Feature development
- Debug specific scenarios

## Best Practices

### 1. Plan Before Adding

Map the complete dependency chain before creating any records:

```
Goal: Sellable item
Required:
├── TAX_GROUP (check exists)
├── ITM_PRODUCT (create)
├── ITM_ITEM (create)
└── ITM_SELLING_PRICE (create)
```

### 2. Validate Continuously

Check after each step:
- Record was added successfully
- Foreign keys are valid
- No duplicates created

### 3. Use Realistic Data

- Follow existing ID patterns
- Use current dates
- Generate meaningful names/descriptions
- Calculate accurate totals

### 4. Document Custom Data

Add commit messages explaining test data:

```bash
git commit -m "feat: Add test customer CUST-TEST-001 for loyalty testing

- Gold tier customer
- 5000 points balance
- Test data for loyalty redemption scenarios"
```

### 5. Keep Data Coherent

Ensure related records tell a consistent story:
- Customer name in order matches customer record
- Order totals match line item sums
- Dates are logically ordered

## Troubleshooting

### Foreign Key Violation

**Problem:** Child record references non-existent parent

**Solution:**
1. Identify the missing parent FK value
2. Create parent record first
3. Then create child record

### Duplicate Primary Key

**Problem:** ID already exists in table

**Solution:**
1. Check existing IDs: `tail -5 post_01_table.csv`
2. Generate unique ID following pattern
3. Verify uniqueness before adding

### Total Mismatch

**Problem:** Order total doesn't match line item sum

**Solution:**
1. Sum all line item amounts
2. Calculate total tax
3. Update order totals to match
4. Verify: TOTAL = SUBTOTAL + TAX_TOTAL - DISCOUNT_TOTAL

## Testing the Skill

After installation/modification, test with:

```
List all tables in the foundation data schema
```

```
What are the dependencies for creating a new order?
```

```
Generate a complete test customer with email and loyalty account
```

Claude should use the skill knowledge to provide accurate, detailed responses.

## Contributing

To enhance this skill:

1. **Update SKILL.md** - Core instructions for Claude
2. **Update SCHEMA_MAP.md** - Add new tables or fields
3. **Update EXAMPLES.md** - Add new scenarios or patterns
4. **Test thoroughly** - Verify Claude uses updated knowledge
5. **Commit & push** - Share with team via git

## Resources

- [SKILL.md](SKILL.md) - Complete skill definition
- [SCHEMA_MAP.md](SCHEMA_MAP.md) - Detailed schema documentation
- [EXAMPLES.md](EXAMPLES.md) - Real-world examples
- [Agent Skills Documentation](https://code.claude.com/docs/en/skills)

## License

Part of the JMC Commerce project.

