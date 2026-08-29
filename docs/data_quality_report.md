# Data Quality Report

## 1. Audit Overview

| Item | Value |
|---|---|
| Dataset | Brazilian E-Commerce Public Dataset by Olist |
| Audit date | August 29, 2026 |
| Source files | 9 CSV files |
| Source location | Local source folder, excluded from Git |
| Audit method | Python CSV and pandas validation |
| Primary reporting period | January 1, 2017 to August 31, 2018 |

The audit evaluated table grain, key uniqueness, referential integrity, missing values, order lifecycle dates, review duplication, financial reconciliation, and customer identity.

## 2. Source Inventory

| Source table | Rows | Columns | Expected grain |
|---|---:|---:|---|
| Customers | 99,441 | 5 | One row per `customer_id` |
| Geolocation | 1,000,163 | 5 | Multiple coordinates per ZIP prefix |
| Order Items | 112,650 | 7 | One row per order item |
| Payments | 103,886 | 5 | One row per payment record |
| Reviews | 99,224 | 7 | One row per source review record |
| Orders | 99,441 | 8 | One row per order |
| Products | 32,951 | 9 | One row per product |
| Sellers | 3,095 | 4 | One row per seller |
| Category Translation | 71 | 2 | One row per translated category |

## 3. Key Integrity

The following keys contain no missing values or duplicate key combinations:

| Table | Valid key |
|---|---|
| Customers | `customer_id` |
| Orders | `order_id` |
| Order Items | `order_id + order_item_id` |
| Payments | `order_id + payment_sequential` |
| Products | `product_id` |
| Sellers | `seller_id` |
| Category Translation | `product_category_name` |

All tested core foreign-key relationships contain zero orphan records:

- Orders to Customers
- Order Items to Orders
- Order Items to Products
- Order Items to Sellers
- Payments to Orders
- Reviews to Orders

## 4. Customer Identity

The Customers source contains:

- 99,441 `customer_id` records
- 96,096 distinct `customer_unique_id` values
- 3,345 additional order-level customer records beyond the number of unique customers

`customer_id` is an order-scoped identifier and must not be used to count people. Customer metrics use `customer_unique_id`.

### Location stability

| Condition | Customers |
|---|---:|
| Multiple customer records | 2,997 |
| Multiple ZIP prefixes | 250 |
| Multiple cities | 122 |
| Multiple states | 39 |

Customer location is therefore treated as an order-level delivery attribute rather than a permanent customer attribute.

## 5. Geolocation Quality

The geolocation source contains:

- 1,000,163 rows
- 19,015 distinct ZIP prefixes
- 981,148 additional rows beyond one row per ZIP prefix

The raw source cannot be connected directly to facts because it would create a many-to-many relationship and duplicate business values.

Relationship exceptions:

| Relationship | Unmatched rows | Unmatched distinct ZIP prefixes |
|---|---:|---:|
| Customer ZIP to Geolocation ZIP | 278 | 157 |
| Seller ZIP to Geolocation ZIP | 7 | 7 |

Planned treatment:

1. Aggregate geolocation to one row per ZIP prefix.
2. Retain unmatched business records.
3. Leave unavailable coordinates blank.
4. Do not remove orders or sellers because of missing geographic coordinates.

## 6. Review Quality

The Reviews source does not have a reliable unique business key.

| Test | Result |
|---|---:|
| Source review rows | 99,224 |
| Distinct reviewed orders | 98,673 |
| Orders without reviews | 768 |
| Orders with multiple review rows | 547 |
| Orders with conflicting review scores | 202 |
| Repeated `review_id` values | 789 |
| Repeated review IDs linked to multiple orders | 789 |
| Exact duplicate rows beyond first occurrence | 0 |

All 789 repeated review IDs contain identical score, comment, and timestamp payloads across their associated orders.

### Review-resolution sensitivity

| Method | Average review score |
|---|---:|
| Raw review rows | 4.086421 |
| First review per order | 4.087217 |
| Latest review per order | 4.086386 |
| Average within order, then overall | 4.086793 |

Only 201 reviewed orders, or 0.2037%, have different first and latest scores.

### Planned treatment

The analytical review grain will be one row per `order_id`.

When multiple reviews exist, select the latest record using:

1. `review_answer_timestamp`
2. `review_creation_date`
3. `review_id` as a deterministic tie-breaker

Missing review scores remain blank and are not replaced with zero.

## 7. Order Lifecycle Quality

### Order-status distribution

| Order status | Orders | Percentage |
|---|---:|---:|
| Delivered | 96,478 | 97.0203% |
| Shipped | 1,107 | 1.1132% |
| Canceled | 625 | 0.6285% |
| Unavailable | 609 | 0.6124% |
| Invoiced | 314 | 0.3158% |
| Processing | 301 | 0.3027% |
| Created | 5 | 0.0050% |
| Approved | 2 | 0.0020% |

### Missing order dates

| Field | Missing rows |
|---|---:|
| `order_approved_at` | 160 |
| `order_delivered_carrier_date` | 1,783 |
| `order_delivered_customer_date` | 2,965 |
| `order_purchase_timestamp` | 0 |
| `order_estimated_delivery_date` | 0 |

Most missing lifecycle dates are consistent with orders that were canceled, unavailable, processing, invoiced, or not yet delivered.

Eight delivered orders are missing `order_delivered_customer_date` and are excluded from delivery-time and late-delivery calculations.

### Date-sequence anomalies

| Test | Eligible orders | Violations |
|---|---:|---:|
| Approval before purchase | 99,281 | 0 |
| Carrier handoff before approval | 97,644 | 1,359 |
| Customer delivery before carrier handoff | 96,475 | 23 |
| Estimated delivery before purchase | 99,441 | 0 |

