# Data

## Data Source

This project uses the **Brazilian E-Commerce Public Dataset by Olist**.

- Publisher: Olist
- Source: [Kaggle – Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- License: CC BY-NC-SA 4.0
- Order purchase coverage: September 2016 to October 2018
- Primary dashboard period: January 2017 to August 2018

The dataset contains real commercial marketplace data that has been anonymized by the publisher.

## Repository Data Policy

The complete source CSV files are not stored in this repository.

Reasons:

- The complete dataset is unnecessarily large for the repository.
- The geolocation file contains more than one million rows.
- Users should obtain the original files directly from the publisher.
- Avoiding copied source files preserves clear attribution and provenance.

This repository does not contain internal company data, credentials, customer contact information, or private business data.

## Expected Source Files

Download and extract the following nine original CSV files:

```text
olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

Do not use cleaned, merged, SQLite, or third-party republished versions because their structure and row counts may differ from the validated source.

## Expected Row Counts

| Source file | Expected rows |
|---|---:|
| `olist_customers_dataset.csv` | 99,441 |
| `olist_geolocation_dataset.csv` | 1,000,163 |
| `olist_order_items_dataset.csv` | 112,650 |
| `olist_order_payments_dataset.csv` | 103,886 |
| `olist_order_reviews_dataset.csv` | 99,224 |
| `olist_orders_dataset.csv` | 99,441 |
| `olist_products_dataset.csv` | 32,951 |
| `olist_sellers_dataset.csv` | 3,095 |
| `product_category_name_translation.csv` | 71 |

## Local Data Setup

1. Download the dataset from the official Kaggle source.
2. Extract all nine CSV files into one local directory.
3. Do not rename or edit the source files.
4. Configure the Power BI `DataFolderPath` parameter to point to the local directory.

The Power BI solution will use a configurable folder parameter rather than a hard-coded personal path.

## Source Validation

Install the validation dependency:

```powershell
python -m pip install -r validation\requirements.txt
```

From the repository root, run:

```powershell
python validation\validate_source_data.py `
    --data-dir "D:\path\to\olist_data"
```

A valid source package should finish with:

```text
VALIDATION PASSED: all source and baseline checks succeeded.
```

See [`docs/data_quality_report.md`](../docs/data_quality_report.md) for the complete audit results, assumptions, exclusions, and validated KPI baselines.

## Sample Data

The `data/sample/` directory is reserved for small portfolio-safe samples or schema examples.

Any sample derived from the Olist dataset must:

- Preserve source attribution.
- Follow the CC BY-NC-SA 4.0 license.
- Contain no additional private or internal data.
- Not be presented as the complete source dataset.