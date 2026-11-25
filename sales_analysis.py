
"""
Seasonal Drink Sales Analysis
Analysis of fictional seasonal drink sales data using Python.

Note: All data in this project is fictional and generated
for learning and portfolio purposes.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Generate fictional sales data
np.random.seed(42)

dates = pd.date_range("2026-09-01", periods=28, freq="D")

products = {
    "Honey Cream Latte": 590,
    "Berry Yogurt Frappuccino": 680,
    "Caramel Apple Tea": 560
}

records = []

for date in dates:
    for product, price in products.items():
        weekday = date.dayofweek
        promotion = np.random.choice([0, 1], p=[0.7, 0.3])
        temperature = np.random.randint(18, 31)

        base_sales = {
            "Honey Cream Latte": 35,
            "Berry Yogurt Frappuccino": 42,
            "Caramel Apple Tea": 28
        }[product]

        weekend_effect = 12 if weekday >= 5 else 0
        promotion_effect = 15 if promotion == 1 else 0
        weather_effect = 8 if (
            product == "Berry Yogurt Frappuccino"
            and temperature >= 27
        ) else 0

        cups = max(
            5,
            int(
                base_sales
                + weekend_effect
                + promotion_effect
                + weather_effect
                + np.random.normal(0, 7)
            )
        )

        records.append({
            "date": date,
            "product": product,
            "price": price,
            "promotion": promotion,
            "temperature": temperature,
            "weekday": date.day_name(),
            "cups_sold": cups,
            "sales_amount": cups * price
        })

df = pd.DataFrame(records)

# 2. Create output folder
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

df.to_csv(
    output_dir / "fictional_sales_data.csv",
    index=False
)

# 3. Analyze sales by product
product_summary = df.groupby("product").agg(
    total_cups=("cups_sold", "sum"),
    total_sales=("sales_amount", "sum"),
    average_cups=("cups_sold", "mean")
).sort_values("total_cups", ascending=False)

print("\n=== Sales by Product ===")
print(product_summary.round(1))

# 4. Compare weekday and weekend sales
df["day_type"] = np.where(
    df["date"].dt.dayofweek >= 5,
    "Weekend",
    "Weekday"
)

day_summary = df.groupby("day_type")["cups_sold"].mean()

print("\n=== Weekday vs Weekend ===")
print(day_summary.round(1))

# 5. Compare promotional and non-promotional sales
promotion_summary = df.groupby("promotion")["cups_sold"].mean()

print("\n=== Promotion Analysis ===")
print(promotion_summary.round(1))

# 6. Visualize the results
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Product sales
product_summary["total_cups"].plot(
    kind="bar",
    ax=axes[0, 0],
    title="Total Cups Sold by Product"
)
axes[0, 0].set_ylabel("Cups Sold")
axes[0, 0].tick_params(axis="x", rotation=20)

# Daily sales trend
daily_sales = df.groupby("date")["cups_sold"].sum()
daily_sales.plot(
    ax=axes[0, 1],
    marker="o",
    title="Daily Sales Trend"
)
axes[0, 1].set_ylabel("Cups Sold")

# Weekday and weekend comparison
day_summary.plot(
    kind="bar",
    ax=axes[1, 0],
    title="Average Sales: Weekday vs Weekend"
)
axes[1, 0].set_ylabel("Average Cups Sold")
axes[1, 0].tick_params(axis="x", rotation=0)

# Promotion comparison
promotion_summary.rename(
    index={0: "No Promotion", 1: "Promotion"}
).plot(
    kind="bar",
    ax=axes[1, 1],
    title="Average Sales by Promotion"
)
axes[1, 1].set_ylabel("Average Cups Sold")
axes[1, 1].tick_params(axis="x", rotation=0)

plt.tight_layout()

plt.savefig(
    output_dir / "sales_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

# 7. Print business insights
best_product = product_summary["total_cups"].idxmax()
best_day = day_summary.idxmax()

promotion_difference = (
    promotion_summary.loc[1]
    - promotion_summary.loc[0]
)

print("\n=== Business Insights ===")
print(f"Best-selling product: {best_product}")
print(f"Higher average sales period: {best_day}")
print(
    "Average sales difference between "
    f"promotion and non-promotion: "
    f"{promotion_difference:.1f} cups"
)

print("\nAnalysis completed successfully!")
print("Files saved in the output folder.")
