# Foundation Data Examples

Complete, realistic examples of generating coherent test data with all dependencies validated.

## Table of Contents

-   [Example 1: Adding a New Product with Complete Data](#example-1-adding-a-new-product-with-complete-data)
-   [Example 2: Creating a Customer Order](#example-2-creating-a-customer-order)
-   [Example 3: Complete Test Scenario](#example-3-complete-test-scenario)
-   [Example 4: Validation Workflow](#example-4-validation-workflow)

---

## Example 1: Adding a New Product with Complete Data

**Goal:** Add a new product "Ultimate Wireless Headphones" with pricing and complete setup

### Step 1: Plan Dependencies

```
Goal: Sellable item with price
Required chain:
├── TAX_GROUP (111 - already exists ✓)
├── ITM_PRODUCT (NEW-PROD-2025-001) - CREATE
├── ITM_ITEM (NEW-ITEM-2025-001) - CREATE
└── ITM_SELLING_PRICE - CREATE
```

### Step 2: Verify Tax Group Exists

```bash
grep "^111," headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_tax-group.csv
```

Expected: Find existing row with TAX_GROUP_ID=111

### Step 3: Create Product Record

**File:** `post_01_itm-product.csv`

```csv
"PRODUCT_ID","DESCRIPTION","PRODUCT_COPY_ID","CREATE_TIME","CREATE_BY","LAST_UPDATE_TIME","LAST_UPDATE_BY","CLASSIFIER_CLASS","CLASSIFIER_STYLE","CLASSIFIER_BRAND","CLASSIFIER_DEPARTMENT"
"NEW-PROD-2025-001","Ultimate Wireless Headphones","NEW-PROD-2025-001",2025-01-15 10:00:00.000,system,2025-01-15 10:00:00.000,system,"Electronics","Premium","AudioTech","Electronics"
```

**Field Breakdown:**

-   `PRODUCT_ID`: `"NEW-PROD-2025-001"` - Unique, memorable for testing
-   `DESCRIPTION`: Full product name
-   `PRODUCT_COPY_ID`: Same as PRODUCT_ID (standard pattern)
-   `CREATE_TIME`/`LAST_UPDATE_TIME`: Current realistic timestamp
-   `CREATE_BY`/`LAST_UPDATE_BY`: `system` (standard for foundation data)
-   Classifier fields: Optional but helpful for categorization

### Step 4: Create Item Record

**File:** `post_01_itm-item.csv`

```csv
ITEM_ID,ITEM_NAME,DESCRIPTION,LONG_DESCRIPTION,TAX_GROUP_ID,TAX_EXEMPT_CODE,TYPE_CODE,TARE_WEIGHT,FAMILY_CODE,EXPIRATION_DATE,PRODUCT_ID,ITEM_COPY_ID,CLASSIFIER_COLOR,CREATE_TIME,CREATE_BY,LAST_UPDATE_TIME,LAST_UPDATE_BY
NEW-ITEM-2025-001,"Ultimate Wireless Headphones","Ultimate Wireless Headphones - Black","Ultimate Wireless Headphones with Active Noise Cancellation - Black",111,0,STOCK,,,,NEW-PROD-2025-001,,,2025-01-15 10:00:00.000,system,2025-01-15 10:00:00.000,system
```

**Field Breakdown:**

-   `ITEM_ID`: `NEW-ITEM-2025-001` - SKU level identifier
-   `DESCRIPTION`: Short description
-   `LONG_DESCRIPTION`: Detailed description with variant (color)
-   `TAX_GROUP_ID`: `111` - References existing tax group ✓
-   `TYPE_CODE`: `STOCK` - Standard sellable item
-   `PRODUCT_ID`: `NEW-PROD-2025-001` - References product created in Step 3 ✓

### Step 5: Create Selling Price

**File:** `post_01_itm-selling-price.csv`

```csv
"SELLING_PRICE_ID","EFFECTIVE_START_TIME","ITEM_ID","PRODUCT_ID","PRICE_TYPE","LIST_PRICE","PRICE","QUANTITY","COST","EFFECTIVE_END_TIME","CREATE_TIME","CREATE_BY","LAST_UPDATE_TIME","LAST_UPDATE_BY","TAG_APP_ID","TAG_BUSINESS_UNIT_ID","TAG_BRAND","TAG_DEVICE_ID","TAG_COUNTRY","TAG_STATE","TAG_STORE_TYPE","TAG_DEVICE_TYPE"
"NEW-ITEM-2025-001",2025-01-15 00:00:00.000,"NEW-ITEM-2025-001","NEW-PROD-2025-001",P,299.990,249.990,1.000,,,2025-01-15 10:00:00.000,system,2025-01-15 10:00:00.000,system,*,*,*,*,*,*,*,*
```

**Field Breakdown:**

-   `SELLING_PRICE_ID`: Typically same as ITEM_ID
-   `EFFECTIVE_START_TIME`: When price becomes active
-   `ITEM_ID`: `NEW-ITEM-2025-001` - References item ✓
-   `PRODUCT_ID`: `NEW-PROD-2025-001` - Must match item's product ✓
-   `LIST_PRICE`: MSRP `299.990`
-   `PRICE`: Actual selling price `249.990`
-   `QUANTITY`: `1.000` - Price per unit
-   Tag fields: All `*` means applies everywhere

### Step 6: Validate Complete Chain

```bash
# Verify product exists
grep "NEW-PROD-2025-001" post_01_itm-product.csv

# Verify item exists and references correct product
grep "NEW-ITEM-2025-001" post_01_itm-item.csv | grep "NEW-PROD-2025-001"

# Verify price exists and references correct item+product
grep "NEW-ITEM-2025-001" post_01_itm-selling-price.csv | grep "NEW-PROD-2025-001"
```

✅ **Result:** Complete, valid product ready for sale

---

## Example 2: Creating a Customer Order

**Goal:** Create a BOPIS order for an existing customer with 2 items

### Step 1: Plan Dependencies

```
Goal: Order with 2 line items
Required chain:
├── CUST_CUSTOMER (verify exists)
├── ITM_ITEM × 2 (verify exist)
├── ITM_PRODUCT × 2 (verify exist)
├── SLS_ORDER (CREATE)
└── SLS_ORDER_LINE_ITEM × 2 (CREATE)
```

### Step 2: Verify Customer Exists

```bash
grep "1052430130500000" headless/point-of-sale/base/src/main/resources/data/foundation/integration/post_01_cust-customer.csv
```

Expected: Customer "Alec Tricity" exists ✓

### Step 3: Verify Items Exist

```bash
# Item 1: 517212AGX0
grep "^517212AGX0," post_01_itm-item.csv
# Expected: Women's Heritage Fleece, PRODUCT_ID=526620AG4 ✓

# Item 2: 527126AGX0
grep "^527126AGX0," post_01_itm-item.csv
# Expected: Women's Sweatshirt, PRODUCT_ID=527365AG5 ✓
```

### Step 4: Calculate Order Totals

```
Line 1: $59.95 × 1 = $59.95, Tax: $6.14
Line 2: $31.19 × 1 = $31.19, Tax: $3.20

Subtotal: $91.14
Tax Total: $9.34
Order Total: $100.48
```

### Step 5: Create Order Record

**File:** `post_01_sls-order.csv`

```csv
"ORDER_ID","BUSINESS_DATE","BUSINESS_UNIT_ID","DEVICE_ID","TAX_TOTAL_FOR_DISPLAY","CUSTOMER_ID","SELLING_CHANNEL_CODE","LOYALTY_CARD_NUMBER","TAX_EXEMPT_CUSTOMER_ID","TAX_EXEMPT_CERTIFICATE","TAX_EXEMPT_CODE","EMPLOYEE_ID_FOR_DISCOUNT","ISO_CURRENCY_CODE","LINE_ITEM_COUNT","AGE_RESTRICTED_DATE_OF_BIRTH","ITEM_COUNT","CUSTOMER_NAME","TENDER_TYPE_CODES","VOIDABLE_FLAG","TAX_GEO_CODE_ORIGIN","ORDER_CUSTOMER_FIRST_NAME","ORDER_CUSTOMER_LAST_NAME","ORDER_CUSTOMER_EMAIL","ORDER_CUSTOMER_PHONE_NUMBER","ORDER_CUSTOMER_ALTERNATE_NAME","TOTAL","PRE_TENDER_BALANCE_DUE","SUBTOTAL","TAX_TOTAL","DISCOUNT_TOTAL","ORDER_TYPE_CODE","PARENT_ORDER_ID","ESTIMATED_AVAILABILITY_DATE","ACTUAL_AVAILABILITY_DATE","ORDER_DUE_DATE","AMOUNT_DUE","PAYMENT_STATUS_CODE","FULFILLING_BUSINESS_UNIT_ID","HANDLING_METHOD_TYPE_CODE","HANDLING_COST","HANDLING_DATE","HANDLING_DESCRIPTION","EXPECTED_SHIP_DATE","SURCHARGE","DELIVERY_GROUP"
"ORD-TEST-2025-001","20250115",,,,"1052430130500000","STORE","5000000",,,,,"USD","2",,,,,,,Alec,Tricity,atricity@gmail.com,6146881597,,"100.480",,"91.140","9.340","0.000","BOPIS",,,,01/20/2025,0.000,"PAY_AT_PICKUP","05243",,,,,,,
```

**Key Points:**

-   `ORDER_ID`: `"ORD-TEST-2025-001"` - Unique identifier
-   `BUSINESS_DATE`: `"20250115"` - YYYYMMDD format
-   `CUSTOMER_ID`: `"1052430130500000"` - References existing customer ✓
-   `LOYALTY_CARD_NUMBER`: Customer's loyalty number
-   `LINE_ITEM_COUNT`: `"2"` - Must match actual line items
-   `TOTAL`: `"100.480"` - Matches calculated total ✓
-   `SUBTOTAL`: `"91.140"` - Matches calculated subtotal ✓
-   `TAX_TOTAL`: `"9.340"` - Matches calculated tax ✓
-   `ORDER_TYPE_CODE`: `"BOPIS"` - Buy Online Pickup In Store
-   `ORDER_DUE_DATE`: `01/20/2025` - Pickup date
-   `PAYMENT_STATUS_CODE`: `"PAY_AT_PICKUP"` - Pay when picking up
-   `FULFILLING_BUSINESS_UNIT_ID`: `"05243"` - Store fulfilling order

### Step 6: Create Line Item 1

**File:** `post_01_sls-order-line-item.csv`

```csv
"ORDER_ID","LINE_SEQUENCE_NUMBER","FULFILLING_BUSINESS_UNIT_ID","ASSIGNMENT_STATUS","VOIDED","OVERRIDE_USER_ID","ENTRY_METHOD_CODE","POS_ITEM_ID","ITEM_ID","ITEM_DESCRIPTION","ITEM_TYPE","REGULAR_UNIT_PRICE","ACTUAL_UNIT_PRICE","QUANTITY","EXTENDED_AMOUNT","DISCOUNT_AMOUNT","EXTENDED_DISCOUNTED_AMOUNT","RTN_EXTENDED_DISCOUNTED_AMOUNT","TAX_AMOUNT","REASON_CODE_GROUP_ID","REASON_CODE","DISPOSITION_CODE","GIFT_RECEIPT","ITEM_RETURNABLE","ITEM_TAXABLE","QUANTITY_AVAIL_FOR_RETURN","ITEM_DISCOUNTABLE","EMPLOYEE_DISCOUNT_ALLOWED","ITEM_PRICE_OVERRIDABLE","DISCOUNT_APPLIED","DAMAGE_DISCOUNT_APPLIED","TAX_INCLUDED_IN_PRICE","TAX_GROUP_ID","ORIG_LINE_SEQUENCE_NUMBER","ORIG_SEQUENCE_NUMBER","ORIG_BUSINESS_DATE","ORIG_DEVICE_ID","ORIG_ORDER_ID","ORIG_USERNAME","ORIG_BUSINESS_UNIT_ID","RETURN_POLICY_ID","ITEM_RETURNED","ISO_CURRENCY_CODE","TARE_WEIGHT","ITEM_WEIGHT","ITEM_WEIGHT_PLUS_TARE","WEIGHT_UNIT_OF_MEASURE","WEIGHT_ENTRY_METHOD_CODE","FAMILY_CODE","ITEM_LENGTH","LENGTH_UNIT_OF_MEASURE","QUANTITY_MODIFIABLE","SAVE_VALUE","SAVE_VALUE_TYPE","COUPON_ALLOWED","USERNAME","EXTERNAL_SYSTEM_ID","PRODUCT_ID","ITEM_NAME","ITEM_LONG_DESCRIPTION","ADDITIONAL_CLASSIFIERS","TENDER_GROUP","TENDER_AUTH_METHOD_CODE","ESTIMATED_AVAILABILITY_DATE","ACTUAL_AVAILABILITY_DATE","ORDER_ITEM_STATUS_CODE","PACKAGE_LINE_SEQUENCE_NUMBER","HANDLING_COST"
"ORD-TEST-2025-001","1","05243",,"0",,"INQUIRY","517212AGX0","517212AGX0","Women's Heritage Fleece Snap Neck Pullover Top","STOCK","59.950","59.950","1.000","59.950","0.000","59.950","59.950","6.140",,,,"0","1","1","0.000","1","1","1","0","0","0","145","1","1","20250115",,,,,,"0","USD",,,,,,"301",,,"1",,,"1",,"","526620AG4","Women's Heritage Fleece Snap Neck Pullover Top","Women's Heritage Fleece Snap Neck Pullover Top",,"IN_STORE","PURCHASE_AUTH",,,"CLAIMED",,
```

**Key Points:**

-   `ORDER_ID`: `"ORD-TEST-2025-001"` - References order ✓
-   `LINE_SEQUENCE_NUMBER`: `"1"` - First line item
-   `ITEM_ID`: `"517212AGX0"` - References existing item ✓
-   `PRODUCT_ID`: `"526620AG4"` - Must match item's product ✓
-   `REGULAR_UNIT_PRICE`: `"59.950"` - Price per unit
-   `QUANTITY`: `"1.000"` - Quantity sold
-   `EXTENDED_AMOUNT`: `"59.950"` - Price × Quantity ✓
-   `TAX_AMOUNT`: `"6.140"` - Calculated tax
-   `TAX_GROUP_ID`: `"145"` - Apparel tax group
-   `ITEM_TYPE`: `"STOCK"` - Physical merchandise
-   `ORDER_ITEM_STATUS_CODE`: `"CLAIMED"` - Reserved for customer

### Step 7: Create Line Item 2

```csv
"ORD-TEST-2025-001","2","05243",,"0",,"INQUIRY","527126AGX0","527126AGX0","Women's Serious Sweats Fleece Lined Reversible Sweatshirt Tunic","STOCK","31.190","31.190","1.000","31.190","0.000","31.190","31.190","3.200",,,,"0","1","1","0.000","1","1","1","0","0","0","145","2","1","20250115",,,,,,"0","USD",,,,,,"301",,,"1",,,"1",,"","527365AG5","Women's Serious Sweats Fleece Lined Reversible Sweatshirt Tunic","Women's Serious Sweats Fleece Lined Reversible Sweatshirt Tunic",,"IN_STORE","PURCHASE_AUTH",,,"CLAIMED",,
```

**Key Points:**

-   `LINE_SEQUENCE_NUMBER`: `"2"` - Second line item
-   All other validations same as Line Item 1

### Step 8: Final Validation

```bash
# Verify order exists
grep "ORD-TEST-2025-001" post_01_sls-order.csv

# Verify 2 line items exist
grep "^\"ORD-TEST-2025-001\"" post_01_sls-order-line-item.csv | wc -l
# Expected: 2

# Verify totals match
# Order SUBTOTAL (91.140) = Line 1 (59.950) + Line 2 (31.190) ✓
# Order TAX_TOTAL (9.340) = Line 1 (6.140) + Line 2 (3.200) ✓
# Order TOTAL (100.480) = SUBTOTAL + TAX_TOTAL ✓
```

✅ **Result:** Complete, validated BOPIS order with correct totals

---

## Example 3: Complete Test Scenario

**Goal:** New customer, new product, complete purchase - full end-to-end

### Scenario Requirements

-   New customer "Jane Smith"
-   New product "Premium Coffee Maker"
-   Customer purchases 1 unit
-   In-store transaction with loyalty signup

### Step 1: Create Customer

**File:** `post_01_cust-customer.csv`

```csv
"CUSTOMER_ID","FIRST_NAME","LAST_NAME","STATUS_CODE","LOYALTY_NUMBER","LOYALTY_POINTS","BIRTHDAY","BIRTH_MONTH","BIRTH_DAY_OF_MONTH","GENDER","MEMBER_TIER","ORGANIZATION","ORGANIZATION_NAME","OTHER_IDENTIFICATION","PARENT_CUSTOMER_ID","OPT_INTO_MARKETING_FLAG","ADDITIONAL_INFO_JSON"
"1052430130599999","Jane","Smith",,"5099999","0.000",1988-06-15 00:00:00.000,06,15,FEMALE,,"0",,,,"1",
```

### Step 2: Add Customer Email

**File:** `post_01_cust-email.csv`

```csv
CUSTOMER_ID,EMAIL_ADDRESS,EMAIL_TYPE,IS_PRIMARY
"1052430130599999","jane.smith@example.com","Personal","1"
```

### Step 3: Add Loyalty Account

**File:** `post_01_cust-loyalty-account.csv`

```csv
CUSTOMER_ID,LOYALTY_ACCOUNT_NUMBER,POINTS,TIER,ENROLLMENT_DATE
"1052430130599999","5099999","0","Bronze","2025-01-15"
```

### Step 4: Create Product

**File:** `post_01_itm-product.csv`

```csv
"PRODUCT_ID","DESCRIPTION","PRODUCT_COPY_ID","CREATE_TIME","CREATE_BY","LAST_UPDATE_TIME","LAST_UPDATE_BY","CLASSIFIER_CLASS","CLASSIFIER_STYLE","CLASSIFIER_BRAND","CLASSIFIER_DEPARTMENT"
"COFFEE-MAKER-001","Premium Coffee Maker","COFFEE-MAKER-001",2025-01-15 10:00:00.000,system,2025-01-15 10:00:00.000,system,"Appliance","Kitchen","BrewMaster","HomeGoods"
```

### Step 5: Create Item

**File:** `post_01_itm-item.csv`

```csv
ITEM_ID,ITEM_NAME,DESCRIPTION,LONG_DESCRIPTION,TAX_GROUP_ID,TAX_EXEMPT_CODE,TYPE_CODE,TARE_WEIGHT,FAMILY_CODE,EXPIRATION_DATE,PRODUCT_ID,ITEM_COPY_ID,CLASSIFIER_COLOR,CREATE_TIME,CREATE_BY,LAST_UPDATE_TIME,LAST_UPDATE_BY
COFFEE-ITEM-001,"Premium Coffee Maker","Premium Coffee Maker - Stainless Steel","BrewMaster Premium Coffee Maker with 12-cup capacity - Stainless Steel",111,0,STOCK,,,,COFFEE-MAKER-001,,,2025-01-15 10:00:00.000,system,2025-01-15 10:00:00.000,system
```

### Step 6: Create Price

**File:** `post_01_itm-selling-price.csv`

```csv
"SELLING_PRICE_ID","EFFECTIVE_START_TIME","ITEM_ID","PRODUCT_ID","PRICE_TYPE","LIST_PRICE","PRICE","QUANTITY","COST","EFFECTIVE_END_TIME","CREATE_TIME","CREATE_BY","LAST_UPDATE_TIME","LAST_UPDATE_BY","TAG_APP_ID","TAG_BUSINESS_UNIT_ID","TAG_BRAND","TAG_DEVICE_ID","TAG_COUNTRY","TAG_STATE","TAG_STORE_TYPE","TAG_DEVICE_TYPE"
"COFFEE-ITEM-001",2025-01-15 00:00:00.000,"COFFEE-ITEM-001","COFFEE-MAKER-001",P,149.990,99.990,1.000,,,2025-01-15 10:00:00.000,system,2025-01-15 10:00:00.000,system,*,*,*,*,*,*,*,*
```

### Step 7: Create Order

**Calculations:**

-   Subtotal: $99.99
-   Tax (10.24%): $10.24
-   Total: $110.23

**File:** `post_01_sls-order.csv`

```csv
"ORDER_ID","BUSINESS_DATE","BUSINESS_UNIT_ID","DEVICE_ID","TAX_TOTAL_FOR_DISPLAY","CUSTOMER_ID","SELLING_CHANNEL_CODE","LOYALTY_CARD_NUMBER","TAX_EXEMPT_CUSTOMER_ID","TAX_EXEMPT_CERTIFICATE","TAX_EXEMPT_CODE","EMPLOYEE_ID_FOR_DISCOUNT","ISO_CURRENCY_CODE","LINE_ITEM_COUNT","AGE_RESTRICTED_DATE_OF_BIRTH","ITEM_COUNT","CUSTOMER_NAME","TENDER_TYPE_CODES","VOIDABLE_FLAG","TAX_GEO_CODE_ORIGIN","ORDER_CUSTOMER_FIRST_NAME","ORDER_CUSTOMER_LAST_NAME","ORDER_CUSTOMER_EMAIL","ORDER_CUSTOMER_PHONE_NUMBER","ORDER_CUSTOMER_ALTERNATE_NAME","TOTAL","PRE_TENDER_BALANCE_DUE","SUBTOTAL","TAX_TOTAL","DISCOUNT_TOTAL","ORDER_TYPE_CODE","PARENT_ORDER_ID","ESTIMATED_AVAILABILITY_DATE","ACTUAL_AVAILABILITY_DATE","ORDER_DUE_DATE","AMOUNT_DUE","PAYMENT_STATUS_CODE","FULFILLING_BUSINESS_UNIT_ID","HANDLING_METHOD_TYPE_CODE","HANDLING_COST","HANDLING_DATE","HANDLING_DESCRIPTION","EXPECTED_SHIP_DATE","SURCHARGE","DELIVERY_GROUP"
"ORD-COFFEE-2025-001","20250115","05243","05243-001",,"1052430130599999","STORE","5099999",,,,,"USD","1",,"1.000",,,,,Jane,Smith,jane.smith@example.com,,,"110.230",,"99.990","10.240","0.000","IN_STORE",,,,,0.000,"PAID","05243",,,,,,,
```

### Step 8: Create Line Item

**File:** `post_01_sls-order-line-item.csv`

```csv
"ORDER_ID","LINE_SEQUENCE_NUMBER","FULFILLING_BUSINESS_UNIT_ID","ASSIGNMENT_STATUS","VOIDED","OVERRIDE_USER_ID","ENTRY_METHOD_CODE","POS_ITEM_ID","ITEM_ID","ITEM_DESCRIPTION","ITEM_TYPE","REGULAR_UNIT_PRICE","ACTUAL_UNIT_PRICE","QUANTITY","EXTENDED_AMOUNT","DISCOUNT_AMOUNT","EXTENDED_DISCOUNTED_AMOUNT","RTN_EXTENDED_DISCOUNTED_AMOUNT","TAX_AMOUNT","REASON_CODE_GROUP_ID","REASON_CODE","DISPOSITION_CODE","GIFT_RECEIPT","ITEM_RETURNABLE","ITEM_TAXABLE","QUANTITY_AVAIL_FOR_RETURN","ITEM_DISCOUNTABLE","EMPLOYEE_DISCOUNT_ALLOWED","ITEM_PRICE_OVERRIDABLE","DISCOUNT_APPLIED","DAMAGE_DISCOUNT_APPLIED","TAX_INCLUDED_IN_PRICE","TAX_GROUP_ID","ORIG_LINE_SEQUENCE_NUMBER","ORIG_SEQUENCE_NUMBER","ORIG_BUSINESS_DATE","ORIG_DEVICE_ID","ORIG_ORDER_ID","ORIG_USERNAME","ORIG_BUSINESS_UNIT_ID","RETURN_POLICY_ID","ITEM_RETURNED","ISO_CURRENCY_CODE","TARE_WEIGHT","ITEM_WEIGHT","ITEM_WEIGHT_PLUS_TARE","WEIGHT_UNIT_OF_MEASURE","WEIGHT_ENTRY_METHOD_CODE","FAMILY_CODE","ITEM_LENGTH","LENGTH_UNIT_OF_MEASURE","QUANTITY_MODIFIABLE","SAVE_VALUE","SAVE_VALUE_TYPE","COUPON_ALLOWED","USERNAME","EXTERNAL_SYSTEM_ID","PRODUCT_ID","ITEM_NAME","ITEM_LONG_DESCRIPTION","ADDITIONAL_CLASSIFIERS","TENDER_GROUP","TENDER_AUTH_METHOD_CODE","ESTIMATED_AVAILABILITY_DATE","ACTUAL_AVAILABILITY_DATE","ORDER_ITEM_STATUS_CODE","PACKAGE_LINE_SEQUENCE_NUMBER","HANDLING_COST"
"ORD-COFFEE-2025-001","1","05243",,"0",,"SCANNED","COFFEE-ITEM-001","COFFEE-ITEM-001","Premium Coffee Maker - Stainless Steel","STOCK","99.990","99.990","1.000","99.990","0.000","99.990","99.990","10.240",,,,"0","1","1","0.000","1","1","1","0","0","0","111","1","1","20250115","05243-001",,,,,"0","USD",,,,,,"301",,,"1",,,"1",,"","COFFEE-MAKER-001","Premium Coffee Maker","Premium Coffee Maker - Stainless Steel",,"IN_STORE","CARD_PRESENT",,,"COMPLETE",,
```

### Complete Validation Checklist

-   [✓] Customer exists and has loyalty account
-   [✓] Product exists
-   [✓] Item exists and references product
-   [✓] Price exists for item
-   [✓] Order references valid customer
-   [✓] Order totals are correct
-   [✓] Line item references valid order, item, product
-   [✓] Line item tax group matches item's tax group
-   [✓] All audit fields populated
-   [✓] All timestamps are realistic

✅ **Result:** Complete, production-ready test scenario

---

## Example 4: Validation Workflow

### Before Adding Any Data

```bash
# 1. Read the file to understand structure
head -1 post_01_itm-item.csv

# 2. Check last few rows to see ID patterns
tail -3 post_01_itm-item.csv

# 3. Verify parent records exist
grep "${PRODUCT_ID}" post_01_itm-product.csv
grep "^${TAX_GROUP_ID}," post_01_tax-group.csv
```

### After Adding Data

```bash
# 1. Confirm new record exists
grep "${NEW_ID}" post_01_target-file.csv

# 2. Verify foreign keys are valid
# (check parent tables as shown above)

# 3. Check for duplicates
grep "^${NEW_ID}," post_01_target-file.csv | wc -l
# Expected: 1 (exactly one match)

# 4. Verify CSV format is valid
# Check for unescaped quotes, malformed lines
tail -5 post_01_target-file.csv
```

### Validating Related Records

```bash
# For items, verify complete chain:
ITEM_ID="NEW-ITEM-001"

# 1. Item exists
grep "^${ITEM_ID}," post_01_itm-item.csv

# 2. Get product ID from item
PRODUCT_ID=$(grep "^${ITEM_ID}," post_01_itm-item.csv | cut -d, -f11)

# 3. Verify product exists
grep "^\"${PRODUCT_ID}\"" post_01_itm-product.csv

# 4. Verify price exists for item
grep "^\"${ITEM_ID}\"" post_01_itm-selling-price.csv

# 5. Check price references same product
grep "^\"${ITEM_ID}\"" post_01_itm-selling-price.csv | grep "\"${PRODUCT_ID}\""
```

---

## Key Takeaways

1. **Always validate parent records first** - Foreign keys must reference existing data
2. **Use realistic IDs** - Follow patterns from existing data
3. **Calculate totals accurately** - Order totals must match line item sums
4. **Maintain data coherence** - Related records should tell a consistent story
5. **Use current timestamps** - Don't copy ancient dates from examples
6. **Verify after adding** - Always confirm data was added correctly
7. **Check the full chain** - Validate from top-level parent to deepest child

These examples demonstrate production-ready test data generation with full referential integrity.
