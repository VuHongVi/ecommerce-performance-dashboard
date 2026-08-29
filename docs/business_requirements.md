# Business Requirements

## 1. Project Overview

The E-commerce Performance Dashboard is a Power BI portfolio project built with the Brazilian E-Commerce Public Dataset by Olist.

The project focuses on Power Query transformation, dimensional modeling, DAX, dashboard design, data validation, and business storytelling. It is intended to demonstrate the ability to turn multi-table e-commerce data into reliable management information.

## 2. Primary Stakeholder

### Marketplace Performance Manager

The primary stakeholder is responsible for monitoring marketplace performance, identifying commercial growth drivers, and prioritizing operational improvements.

### Secondary Stakeholders

- Category Manager
- Customer Experience Manager
- Fulfillment and Logistics Manager

The dashboard is designed primarily for management users rather than technical users.

## 3. Business Problem

Olist marketplace data is distributed across multiple tables with different grains, including orders, order items, customers, payments, reviews, products, sellers, and geolocation records.

Management needs a consolidated and reliable view of:

- Overall commercial performance
- Product-category contribution
- Customer purchasing behavior
- Delivery performance
- Customer experience

Without a controlled semantic model, combining these tables can produce duplicated orders, inflated GMV, incorrect customer counts, and misleading review metrics.

## 4. Project Objective

The objective is to build an interactive Power BI dashboard that helps marketplace management:

1. Monitor commercial performance over time.
2. Identify the drivers of growth or decline.
3. Evaluate product-category contribution and concentration.
4. Understand new and returning customer behavior.
5. Monitor delivery performance across regions and sellers.
6. Evaluate the relationship between delivery performance and customer reviews.
7. Identify areas that require management attention.

## 5. Reporting Scope

| Item | Definition |
|---|---|
| Dataset | Brazilian E-Commerce Public Dataset by Olist |
| Dataset source period | September 2016 to October 2018 |
| Primary reporting period | January 1, 2017 to August 31, 2018 |
| Currency | Brazilian Real (BRL) |
| Primary commercial population | Delivered orders within the reporting period |
| Customer identifier | `customer_unique_id` |
| Order identifier | `order_id` |
| Primary date | `order_purchase_timestamp` |
| Primary commercial value | Merchandise GMV |
| Delivery population | Delivered orders with valid delivery dates |
| Review population | Orders with a valid selected review |

The incomplete periods in 2016 and September–October 2018 are excluded from the primary reporting scope to avoid misleading time comparisons.

## 6. Business Questions

### 6.1 Executive Overview

1. How do Merchandise GMV, delivered orders, customers, and Average Order Value change over time?
2. How does current performance compare with the previous month or previous year?
3. Is commercial growth driven by customer volume, order volume, or Average Order Value?
4. Which states and regions contribute the most to marketplace performance?
5. How is the marketplace performing against its previous period?

### 6.2 Product and Customer Analysis

1. Which product categories contribute the most Merchandise GMV and delivered orders?
2. Which categories are growing or declining?
3. Is marketplace performance overly concentrated in a small number of categories?
4. How do new-customer orders and returning-customer orders differ?
5. What is the observed repeat-purchase rate?
6. Which customer groups contribute the most value and purchase frequency?

### 6.3 Delivery and Customer Experience

1. How do delivery time and on-time delivery rate change over time?
2. Which states, sellers, or product categories experience the most delivery delays?
3. How large is the difference between actual and estimated delivery dates?
4. Is late delivery associated with lower review scores?
5. Which high-value sellers have poor delivery or review performance?

## 7. KPI Principles

### Merchandise GMV

Merchandise GMV is based on the sum of order-item `price` values for delivered orders. It excludes freight and must not be interpreted as Olist's accounting revenue or commission income.

### Freight Value

Freight Value is reported separately from Merchandise GMV.

### Total Paid

Total Paid is based on the sum of `payment_value`. It is maintained separately because it does not reconcile exactly with Merchandise GMV plus freight for every order.

### Average Order Value

Average Order Value is defined as Merchandise GMV divided by distinct delivered orders.

### New and Returning Orders

A customer's delivered orders are sequenced using the full observed dataset history before applying the reporting-period filter:

- Order number 1: New Customer Order
- Order number greater than 1: Returning Customer Order

“New customer” means the first delivered purchase observed in the available dataset. Purchases before the dataset began are unknown.

### Review Score

When multiple reviews exist for one order, the latest review is selected using `review_answer_timestamp`, followed by `review_creation_date` and `review_id` as deterministic tie-breakers.

### Delivery Time

Delivery Time is measured from `order_purchase_timestamp` to `order_delivered_customer_date`.

### Late Delivery

An order is considered late when:

`order_delivered_customer_date > order_estimated_delivery_date`

Orders without a valid delivery date are excluded from delivery-time and late-delivery calculations.

## 8. Functional Requirements

The dashboard should:

- Contain approximately three report pages.
- Provide clear navigation between pages.
- Support filtering by date, state, product category, and seller where appropriate.
- Display current-period and prior-period comparisons.
- Use consistent KPI definitions across all pages.
- Prevent double counting across orders, items, payments, and reviews.
- Present actionable insights for non-technical management users.
- Use concise labels, tooltips, and explanatory notes where necessary.

## 9. Out of Scope

The following analyses are excluded because the dataset does not provide sufficient supporting data:

- Cost of goods sold
- Gross profit or net profit
- Profit margin
- Marketing spend
- Customer acquisition cost
- Return on ad spend
- Inventory and stock-out analysis
- Refund value and return rate
- Customer demographics
- Accounting revenue
- Predictive Customer Lifetime Value

No synthetic cost, profit, marketing, or demographic fields will be created.

## 10. Data Limitations and Assumptions

- The dataset contains real commercial data that has been anonymized.
- The available history does not represent the complete lifetime of every customer.
- The dataset contains incomplete months outside the primary reporting period.
- Some products have missing or untranslated categories.
- Some orders do not contain items, payments, reviews, or completed delivery dates.
- Review identifiers are not globally unique in the source data.
- Customer location may change between orders and is therefore treated as an order-level delivery attribute.
- Payment totals differ slightly from item price plus freight for a small number of orders.
- Source-level financial differences are retained and are not artificially corrected.

## 11. Success Criteria

The project is considered successful when:

1. The Power BI model uses controlled fact and dimension grains.
2. Core KPIs reconcile with independently validated baselines.
3. The dashboard answers the agreed business questions.
4. Time comparisons exclude incomplete reporting periods.
5. Customer, order, item, payment, and review metrics are not double counted.
6. The report is clear and usable for management decision-making.
7. Documentation explains metric definitions, assumptions, limitations, and data-quality decisions.