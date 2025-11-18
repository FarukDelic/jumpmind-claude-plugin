# CSV Data Manager Examples

Real-world examples for adding data to JMC Commerce foundation data files.

## Table of Contents

-   [Item Management](#item-management)
-   [Customer Data](#customer-data)
-   [Promotions](#promotions)
-   [Tax Configuration](#tax-configuration)
-   [User Management](#user-management)

---

## Item Management

### Add New Product

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-product.csv \
  productId="PROD-2025-001" \
  description="Premium Widget Pro" \
  category="Electronics" \
  manufacturer="ACME Corp" \
  active="true"
```

### Add Item with Pricing

```bash
# First, add the item
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-item.csv \
  itemId="ITM-12345" \
  productId="PROD-2025-001" \
  sku="WDG-PRO-001" \
  description="Premium Widget Pro - Blue" \
  color="Blue" \
  size="Large"

# Then add the selling price
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-selling-price.csv \
  itemId="ITM-12345" \
  price="199.99" \
  currency="USD" \
  effectiveDate="2025-01-01"
```

### Add Item Image Reference

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-item-image.csv \
  itemId="ITM-12345" \
  imageUrl="content/items/Jumpmind/ITM-12345.jpg" \
  isPrimary="true" \
  sequence="1"
```

---

## Customer Data

### Add New Customer

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_cust-customer.csv \
  customerId="CUST-202501-001" \
  firstName="Sarah" \
  lastName="Johnson" \
  dateOfBirth="1990-05-15" \
  loyaltyTier="Gold" \
  active="true"
```

### Add Customer Email

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_cust-email.csv \
  customerId="CUST-202501-001" \
  emailAddress="sarah.johnson@example.com" \
  emailType="Personal" \
  isPrimary="true" \
  optInMarketing="true"
```

### Add Customer Address

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_cust-address.csv \
  customerId="CUST-202501-001" \
  addressLine1="123 Main Street" \
  addressLine2="Apt 4B" \
  city="Springfield" \
  state="IL" \
  postalCode="62701" \
  country="US" \
  addressType="Shipping"
```

### Add Loyalty Account

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_cust-loyalty-account.csv \
  customerId="CUST-202501-001" \
  loyaltyAccountNumber="LOY-9876543210" \
  points="5000" \
  tier="Gold" \
  enrollmentDate="2025-01-01" \
  expirationDate="2026-12-31"
```

---

## Promotions

### Add Promotion

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_prm-promotion.csv \
  promotionId="PROMO-SPRING25" \
  name="Spring Sale 2025" \
  description="25% off all seasonal items" \
  startDate="2025-03-01" \
  endDate="2025-03-31" \
  discountPercent="25" \
  active="true"
```

### Add Promotion Reward

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_prm-reward.csv \
  rewardId="RWD-SPRING25-001" \
  promotionId="PROMO-SPRING25" \
  rewardType="PercentOff" \
  rewardValue="25.00" \
  maxApplications="1"
```

### Add Promo Code

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_prm-reward-promo-code.csv \
  promoCodeId="PC-SPRING2025" \
  rewardId="RWD-SPRING25-001" \
  code="SPRING2025" \
  usageLimit="1000" \
  currentUsage="0"
```

---

## Tax Configuration

### Add Tax Jurisdiction

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_tax-jurisdiction.csv \
  jurisdictionId="TAX-IL-SPRINGFIELD" \
  name="Springfield, IL" \
  state="IL" \
  city="Springfield" \
  postalCode="62701" \
  taxRate="8.25"
```

### Add Tax Group

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_tax-group.csv \
  taxGroupId="TG-GENERAL" \
  description="General Merchandise Tax Group" \
  taxable="true" \
  taxJurisdictionId="TAX-IL-SPRINGFIELD"
```

---

## User Management

### Add User (IntelliJ/Dev Environment)

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/intellij/post_01_usr-user.csv \
  userId="dev-user-003" \
  username="developer3" \
  password="password123" \
  firstName="Alex" \
  lastName="Developer" \
  email="alex.dev@jumpmind.com" \
  active="true"
```

### Add User Job Code

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/intellij/post_01_usr-user-job-code.csv \
  userId="dev-user-003" \
  jobCode="Developer" \
  isPrimary="true"
```

---

## Business Unit Configuration

### Add Business Unit

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_ctx-business-unit.csv \
  businessUnitId="STORE-NY-001" \
  name="New York Store 001" \
  city="New York" \
  state="NY" \
  postalCode="10001" \
  phone="212-555-0100" \
  timezone="America/New_York"
```

### Add Device

```bash
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/intellij/post_01_dev-device.csv \
  deviceId="POS-NY001-REG01" \
  businessUnitId="STORE-NY-001" \
  deviceType="Register" \
  description="Register 01" \
  ipAddress="192.168.1.101" \
  active="true"
```

---

## Workflow Example: Adding Complete Product

This example shows adding a complete product with all related data:

```bash
# Step 1: Add product
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-product.csv \
  productId="PROD-WIDGET-001" \
  description="Super Widget Deluxe" \
  category="Widgets" \
  active="true"

# Step 2: Add item variant
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-item.csv \
  itemId="ITM-WIDGET-001-BLU" \
  productId="PROD-WIDGET-001" \
  sku="WDG-DLX-BLU-L" \
  description="Super Widget Deluxe - Blue, Large" \
  color="Blue" \
  size="Large"

# Step 3: Add selling price
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-selling-price.csv \
  itemId="ITM-WIDGET-001-BLU" \
  price="299.99" \
  currency="USD" \
  effectiveDate="2025-01-01"

# Step 4: Add selling rule
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-selling-rule.csv \
  itemId="ITM-WIDGET-001-BLU" \
  ruleType="Standard" \
  active="true"

# Step 5: Add image
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-item-image.csv \
  itemId="ITM-WIDGET-001-BLU" \
  imageUrl="content/items/Jumpmind/WIDGET-001-BLU.jpg" \
  isPrimary="true" \
  sequence="1"
```

---

## Inspecting Before Adding

Always inspect the CSV structure before adding data:

```bash
# Show all available columns
python .claude/skills/csv-data-manager/scripts/add_csv_row.py \
  headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_itm-item.csv \
  --show-headers
```

Example output:

```
Headers for post_01_itm-item.csv:
  1. itemId
  2. productId
  3. sku
  4. description
  5. color
  6. size
  7. active

Total columns: 7
```

This helps you understand exactly what fields are available and required.
