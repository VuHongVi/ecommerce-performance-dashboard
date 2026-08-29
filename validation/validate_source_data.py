"""Validate the original Olist source files and analytical baselines.

Usage:
    python validation/validate_source_data.py --data-dir "D:\olist_dataset_review"
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import pandas as pd


EXPECTED_ROW_COUNTS = {
    "olist_customers_dataset.csv": 99_441,
    "olist_geolocation_dataset.csv": 1_000_163,
    "olist_order_items_dataset.csv": 112_650,
    "olist_order_payments_dataset.csv": 103_886,
    "olist_order_reviews_dataset.csv": 99_224,
    "olist_orders_dataset.csv": 99_441,
    "olist_products_dataset.csv": 32_951,
    "olist_sellers_dataset.csv": 3_095,
    "product_category_name_translation.csv": 71,
}

REPORTING_START = pd.Timestamp("2017-01-01")
REPORTING_END = pd.Timestamp("2018-09-01")

failures: list[str] = []


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Olist source data and reporting baselines."
    )
    parser.add_argument(
        "--data-dir",
        required=True,
        type=Path,
        help="Directory containing the nine original Olist CSV files.",
    )
    return parser.parse_args()


def count_csv_records(path: Path) -> int:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.reader(file)
        next(reader)
        return sum(1 for _ in reader)


def read_csv(
    data_dir: Path,
    filename: str,
    usecols: list[str] | None = None,
) -> pd.DataFrame:
    return pd.read_csv(
        data_dir / filename,
        usecols=usecols,
        dtype="string",
        low_memory=False,
    )


def check_equal(
    label: str,
    actual: int,
    expected: int,
) -> None:
    if actual == expected:
        print(f"PASS | {label}: {actual:,}")
    else:
        message = (
            f"FAIL | {label}: "
            f"actual={actual:,}, expected={expected:,}"
        )
        failures.append(message)
        print(message)


def check_close(
    label: str,
    actual: float,
    expected: float,
    tolerance: float = 0.01,
) -> None:
    if math.isclose(
        actual,
        expected,
        abs_tol=tolerance,
        rel_tol=0,
    ):
        print(f"PASS | {label}: {actual:,.6f}")
    else:
        message = (
            f"FAIL | {label}: "
            f"actual={actual:,.6f}, "
            f"expected={expected:,.6f}"
        )
        failures.append(message)
        print(message)


def check_key(
    label: str,
    dataframe: pd.DataFrame,
    columns: list[str],
) -> None:
    missing_rows = int(
        dataframe[columns]
        .isna()
        .any(axis=1)
        .sum()
    )

    duplicate_rows = int(
        dataframe.duplicated(
            subset=columns,
            keep=False,
        ).sum()
    )

    check_equal(
        f"{label} missing-key rows",
        missing_rows,
        0,
    )

    check_equal(
        f"{label} duplicate-key rows",
        duplicate_rows,
        0,
    )


def check_foreign_key(
    label: str,
    child: pd.DataFrame,
    child_column: str,
    parent: pd.DataFrame,
    parent_column: str,
) -> None:
    child_values = child[child_column].dropna()
    parent_values = parent[parent_column].dropna()

    unmatched_rows = int(
        (~child_values.isin(parent_values)).sum()
    )

    check_equal(
        f"{label} unmatched rows",
        unmatched_rows,
        0,
    )


def main() -> None:
    arguments = parse_arguments()
    data_dir = arguments.data_dir.resolve()

    if not data_dir.is_dir():
        raise SystemExit(
            f"Data directory does not exist: {data_dir}"
        )

    print("=" * 72)
    print("FILE INVENTORY")
    print("=" * 72)

    for filename, expected_rows in EXPECTED_ROW_COUNTS.items():
        path = data_dir / filename

        if not path.is_file():
            message = f"FAIL | Missing source file: {filename}"
            failures.append(message)
            print(message)
            continue

        actual_rows = count_csv_records(path)

        check_equal(
            f"{filename} rows",
            actual_rows,
            expected_rows,
        )

    if failures:
        print("\nSource inventory failed. Further checks were stopped.")
        raise SystemExit(1)

    customers = read_csv(
        data_dir,
        "olist_customers_dataset.csv",
    )

    geolocation = read_csv(
        data_dir,
        "olist_geolocation_dataset.csv",
        ["geolocation_zip_code_prefix"],
    )

    order_items = read_csv(
        data_dir,
        "olist_order_items_dataset.csv",
    )

    payments = read_csv(
        data_dir,
        "olist_order_payments_dataset.csv",
    )

    reviews = read_csv(
        data_dir,
        "olist_order_reviews_dataset.csv",
        [
            "review_id",
            "order_id",
            "review_score",
            "review_creation_date",
            "review_answer_timestamp",
        ],
    )

    orders = read_csv(
        data_dir,
        "olist_orders_dataset.csv",
    )

    products = read_csv(
        data_dir,
        "olist_products_dataset.csv",
    )

    sellers = read_csv(
        data_dir,
        "olist_sellers_dataset.csv",
    )

    translations = read_csv(
        data_dir,
        "product_category_name_translation.csv",
    )

    print("\n" + "=" * 72)
    print("KEY INTEGRITY")
    print("=" * 72)

    check_key(
        "Customers.customer_id",
        customers,
        ["customer_id"],
    )

    check_key(
        "Orders.order_id",
        orders,
        ["order_id"],
    )

    check_key(
        "OrderItems.order_id + order_item_id",
        order_items,
        ["order_id", "order_item_id"],
    )

    check_key(
        "Payments.order_id + payment_sequential",
        payments,
        ["order_id", "payment_sequential"],
    )

    check_key(
        "Products.product_id",
        products,
        ["product_id"],
    )

    check_key(
        "Sellers.seller_id",
        sellers,
        ["seller_id"],
    )

    check_key(
        "Translations.product_category_name",
        translations,
        ["product_category_name"],
    )

    print("\n" + "=" * 72)
    print("REFERENTIAL INTEGRITY")
    print("=" * 72)

    check_foreign_key(
        "Orders -> Customers",
        orders,
        "customer_id",
        customers,
        "customer_id",
    )

    check_foreign_key(
        "OrderItems -> Orders",
        order_items,
        "order_id",
        orders,
        "order_id",
    )

    check_foreign_key(
        "OrderItems -> Products",
        order_items,
        "product_id",
        products,
        "product_id",
    )

    check_foreign_key(
        "OrderItems -> Sellers",
        order_items,
        "seller_id",
        sellers,
        "seller_id",
    )

    check_foreign_key(
        "Payments -> Orders",
        payments,
        "order_id",
        orders,
        "order_id",
    )

    check_foreign_key(
        "Reviews -> Orders",
        reviews,
        "order_id",
        orders,
        "order_id",
    )

    print("\n" + "=" * 72)
    print("SOURCE QUALITY BASELINES")
    print("=" * 72)

    check_equal(
        "Distinct customer_unique_id",
        int(customers["customer_unique_id"].nunique()),
        96_096,
    )

    check_equal(
        "Distinct geolocation ZIP prefixes",
        int(
            geolocation[
                "geolocation_zip_code_prefix"
            ].nunique()
        ),
        19_015,
    )

    check_equal(
        "Missing product categories",
        int(products["product_category_name"].isna().sum()),
        610,
    )

    product_categories = (
        products["product_category_name"].dropna()
    )

    untranslated_products = int(
        (
            ~product_categories.isin(
                translations["product_category_name"]
            )
        ).sum()
    )

    check_equal(
        "Products with untranslated named categories",
        untranslated_products,
        13,
    )

    check_equal(
        "Repeated review IDs",
        int(
            (
                reviews.groupby("review_id").size() > 1
            ).sum()
        ),
        789,
    )

    check_equal(
        "Orders with multiple review rows",
        int(
            (
                reviews.groupby("order_id").size() > 1
            ).sum()
        ),
        547,
    )

    check_equal(
        "Distinct reviewed orders",
        int(reviews["order_id"].nunique()),
        98_673,
    )

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"],
        errors="coerce",
    )

    orders["order_approved_at"] = pd.to_datetime(
        orders["order_approved_at"],
        errors="coerce",
    )

    orders["order_delivered_carrier_date"] = pd.to_datetime(
        orders["order_delivered_carrier_date"],
        errors="coerce",
    )

    orders["order_delivered_customer_date"] = pd.to_datetime(
        orders["order_delivered_customer_date"],
        errors="coerce",
    )

    orders["order_estimated_delivery_date"] = pd.to_datetime(
        orders["order_estimated_delivery_date"],
        errors="coerce",
    )

    check_equal(
        "Delivered orders missing customer delivery date",
        int(
            (
                (orders["order_status"] == "delivered")
                & orders[
                    "order_delivered_customer_date"
                ].isna()
            ).sum()
        ),
        8,
    )

    check_equal(
        "Carrier handoff before approval",
        int(
            (
                orders["order_approved_at"].notna()
                & orders[
                    "order_delivered_carrier_date"
                ].notna()
                & (
                    orders["order_delivered_carrier_date"]
                    < orders["order_approved_at"]
                )
            ).sum()
        ),
        1_359,
    )

    check_equal(
        "Customer delivery before carrier handoff",
        int(
            (
                orders[
                    "order_delivered_carrier_date"
                ].notna()
                & orders[
                    "order_delivered_customer_date"
                ].notna()
                & (
                    orders[
                        "order_delivered_customer_date"
                    ]
                    < orders[
                        "order_delivered_carrier_date"
                    ]
                )
            ).sum()
        ),
        23,
    )

    print("\n" + "=" * 72)
    print("REVIEW RESOLUTION")
    print("=" * 72)

    reviews["review_score"] = pd.to_numeric(
        reviews["review_score"],
        errors="coerce",
    )

    reviews["review_creation_date"] = pd.to_datetime(
        reviews["review_creation_date"],
        errors="coerce",
    )

    reviews["review_answer_timestamp"] = pd.to_datetime(
        reviews["review_answer_timestamp"],
        errors="coerce",
    )

    latest_reviews = (
        reviews.sort_values(
            [
                "order_id",
                "review_answer_timestamp",
                "review_creation_date",
                "review_id",
            ],
            na_position="first",
        )
        .drop_duplicates(
            subset=["order_id"],
            keep="last",
        )
    )

    check_equal(
        "Latest-review rows",
        len(latest_reviews),
        98_673,
    )

    check_close(
        "Latest-review average score",
        float(latest_reviews["review_score"].mean()),
        4.086386,
        tolerance=0.000001,
    )

    print("\n" + "=" * 72)
    print("COMMERCIAL BASELINES")
    print("=" * 72)

    order_items["price"] = pd.to_numeric(
        order_items["price"],
        errors="coerce",
    )

    order_items["freight_value"] = pd.to_numeric(
        order_items["freight_value"],
        errors="coerce",
    )

    payments["payment_value"] = pd.to_numeric(
        payments["payment_value"],
        errors="coerce",
    )

    item_by_order = (
        order_items.groupby("order_id", as_index=False)
        .agg(
            merchandise_gmv=("price", "sum"),
            freight_value=("freight_value", "sum"),
            item_count=("order_id", "size"),
        )
    )

    item_by_order["item_plus_freight"] = (
        item_by_order["merchandise_gmv"]
        + item_by_order["freight_value"]
    )

    payment_by_order = (
        payments.groupby("order_id", as_index=False)
        .agg(
            payment_total=("payment_value", "sum"),
        )
    )

    reporting_orders = orders.loc[
        (orders["order_status"] == "delivered")
        & (
            orders["order_purchase_timestamp"]
            >= REPORTING_START
        )
        & (
            orders["order_purchase_timestamp"]
            < REPORTING_END
        )
    ].copy()

    commercial = (
        reporting_orders[
            [
                "order_id",
                "customer_id",
                "order_purchase_timestamp",
            ]
        ]
        .merge(
            item_by_order,
            on="order_id",
            how="left",
            validate="one_to_one",
        )
        .merge(
            payment_by_order,
            on="order_id",
            how="left",
            validate="one_to_one",
        )
    )

    check_equal(
        "Delivered orders in reporting period",
        len(commercial),
        96_211,
    )

    check_equal(
        "Delivered orders missing items",
        int(commercial["item_count"].isna().sum()),
        0,
    )

    check_equal(
        "Delivered orders missing payments",
        int(commercial["payment_total"].isna().sum()),
        0,
    )

    check_equal(
        "Item rows in reporting period",
        int(commercial["item_count"].sum()),
        109_880,
    )

    check_close(
        "Merchandise GMV",
        float(commercial["merchandise_gmv"].sum()),
        13_181_027.13,
    )

    check_close(
        "Freight Value",
        float(commercial["freight_value"].sum()),
        2_192_092.88,
    )

    check_close(
        "Merchandise plus Freight",
        float(commercial["item_plus_freight"].sum()),
        15_373_120.01,
    )

    check_close(
        "Total Paid",
        float(commercial["payment_total"].sum()),
        15_375_875.44,
    )

    check_close(
        "Merchandise AOV",
        float(
            commercial["merchandise_gmv"].sum()
            / len(commercial)
        ),
        137.00124860982632,
        tolerance=0.000001,
    )

    commercial["payment_difference"] = (
        commercial["payment_total"]
        - commercial["item_plus_freight"]
    )

    check_equal(
        "Orders with payment difference above 0.01",
        int(
            (
                commercial["payment_difference"].abs()
                > 0.01
            ).sum()
        ),
        370,
    )

    print("\n" + "=" * 72)
    print("CUSTOMER BASELINES")
    print("=" * 72)

    order_customers = orders.merge(
        customers[
            [
                "customer_id",
                "customer_unique_id",
            ]
        ],
        on="customer_id",
        how="left",
        validate="one_to_one",
    )

    delivered_history = (
        order_customers.loc[
            order_customers["order_status"] == "delivered"
        ]
        .sort_values(
            [
                "customer_unique_id",
                "order_purchase_timestamp",
                "order_id",
            ]
        )
        .copy()
    )

    delivered_history["observed_order_number"] = (
        delivered_history.groupby("customer_unique_id")
        .cumcount()
        + 1
    )

    reporting_customers = delivered_history.loc[
        (
            delivered_history["order_purchase_timestamp"]
            >= REPORTING_START
        )
        & (
            delivered_history["order_purchase_timestamp"]
            < REPORTING_END
        )
    ]

    check_equal(
        "Distinct reporting-period customers",
        int(
            reporting_customers[
                "customer_unique_id"
            ].nunique()
        ),
        93_104,
    )

    check_equal(
        "New customer orders",
        int(
            (
                reporting_customers[
                    "observed_order_number"
                ]
                == 1
            ).sum()
        ),
        93_094,
    )

    check_equal(
        "Returning customer orders",
        int(
            (
                reporting_customers[
                    "observed_order_number"
                ]
                > 1
            ).sum()
        ),
        3_117,
    )

    check_equal(
        "Customers with a returning order",
        int(
            reporting_customers.loc[
                reporting_customers[
                    "observed_order_number"
                ]
                > 1,
                "customer_unique_id",
            ].nunique()
        ),
        2_798,
    )

    print("\n" + "=" * 72)

    if failures:
        print(f"VALIDATION FAILED: {len(failures)} check(s) failed.")

        for failure in failures:
            print(f"- {failure}")

        raise SystemExit(1)

    print("VALIDATION PASSED: all source and baseline checks succeeded.")


if __name__ == "__main__":
    main()