
import pandas as pd
from pathlib import Path

# Find the project folder automatically
project_folder = Path(__file__).resolve().parent

# Load the sales dataset
file_path = project_folder / "data" / "raw" / "Sample - Superstore.csv"

df = pd.read_csv(file_path, encoding="latin1")

# Display basic information
print("===== SALES DATASET INSPECTION =====")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape (rows, columns):")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values in each column:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nData types:")
print(df.dtypes)

#Add date conversion and save cleaned data


# Convert date columns into proper date format
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Create a new column for shipping time in days
df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# Create month and year columns for sales analysis
df["Order Month"] = df["Order Date"].dt.month
df["Order Year"] = df["Order Date"].dt.year

# Save the cleaned dataset
output_folder = project_folder / "data" / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "superstore_cleaned.csv"
df.to_csv(output_file, index=False)

print("\n===== DATA CLEANING COMPLETE =====")
print("Order Date type:", df["Order Date"].dtype)
print("Ship Date type:", df["Ship Date"].dtype)
print("\nShipping Days summary:")
print(df["Shipping Days"].describe())
print("\nCleaned file saved to:", output_file)


# ==========================================
#  SALES PERFORMANCE KPI ANALYSIS
# ==========================================

# Total sales and profit
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()

# Total quantity sold
total_quantity = df["Quantity"].sum()

# Count unique orders and customers
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()

# Calculate profit margin
profit_margin = (total_profit / total_sales) * 100

# Calculate average order value
average_order_value = total_sales / total_orders

# Display KPI results
print("\n===== SALES PERFORMANCE KPIs =====")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Quantity Sold: {total_quantity:,}")
print(f"Total Orders: {total_orders:,}")
print(f"Unique Customers: {total_customers:,}")
print(f"Profit Margin: {profit_margin:.2f}%")
print(f"Average Order Value: ${average_order_value:,.2f}")


# ==========================================
# MONTHLY SALES ANALYSIS
# ==========================================

# Group sales and profit by month
monthly_sales = (
    df.groupby("Order Month")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    )
    .reset_index()
)

# Sort months from January to December
monthly_sales = monthly_sales.sort_values("Order Month")

print("\n===== MONTHLY SALES ANALYSIS =====")
print(monthly_sales.to_string(index=False))

# Identify the highest-sales month
best_month = monthly_sales.loc[
    monthly_sales["Total_Sales"].idxmax()
]

print("\nHighest-sales month:", int(best_month["Order Month"]))
print(f"Sales: ${best_month['Total_Sales']:,.2f}")

# Save the monthly analysis
monthly_sales.to_csv(
    project_folder / "data" / "processed" / "monthly_sales.csv",
    index=False
)

print("\nMonthly sales report saved successfully.")



# ==========================================
# CATEGORY SALES ANALYSIS
# ==========================================

category_sales = (
    df.groupby("Category")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Total_Sales", ascending=False)
)

print("\n===== CATEGORY SALES ANALYSIS =====")
print(category_sales.to_string(index=False))

category_sales.to_csv(
    project_folder / "data" / "processed" / "category_sales.csv",
    index=False
)

print("\nCategory sales report saved successfully.")



# ==========================================
# REGIONAL SALES ANALYSIS
# ==========================================

region_sales = (
    df.groupby("Region")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Total_Sales", ascending=False)
)

print("\n===== REGIONAL SALES ANALYSIS =====")
print(region_sales.to_string(index=False))

region_sales.to_csv(
    project_folder / "data" / "processed" / "region_sales.csv",
    index=False
)

print("\nRegional sales report saved successfully.")


# ==========================================
# SUB-CATEGORY PROFIT ANALYSIS
# ==========================================

subcategory_analysis = (
    df.groupby("Sub-Category")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Total_Profit", ascending=False)
)

print("\n===== SUB-CATEGORY PROFIT ANALYSIS =====")
print(subcategory_analysis.to_string(index=False))

subcategory_analysis.to_csv(
    project_folder / "data" / "processed" / "subcategory_analysis.csv",
    index=False
)

print("\nSub-category analysis saved successfully.")


# ==========================================
# PROJECT SUMMARY
# ==========================================

best_category = category_sales.loc[
    category_sales["Total_Sales"].idxmax()
]

best_region = region_sales.loc[
    region_sales["Total_Sales"].idxmax()
]

best_subcategory = subcategory_analysis.loc[
    subcategory_analysis["Total_Profit"].idxmax()
]

worst_subcategory = subcategory_analysis.loc[
    subcategory_analysis["Total_Profit"].idxmin()
]

summary = f"""
SALES PERFORMANCE DASHBOARD - PROJECT SUMMARY
=============================================

Total Sales: ${total_sales:,.2f}
Total Profit: ${total_profit:,.2f}
Total Orders: {total_orders:,}
Unique Customers: {total_customers:,}
Profit Margin: {profit_margin:.2f}%

Highest-Sales Category: {best_category['Category']}
Category Sales: ${best_category['Total_Sales']:,.2f}

Highest-Sales Region: {best_region['Region']}
Regional Sales: ${best_region['Total_Sales']:,.2f}

Most Profitable Sub-Category: {best_subcategory['Sub-Category']}
Sub-Category Profit: ${best_subcategory['Total_Profit']:,.2f}

Lowest-Profit Sub-Category: {worst_subcategory['Sub-Category']}
Sub-Category Profit: ${worst_subcategory['Total_Profit']:,.2f}
"""

summary_file = (
    project_folder / "data" / "processed" / "project_summary.txt"
)

summary_file.write_text(summary, encoding="utf-8")

print("\n===== PROJECT SUMMARY =====")
print(summary)
print("\nProject summary saved successfully.")


#.........................
#Check the CSV row count
#.........................

print("CSV row count:", len(df))
print("CSV columns:", len(df.columns))

# .........................
# check the saved CSV file itself
# .........................
cleaned_file = project_folder / "data" / "processed" / "superstore_cleaned.csv"
check_df = pd.read_csv(cleaned_file, encoding="utf-8")

print("Saved CSV rows:", len(check_df))
print("Saved CSV columns:", len(check_df.columns))




