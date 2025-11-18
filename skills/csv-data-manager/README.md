# CSV Data Manager Skill

A Claude Code Agent Skill for safely adding new rows to CSV files with automatic validation and column mapping.

## Quick Start

### Installation

The skill is already installed in this project at:
```
.claude/skills/csv-data-manager/
```

### Usage

Ask Claude to add data to CSV files naturally:

```
Can you add a new item to the integration data with ID "ITM-NEW-001" and description "Test Item"?
```

or

```
I need to add a customer to post_01_cust-customer.csv with firstName="John", lastName="Doe", email="john@example.com"
```

Claude will automatically:
1. Locate the appropriate CSV file
2. Inspect the headers
3. Validate your data against the columns
4. Add the new row
5. Confirm the addition

## Direct Script Usage

You can also use the script directly:

### Show CSV Headers
```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  path/to/file.csv --show-headers
```

### Add New Row
```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  path/to/file.csv \
  column1="value1" \
  column2="value2"
```

## Features

- ✅ **Automatic Header Validation** - Ensures column names match exactly
- ✅ **Data Type Safety** - Validates data format before writing
- ✅ **CSV Format Preservation** - Maintains proper escaping and encoding
- ✅ **Error Prevention** - Rejects invalid columns or malformed data
- ✅ **Verbose Output** - Shows before/after row counts and added data
- ✅ **No Dependencies** - Uses Python standard library only

## Common Use Cases

### Foundation Data (Integration)
Add test/integration data for development:
```
headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_*.csv
```

### Foundation Data (IntelliJ)
Add local development data:
```
headless/point-of-sale/base/src/main/resources/data/foundation/intellij/post_01_*.csv
```

### Test Data
Add test fixtures for automated testing

### Configuration Data
Maintain CSV-based configuration files

## Examples

See [EXAMPLES.md](EXAMPLES.md) for detailed examples including:
- Adding items and products
- Managing customer data
- Creating promotions
- Configuring tax rules
- User management
- Complete workflows

## Validation Rules

The script enforces:
1. **Exact Column Name Matching** (case-sensitive)
2. **No Unknown Columns** (rejects extra fields)
3. **Proper CSV Escaping** (handles commas, quotes, newlines)
4. **UTF-8 Encoding** (consistent character encoding)
5. **Row Integrity** (validates complete row structure)

## Error Messages

### Unknown Column
```
❌ Validation Error: Unknown columns: invalidColumn
```
**Solution**: Check headers with `--show-headers`, fix column name spelling/case

### File Not Found
```
❌ Error: CSV file not found: path/to/file.csv
```
**Solution**: Verify file path is correct and relative to project root

### Invalid Format
```
❌ Validation Error: Invalid format: 'data'. Use key=value format
```
**Solution**: Use `column="value"` format for all data arguments

## Testing the Skill

After installation, test with Claude:

```
Show me the headers for post_01_itm-item.csv in the integration folder
```

Then:

```
Add a test item with ITEM_ID="TEST-001" and DESCRIPTION="Test Item"
```

Claude should automatically use this skill to complete the task.

## Files

```
.claude/skills/csv-data-manager/
├── SKILL.md           # Skill definition and instructions
├── README.md          # This file
├── EXAMPLES.md        # Real-world examples
└── scripts/
    └── add_csv_row.py # Python script for CSV operations
```

## Limitations

- **Append Only** - Cannot modify or delete existing rows
- **CSV Only** - Does not support TSV, Excel, or other formats
- **No Business Logic** - Does not validate unique constraints or relationships
- **UTF-8 Encoding** - Assumes all files use UTF-8

## Contributing

To improve this skill:
1. Edit the relevant files in `.claude/skills/csv-data-manager/`
2. Test changes thoroughly
3. Update documentation
4. Commit to git for team sharing

## License

Part of the JMC Commerce project.

