# Foundation Data Schema Map

Complete relationship diagram and field specifications for JMC Commerce foundation data tables.

## Table of Contents

- [Product & Item Schema](#product--item-schema)
- [Customer Schema](#customer-schema)
- [Order & Transaction Schema](#order--transaction-schema)
- [Tax Schema](#tax-schema)
- [Promotion Schema](#promotion-schema)
- [User & Device Schema](#user--device-schema)

---

## Product & Item Schema

### Relationship Diagram

```
ITM_PRODUCT (Parent)
    └── ITM_ITEM (Child)
        ├── ITM_SELLING_PRICE (Child)
        ├── ITM_SELLING_RULE (Child)
        ├── ITM_ITEM_IMAGE (Child)
        ├── ITM_ITEM_ID (Child - Alternate IDs)
        ├── ITM_ASSIGNED_ITEM (Child)
        ├── ITM_ITEM_GROUP_MEMBER (Child)
        └── ITM_RELATED_ITEM (Child)

ITM_PRODUCT also has:
    ├── ITM_PRODUCT_OPTION (Child)
    ├── ITM_PRODUCT_COPY_SECTION (Child)
    └── ITM_INQ_ATTRIBUTE_PRODUCT_VAL (Child)
```

### ITM_PRODUCT

**File:** `post_01_itm-product.csv`

**Purpose:** Master product catalog (style/model level)

**Fields:**
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| PRODUCT_ID | String(PK) | Yes | Unique product identifier | `"432685"`, `"0000-0001-01"` |
| DESCRIPTION | String | Yes | Product name/description | `"W- WHISKEY GLASSES 3PACK"` |
| PRODUCT_COPY_ID | String | No | Copy/content reference | Same as PRODUCT_ID |
| CLASSIFIER_CLASS | String | No | Product classification | `""` |
| CLASSIFIER_STYLE | String | No | Style classification | `""` |
| CLASSIFIER_BRAND | String | No | Brand name | `""` |
| CLASSIFIER_DEPARTMENT | String | No | Department code | `""` |
| CREATE_TIME | Timestamp | Yes | Creation timestamp | `2024-02-20 15:19:06.260` |
| CREATE_BY | String | Yes | Creator | `system` |
| LAST_UPDATE_TIME | Timestamp | Yes | Last update timestamp | `2024-02-20 15:19:06.260` |
| LAST_UPDATE_BY | String | Yes | Last updater | `system` |

**Dependencies:** None (root table)

---

### ITM_ITEM

**File:** `post_01_itm-item.csv`

**Purpose:** Sellable SKU/variant level (color, size, configuration)

**Fields:**
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| ITEM_ID | String(PK) | Yes | Unique item/SKU identifier | `"1210000251"`, `"517212AGX0"` |
| ITEM_NAME | String | No | Short item name | `"BAUER 20V Brushless..."` |
| DESCRIPTION | String | Yes | Item description | Full description |
| LONG_DESCRIPTION | String | No | Extended description | Detailed description |
| TAX_GROUP_ID | String(FK) | Yes | Tax category | `"111"`, `"145"`, `"155"` |
| TAX_EXEMPT_CODE | String | No | Tax exemption code | `"0"` |
| TYPE_CODE | String | Yes | Item type | `"STOCK"`, `"WARRANTY"`, `"SERVICE"` |
| TARE_WEIGHT | Decimal | No | Container weight | `""` |
| FAMILY_CODE | String | No | Product family | `""` |
| EXPIRATION_DATE | Date | No | Expiration date | `""` |
| PRODUCT_ID | String(FK) | Yes | Parent product | References ITM_PRODUCT |
| ITEM_COPY_ID | String | No | Copy reference | `""` |
| CLASSIFIER_COLOR | String | No | Color classification | `""` |
| CREATE_TIME | Timestamp | Yes | Creation timestamp | `2024-02-20 15:19:05.701` |
| CREATE_BY | String | Yes | Creator | `system` |
| LAST_UPDATE_TIME | Timestamp | Yes | Last update timestamp | `2024-02-20 15:19:05.701` |
| LAST_UPDATE_BY | String | Yes | Last updater | `system` |

**Dependencies:**
- **PRODUCT_ID** → ITM_PRODUCT.PRODUCT_ID (REQUIRED)
- **TAX_GROUP_ID** → TAX_GROUP.TAX_GROUP_ID (REQUIRED)

**Validation:**
- PRODUCT_ID must exist in ITM_PRODUCT before creating item
- TAX_GROUP_ID must exist in TAX_GROUP (common values: 111, 145, 155)
- TYPE_CODE must be valid enum: STOCK, WARRANTY, SERVICE

---

### ITM_SELLING_PRICE

**File:** `post_01_itm-selling-price.csv`

**Purpose:** Price rules for items (can be tag-based for different locations)

**Fields:**
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| SELLING_PRICE_ID | String(PK) | Yes | Unique price rule ID | `"1210000251"` |
| EFFECTIVE_START_TIME | Timestamp | Yes | When price becomes active | `2000-01-01 00:00:00.000` |
| ITEM_ID | String(FK) | Yes | Item being priced | References ITM_ITEM |
| PRODUCT_ID | String(FK) | Yes | Product being priced | References ITM_PRODUCT |
| PRICE_TYPE | String | Yes | Price type code | `"P"` (regular price) |
| LIST_PRICE | Decimal | No | MSRP/list price | `0.000` |
| PRICE | Decimal | Yes | Actual selling price | `159.99`, `11.950` |
| QUANTITY | Decimal | Yes | Price quantity | `1.000` |
| COST | Decimal | No | Cost basis | `""` |
| EFFECTIVE_END_TIME | Timestamp | No | When price expires | `""` |
| TAG_APP_ID | String | No | Application tag filter | `"*"` (all) |
| TAG_BUSINESS_UNIT_ID | String | No | Store tag filter | `"*"` (all) |
| TAG_BRAND | String | No | Brand tag filter | `"*"` (all) |
| TAG_DEVICE_ID | String | No | Device tag filter | `"*"` (all) |
| TAG_COUNTRY | String | No | Country tag filter | `"*"` or `"CA"` |
| TAG_STATE | String | No | State tag filter | `"*"` or `"AB"` |
| TAG_STORE_TYPE | String | No | Store type tag filter | `"*"` (all) |
| TAG_DEVICE_TYPE | String | No | Device type tag filter | `"*"` (all) |
| CREATE_TIME | Timestamp | Yes | Creation timestamp | `2024-02-20 15:19:06.486` |
| CREATE_BY | String | Yes | Creator | `system` |
| LAST_UPDATE_TIME | Timestamp | Yes | Last update timestamp | `2024-02-20 15:19:06.486` |
| LAST_UPDATE_BY | String | Yes | Last updater | `system` |

**Dependencies:**
- **ITEM_ID** → ITM_ITEM.ITEM_ID (REQUIRED)
- **PRODUCT_ID** → ITM_PRODUCT.PRODUCT_ID (REQUIRED)

**Validation:**
- Both ITEM_ID and PRODUCT_ID must exist
- ITEM_ID must belong to PRODUCT_ID (check ITM_ITEM.PRODUCT_ID)
- PRICE must be positive decimal
- Tags use `"*"` for "match all"

---

## Customer Schema

### Relationship Diagram

```
CUST_CUSTOMER (Parent)
    ├── CUST_EMAIL (Child)
    ├── CUST_PHONE (Child)
    ├── CUST_ADDRESS (Child)
    ├── CUST_LOYALTY_ACCOUNT (Child)
    ├── CUST_PRIVATE_LABEL_ACCOUNT (Child)
    ├── CUST_ACCOUNT_LINK (Child)
    └── CUST_CONTACT_PREFERENCES (Child)
```

### CUST_CUSTOMER

**File:** `post_01_cust-customer.csv`

**Purpose:** Customer master records

**Fields:**
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| CUSTOMER_ID | String(PK) | Yes | Unique customer ID | `"1052430130500000"` (16 digits) |
| FIRST_NAME | String | Yes | First name | `"Alec"` |
| LAST_NAME | String | Yes | Last name | `"Tricity"` |
| STATUS_CODE | String | No | Account status | `""` |
| LOYALTY_NUMBER | String | No | Loyalty account number | `"5000000"` |
| LOYALTY_POINTS | Decimal | No | Point balance | `"3.000"` |
| BIRTHDAY | Timestamp | No | Full birthdate | `1972-04-01 00:00:00.000` |
| BIRTH_MONTH | String | No | Birth month | `"04"` |
| BIRTH_DAY_OF_MONTH | String | No | Birth day | `"01"` |
| GENDER | String | No | Gender | `"MALE"`, `"FEMALE"`, `"UNSPECIFIED"` |
| MEMBER_TIER | String | No | Loyalty tier | `""`, `"Gold"`, `"Silver"` |
| ORGANIZATION | String | No | Organization flag | `"0"` (individual) |
| ORGANIZATION_NAME | String | No | Org name if applicable | `""` |
| OTHER_IDENTIFICATION | String | No | Alt ID | `""` |
| PARENT_CUSTOMER_ID | String(FK) | No | Parent customer (households) | `""` |
| OPT_INTO_MARKETING_FLAG | Boolean | No | Marketing opt-in | `""`, `"1"` |
| ADDITIONAL_INFO_JSON | JSON | No | Extended attributes | `""` |

**Dependencies:** None (can reference self for PARENT_CUSTOMER_ID)

**Validation:**
- CUSTOMER_ID should be unique 16-digit number
- GENDER must be: MALE, FEMALE, UNSPECIFIED
- If PARENT_CUSTOMER_ID used, must reference existing CUSTOMER_ID

---

### CUST_EMAIL

**File:** `post_01_cust-email.csv`

**Purpose:** Customer email addresses

**Dependencies:**
- **CUSTOMER_ID** → CUST_CUSTOMER.CUSTOMER_ID (REQUIRED)

---

### CUST_ADDRESS

**File:** `post_01_cust-address.csv`

**Purpose:** Customer addresses (shipping, billing)

**Dependencies:**
- **CUSTOMER_ID** → CUST_CUSTOMER.CUSTOMER_ID (REQUIRED)

---

### CUST_LOYALTY_ACCOUNT

**File:** `post_01_cust-loyalty-account.csv`

**Purpose:** Loyalty program memberships

**Dependencies:**
- **CUSTOMER_ID** → CUST_CUSTOMER.CUSTOMER_ID (REQUIRED)

---

## Order & Transaction Schema

### Relationship Diagram

```
CUST_CUSTOMER
    └── SLS_ORDER (Child)
        ├── SLS_ORDER_LINE_ITEM (Child)
        │   ├── → ITM_ITEM (FK)
        │   └── → ITM_PRODUCT (FK)
        └── SLS_ORDER_NOTE (Child)
```

### SLS_ORDER

**File:** `post_01_sls-order.csv`

**Purpose:** Orders/transactions (BOPIS, ship-to-home, in-store)

**Key Fields:**
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| ORDER_ID | String(PK) | Yes | Unique order ID | `"8765309"` |
| BUSINESS_DATE | String | No | Business date | `"20230831"` (YYYYMMDD) |
| BUSINESS_UNIT_ID | String | No | Store ID | `""` |
| DEVICE_ID | String | No | Register/device ID | `""` |
| CUSTOMER_ID | String(FK) | Yes | Customer placing order | References CUST_CUSTOMER |
| SELLING_CHANNEL_CODE | String | Yes | Sales channel | `"STORE"`, `"ONLINE"` |
| LOYALTY_CARD_NUMBER | String | No | Loyalty number used | `"5000000"` |
| ISO_CURRENCY_CODE | String | Yes | Currency | `"USD"` |
| LINE_ITEM_COUNT | Integer | Yes | Number of line items | `"2"` |
| ITEM_COUNT | Integer | No | Total item quantity | `""` |
| ORDER_CUSTOMER_FIRST_NAME | String | Yes | Customer first name | `"Alec"` |
| ORDER_CUSTOMER_LAST_NAME | String | Yes | Customer last name | `"Tricity"` |
| ORDER_CUSTOMER_EMAIL | String | Yes | Customer email | `"atricity@gmail.com"` |
| ORDER_CUSTOMER_PHONE_NUMBER | String | No | Customer phone | `"6146881597"` |
| TOTAL | Decimal | Yes | Order total | `"86.500"` |
| SUBTOTAL | Decimal | Yes | Subtotal before tax | `"86.000"` |
| TAX_TOTAL | Decimal | Yes | Total tax | `"6.500"` |
| DISCOUNT_TOTAL | Decimal | Yes | Total discounts | `"0.000"` |
| ORDER_TYPE_CODE | String | Yes | Order type | `"BOPIS"`, `"SHIP_TO_HOME"` |
| ORDER_DUE_DATE | String | No | Expected fulfillment | `"05/01/2024"` |
| AMOUNT_DUE | Decimal | Yes | Balance due | `"0.000"` |
| PAYMENT_STATUS_CODE | String | Yes | Payment status | `"PAY_AT_PICKUP"`, `"PAID"` |
| FULFILLING_BUSINESS_UNIT_ID | String | No | Fulfillment store | `"05243"` |

**Dependencies:**
- **CUSTOMER_ID** → CUST_CUSTOMER.CUSTOMER_ID (REQUIRED)

**Validation:**
- CUSTOMER_ID must exist before creating order
- TOTAL should equal SUBTOTAL + TAX_TOTAL - DISCOUNT_TOTAL
- LINE_ITEM_COUNT should match actual line item rows

---

### SLS_ORDER_LINE_ITEM

**File:** `post_01_sls-order-line-item.csv`

**Purpose:** Individual items within an order

**Key Fields:**
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| ORDER_ID | String(FK) | Yes | Parent order | References SLS_ORDER |
| LINE_SEQUENCE_NUMBER | Integer(PK) | Yes | Line number | `"1"`, `"2"` |
| ITEM_ID | String(FK) | Yes | Item being sold | References ITM_ITEM |
| PRODUCT_ID | String(FK) | Yes | Product being sold | References ITM_PRODUCT |
| ITEM_DESCRIPTION | String | Yes | Item name | `"Women's Heritage Fleece..."` |
| ITEM_TYPE | String | Yes | Type | `"STOCK"`, `"SERVICE"` |
| REGULAR_UNIT_PRICE | Decimal | Yes | Regular price | `"59.950"` |
| ACTUAL_UNIT_PRICE | Decimal | Yes | Actual price paid | `"59.950"` |
| QUANTITY | Decimal | Yes | Quantity sold | `"1.000"` |
| EXTENDED_AMOUNT | Decimal | Yes | Line subtotal | `"59.950"` |
| DISCOUNT_AMOUNT | Decimal | Yes | Line discount | `"0.000"` |
| EXTENDED_DISCOUNTED_AMOUNT | Decimal | Yes | After discount | `"59.950"` |
| TAX_AMOUNT | Decimal | Yes | Line tax | `"6.140"` |
| TAX_GROUP_ID | String(FK) | Yes | Tax group | `"145"` |
| ISO_CURRENCY_CODE | String | Yes | Currency | `"USD"` |
| ITEM_RETURNABLE | String | Yes | Can return? | `"0"`, `"1"` |
| ITEM_TAXABLE | String | Yes | Is taxable? | `"0"`, `"1"` |
| ITEM_DISCOUNTABLE | String | Yes | Can discount? | `"0"`, `"1"` |

**Dependencies:**
- **ORDER_ID** → SLS_ORDER.ORDER_ID (REQUIRED)
- **ITEM_ID** → ITM_ITEM.ITEM_ID (REQUIRED)
- **PRODUCT_ID** → ITM_PRODUCT.PRODUCT_ID (REQUIRED)
- **TAX_GROUP_ID** → TAX_GROUP.TAX_GROUP_ID (REQUIRED)

**Validation:**
- Order must exist before adding line items
- Item and Product must exist
- Item must belong to Product (check ITM_ITEM.PRODUCT_ID)
- EXTENDED_AMOUNT should equal REGULAR_UNIT_PRICE × QUANTITY
- Tax group should match item's tax group

---

## Tax Schema

### TAX_GROUP

**File:** `post_01_tax-group.csv`

**Purpose:** Tax categories/groups

**Common Values:**
- `111` - Standard merchandise
- `145` - Clothing/apparel
- `155` - Food/beverage

**Dependencies:** None

---

### TAX_JURISDICTION

**File:** `post_01_tax-jurisdiction.csv`

**Purpose:** Geographic tax regions

**Dependencies:** None

---

## Promotion Schema

### Relationship Diagram

```
PRM_PROMOTION (Parent)
    ├── PRM_QUALIFICATION (Child)
    │   ├── PRM_QUALIFICATION_ATTR (Child)
    │   └── PRM_QUALIFICATION_ITEM (Child)
    │       └── PRM_QUALIFICATION_ITEM_ATTR (Child)
    ├── PRM_REWARD (Child)
    │   ├── PRM_REWARD_ITEM (Child)
    │   ├── PRM_REWARD_CATEGORY (Child)
    │   └── PRM_REWARD_PROMO_CODE (Child)
    └── PRM_ASSIGNED_PROMOTION (Child)
```

### Key Dependencies

- PRM_QUALIFICATION → PRM_PROMOTION
- PRM_REWARD → PRM_PROMOTION
- PRM_REWARD_PROMO_CODE → PRM_REWARD

---

## User & Device Schema

### USR_USER

**File:** `post_01_usr-user.csv` (intellij)

**Purpose:** System users (employees, managers)

**Dependencies:** None

---

### DEV_DEVICE

**File:** `post_01_dev-device.csv` (intellij)

**Purpose:** POS devices, registers, tablets

**Dependencies:**
- Business unit references (if used)

---

## Cross-Reference Summary

### Most Common Dependencies

1. **ITM_ITEM** depends on:
   - ITM_PRODUCT (PRODUCT_ID)
   - TAX_GROUP (TAX_GROUP_ID)

2. **ITM_SELLING_PRICE** depends on:
   - ITM_ITEM (ITEM_ID)
   - ITM_PRODUCT (PRODUCT_ID)

3. **SLS_ORDER** depends on:
   - CUST_CUSTOMER (CUSTOMER_ID)

4. **SLS_ORDER_LINE_ITEM** depends on:
   - SLS_ORDER (ORDER_ID)
   - ITM_ITEM (ITEM_ID)
   - ITM_PRODUCT (PRODUCT_ID)
   - TAX_GROUP (TAX_GROUP_ID)

### Creation Order for Complete Test Scenario

1. **TAX_GROUP** (if needed)
2. **CUST_CUSTOMER**
3. **ITM_PRODUCT**
4. **ITM_ITEM**
5. **ITM_SELLING_PRICE**
6. **SLS_ORDER**
7. **SLS_ORDER_LINE_ITEM**

This order ensures all foreign key dependencies are satisfied.