Because of these anomalies, approval-to-carrier time is not used as a primary KPI. Carrier-to-customer duration excludes records with invalid timestamp sequences.

The primary delivery-duration calculation uses purchase timestamp to customer delivery timestamp.

## 8. Child-Record Coverage

### Orders without order items

775 orders do not have order-item records:

| Status | Orders |
|---|---:|
| Unavailable | 603 |
| Canceled | 164 |
| Created | 5 |
| Invoiced | 2 |
| Shipped | 1 |

These orders remain available for order-status analysis but do not contribute Merchandise GMV.

### Orders without payments

One order in the full source does not have a payment record. No delivered order within the primary reporting period is missing a payment.

### Orders without reviews

768 orders do not have reviews, including 646 delivered orders. Missing reviews remain blank.

## 9. Product Quality

### Missing product values

| Field group | Missing rows |
|---|---:|
| Category, name length, description length, photo quantity | 610 |
| Weight, length, height, width | 2 |

Thirteen products across two named categories do not have an English category translation.

Planned treatment:

- Missing category values are assigned `Unknown`.
- Named untranslated categories retain a documented fallback label.
- Products are not removed because of missing attributes.
- Missing physical attributes remain blank.
- Product weight equal to zero is treated as unreliable for weight-based analysis.

## 10. Numeric-Value Quality

### Order Items

| Field | Minimum | Maximum | Zero values | Negative values |
|---|---:|---:|---:|---:|
| `price` | 0.85 | 6,735.00 | 0 | 0 |
| `freight_value` | 0.00 | 409.68 | 383 | 0 |

Zero freight values are retained as potentially valid free-shipping transactions.

### Payments

| Field | Minimum | Maximum | Zero values | Negative values |
|---|---:|---:|---:|---:|
| `payment_installments` | 0 | 24 | 2 | 0 |
| `payment_value` | 0.00 | 13,664.08 | 9 | 0 |

Additional payment-quality findings:

- Three zero-value payments use `not_defined` as payment type.
- These three records belong to canceled orders.
- Two positive credit-card payments have zero installments.
- Zero-value voucher records do not affect total payment value.

Invalid installment values are not automatically changed to one.

## 11. Reporting-Period Selection

The source purchase-date range is:

- Minimum: September 4, 2016
- Maximum: October 17, 2018

The following periods are incomplete:

- September–December 2016
- September–October 2018

The primary reporting period is therefore:

> January 1, 2017 to August 31, 2018

Incomplete periods are retained in the source layer but excluded from primary business reporting.

## 12. Financial Reconciliation

For delivered orders in the primary reporting period:

| Metric | Validated baseline |
|---|---:|
| Delivered Orders | 96,211 |
| Item Rows | 109,880 |
| Merchandise GMV | R$13,181,027.13 |
| Freight Value | R$2,192,092.88 |
| Merchandise plus Freight | R$15,373,120.01 |
| Total Paid | R$15,375,875.44 |
| Merchandise AOV | R$137.00 |

Financial reconciliation results:

| Test | Result |
|---|---:|
| Comparable delivered orders | 96,211 |
| Orders with difference greater than R$0.01 | 370 |
| Mismatch rate | 0.3846% |
| Aggregate payment difference | R$2,755.43 |
| Total absolute order-level difference | R$3,026.19 |
| Median order-level difference | R$0.00 |
| Maximum positive difference | R$182.81 |
| Minimum difference | -R$21.80 |

The dataset does not contain enough information to explain or allocate every difference.

Planned treatment:

- Merchandise GMV remains based on item price.
- Freight remains a separate metric.
- Total Paid remains based on payment records.
- Differences are retained without artificial correction.
- Payment data is never flattened directly onto order-item rows.

## 13. Customer Purchase Baseline

For delivered orders in the primary reporting period:

| Metric | Validated baseline |
|---|---:|
| Distinct Customers | 93,104 |
| New Customer Orders | 93,094 |
| Returning Customer Orders | 3,117 |
| Returning Order Rate | 3.2398% |
| Customers with at least one returning order | 2,798 |

Customer order number is calculated over the full observed delivered-order history before applying the reporting-period filter.

“New” means the first delivered order observed in the dataset. Customer purchases before the source history began are unknown.

## 14. Data-Quality Assessment

| Area | Assessment | Required action |
|---|---|---|
| Core keys | Good | Preserve validated keys |
| Referential integrity | Good | No orphan remediation required |
| Order-item values | Good | Apply correct numeric types |
| Payment reconciliation | Good with minor differences | Keep financial metrics separate |
| Reviews | Requires transformation | Select latest review per order |
| Geolocation | Requires aggregation | Reduce to one row per ZIP prefix |
| Customer identity | Requires semantic correction | Use `customer_unique_id` |
| Customer location | Slowly changing | Attach geography at order grain |
| Product categories | Minor missing mappings | Assign documented fallback values |
| Order dates | Status-dependent missing values | Exclude ineligible records by metric |
| Reporting period | Incomplete source edges | Restrict primary reporting period |

## 15. Quality-Control Principles

The project will follow these principles:

1. Do not delete a business record only because a related optional attribute is missing.
2. Do not replace missing review scores or dates with zero.
3. Do not force payment totals to equal item value plus freight.
4. Do not use `customer_id` to count unique customers.
5. Do not connect raw geolocation records directly to fact tables.
6. Do not flatten multiple fact grains into one duplicated table.
7. Document every exclusion, fallback mapping, and KPI population.
8. Reconcile final Power BI measures against the validated baselines in this report.