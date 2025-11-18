---
name: csv-data-manager
description: Add new rows to CSV files with automatic header validation and column mapping. Use when adding data to CSV files, foundation data files, integration test data, or any comma-separated data files. Validates column names and maintains proper CSV formatting.
allowed-tools: read_file, write, run_terminal_cmd
---

# CSV Data Manager

Safely add new rows to CSV files with automatic validation and formatting. This skill ensures data integrity by validating column names against existing headers and maintaining proper CSV structure.

## When to Use

Use this skill when you need to:
- Add new foundation data rows (e.g., `post_01_*.csv` files)
- Insert test data into CSV files
- Append records to integration data files
- Add configuration data in CSV format
- Maintain data consistency across CSV files

## Instructions

### Step 1: Inspect CSV Structure

Before adding data, review the CSV file structure:

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py path/to/file.csv --show-headers
```

This shows all available columns and helps you understand what data fields are needed.

### Step 2: Prepare Data

Organize data as key=value pairs matching the CSV column names exactly. Column names are case-sensitive.

### Step 3: Add Row

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py path/to/file.csv \
  column1="value1" \
  column2="value2" \
  column3="value3"
```

The script will:
1. ✅ Validate column names exist in the CSV
2. ✅ Check data format compatibility
3. ✅ Maintain proper CSV escaping for special characters
4. ✅ Preserve file encoding (UTF-8)
5. ✅ Append data to the end of the file

### Step 4: Verify Addition

The script outputs confirmation with:
- Current row count before addition
- New row count after addition
- Summary of added data

## Common Use Cases

### Foundation Data Files

For files in `headless/point-of-sale/base/src/main/resources/data/foundation/`:

```bash
# Add a new item
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-item.csv \
  itemId="NEW-SKU-123" \
  description="New Product Name" \
  price="29.99" \
  active="true"

# Add a new customer
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_cust-customer.csv \
  customerId="CUST-9999" \
  firstName="John" \
  lastName="Doe" \
  email="john.doe@example.com"
```

### Integration Test Data

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/intellij/post_01_usr-user.csv \
  userId="testuser123" \
  username="testuser" \
  password="encrypted_password"
```

## Validation Rules

The script enforces these rules:

1. **Column Name Matching**: All data keys must match existing CSV headers exactly
2. **Unknown Columns**: Script rejects data with columns not in the CSV
3. **Missing Columns**: Empty values used for any omitted columns
4. **Special Characters**: Automatically escapes commas, quotes, and newlines
5. **Encoding**: Maintains UTF-8 encoding throughout

## Error Handling

### Unknown Column Error

```
❌ Validation Error: Unknown columns: invalidColumn
```

**Fix**: Check column names with `--show-headers` and ensure exact match (case-sensitive).

### File Not Found

```
❌ Error: CSV file not found: path/to/file.csv
```

**Fix**: Verify the file path is correct relative to project root.

### Invalid Format

```
❌ Validation Error: Invalid format: 'baddata'. Use key=value format
```

**Fix**: Ensure all data arguments use `key=value` format.

## Advanced Usage

### Quiet Mode

Suppress output for scripting:

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  data/file.csv column="value" --quiet
```

### Show Headers Only

Inspect CSV structure without making changes:

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  data/file.csv --show-headers
```

## Examples

See [EXAMPLES.md](EXAMPLES.md) for detailed examples with real JMC Commerce foundation data files.

## Best Practices

1. **Always inspect headers first** using `--show-headers`
2. **Use quotes for values** containing spaces or special characters
3. **Verify the addition** by checking the row count output
4. **Commit changes** to version control after adding foundation data
5. **Test locally** before deploying to other environments

## Script Location

The Python script is located at:
```
.claude/skills/csv-data-manager/scripts/add_csv_row.py
```

No external dependencies required - uses Python standard library only.

## Limitations

- Only supports CSV files (comma-separated)
- Cannot modify existing rows (append only)
- Does not validate business logic (e.g., unique IDs)
- Assumes UTF-8 encoding

