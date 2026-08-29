# E-commerce Performance Dashboard

A Power BI portfolio project analyzing marketplace performance, customer behavior, product contribution, delivery operations, and customer experience using the Brazilian E-Commerce Public Dataset by Olist.

## Project Status

> **In development**

Completed:

- Dataset selection and source verification
- Business-requirement definition
- Source-data profiling
- Grain and relationship validation
- Data-quality documentation
- Financial and customer baseline reconciliation
- Reusable source-validation script

In progress:

- Power Query transformations
- Dimensional data model
- DAX measure layer
- Dashboard design and business storytelling

## Project Objective

This project demonstrates how multi-table e-commerce data can be transformed into a reliable and decision-oriented Power BI solution.

The dashboard is designed for a **Marketplace Performance Manager** who needs to:

- Monitor commercial performance over time.
- Identify product-category growth drivers.
- Understand new and returning customer behavior.
- Evaluate delivery performance by region and seller.
- Measure the relationship between delivery delays and customer reviews.
- Identify areas requiring management attention.

## Dashboard Scope

The planned report contains approximately three pages:

1. **Executive Overview**
2. **Product and Customer Analysis**
3. **Delivery and Customer Experience**

The primary reporting period is **January 1, 2017 to August 31, 2018**. Incomplete source periods are excluded from primary time comparisons.

## Validated Commercial Baseline

The following results were independently validated before building the Power BI model:

| Metric | Validated value |
|---|---:|
| Delivered Orders | 96,211 |
| Distinct Customers | 93,104 |
| Item Rows | 109,880 |
| Merchandise GMV | R$13,181,027.13 |
| Freight Value | R$2,192,092.88 |
| Merchandise AOV | R$137.00 |
| New Customer Orders | 93,094 |
| Returning Customer Orders | 3,117 |
| Returning Order Rate | 3.2398% |

Merchandise GMV is based on order-item price and excludes freight. It should not be interpreted as Olist's accounting revenue or commission income.

## Business Questions

### Executive Performance

- How do Merchandise GMV, delivered orders, customers, and AOV change over time?
- How does current performance compare with the previous month or year?
- Is growth driven by customer volume, order volume, or order value?
- Which states contribute the most marketplace value?

### Product and Customer Performance

- Which product categories contribute the most GMV and orders?
- Which categories are growing or declining?
- Is marketplace performance concentrated in a small number of categories?
- How do new and returning customer orders differ?
- What is the observed repeat-purchase rate?

### Delivery and Customer Experience

- How do delivery time and on-time delivery rate change over time?
- Which regions, sellers, or categories experience the most delays?
- Is late delivery associated with lower review scores?
- Which high-value sellers have poor delivery or review performance?

## Dataset

This project uses the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

- Publisher: Olist
- License: CC BY-NC-SA 4.0
- Source files: 9 CSV files
- Order purchase coverage: September 2016 to October 2018
- Primary dashboard period: January 2017 to August 2018

The complete source dataset is not stored in this repository. See [`data/README.md`](data/README.md) for download, setup, attribution, and validation instructions.

## Data-Quality Approach

The source audit checks:

- Expected files and row counts
- Primary and composite-key uniqueness
- Referential integrity
- Missing values
- Order lifecycle and timestamp sequences
- Review duplication and review-selection logic
- Payment and order-item reconciliation
- Customer identity and repeat-purchase logic
- Reporting-period completeness

Important modeling decisions include:

- Use `customer_unique_id` to count customers.
- Keep customer geography at the order grain.
- Aggregate geolocation to one row per ZIP prefix.
- Select the latest review for each order.
- Keep Merchandise GMV, Freight Value, and Total Paid as separate metrics.
- Prevent many-to-many joins between items, payments, and reviews.
- Keep incomplete source periods outside primary reporting.

See [`docs/data_quality_report.md`](docs/data_quality_report.md) for measured results and treatment decisions.

## Technology

- Power BI Desktop
- Power Query
- DAX
- Python 3.11
- pandas
- Git and GitHub

Python is used only for reproducible validation and reconciliation. The analytical transformation and semantic-modeling work is centered on Power BI.

## Repository Structure

```text
ecommerce-performance-dashboard/
├── README.md
├── .gitignore
├── assets/
├── data/
│   ├── README.md
│   └── sample/
├── docs/
│   ├── business_requirements.md
│   └── data_quality_report.md
├── powerbi/
└── validation/
    ├── requirements.txt
    └── validate_source_data.py
```

Additional documentation and dashboard assets will be added as the project progresses.

## Reproduce the Source Validation

Install the validation dependency:

```powershell
python -m pip install -r validation\requirements.txt
```

Run the validation script from the repository root:

```powershell
python validation\validate_source_data.py `
    --data-dir "D:\path\to\olist_data"
```

Expected result:

```text
VALIDATION PASSED: all source and baseline checks succeeded.
```

## Documentation

- [Business Requirements](docs/business_requirements.md)
- [Data Quality Report](docs/data_quality_report.md)
- [Data Setup and Attribution](data/README.md)

The data dictionary, metric definitions, semantic-model documentation, dashboard screenshots, and PBIX file will be added during the next project stages.

## Current Limitations

The dataset does not support reliable calculations for:

- Cost of goods sold
- Gross or net profit
- Marketing spend
- Customer acquisition cost
- Return on ad spend
- Inventory availability
- Refund value
- Customer demographics
- Accounting revenue

No unsupported cost, profit, marketing, or demographic fields are created.

## Author

**Vu Hong Vi**

- GitHub: [VuHongVi](https://github.com/VuHongVi)