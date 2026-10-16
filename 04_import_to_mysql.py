
import pandas as pd
import mysql.connector
from getpass import getpass
from pathlib import Path

# Find the cleaned CSV file
project_folder = Path(__file__).resolve().parent
csv_file = project_folder / "data" / "processed" / "superstore_cleaned.csv"

df = pd.read_csv(csv_file)
print("CSV rows found:", len(df))

# Enter your MySQL password securely when prompted
password = getpass.getpass("Enter your MySQL password: ")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="sales_dashboard"
)

cursor = connection.cursor()

# Create a separate table so existing tables remain unchanged
cursor.execute("""
CREATE TABLE superstore_python_import (
    `Row ID` INT,
    `Order ID` VARCHAR(50),
    `Order Date` VARCHAR(30),
    `Ship Date` VARCHAR(30),
    `Ship Mode` VARCHAR(50),
    `Customer ID` VARCHAR(50),
    `Customer Name` VARCHAR(150),
    `Segment` VARCHAR(50),
    `Country` VARCHAR(100),
    `City` VARCHAR(100),
    `State` VARCHAR(100),
    `Postal Code` INT NULL,
    `Region` VARCHAR(50),
    `Product ID` VARCHAR(50),
    `Category` VARCHAR(50),
    `Sub-Category` VARCHAR(50),
    `Product Name` TEXT,
    `Sales` DOUBLE,
    `Quantity` INT,
    `Discount` DOUBLE,
    `Profit` DOUBLE,
    `Shipping Days` INT,
    `Order Month` INT,
    `Order Year` INT
)
""")

columns = ", ".join(f"`{col}`" for col in df.columns)
placeholders = ", ".join(["%s"] * len(df.columns))

sql = f"INSERT INTO superstore_python_import ({columns}) VALUES ({placeholders})"

# Convert missing values to SQL NULL
rows = [
    tuple(None if pd.isna(value) else value for value in row)
    for row in df.itertuples(index=False, name=None)
]

for start in range(0, len(rows), 500):
    cursor.executemany(sql, rows[start:start + 500])
    connection.commit()

cursor.execute("SELECT COUNT(*) FROM superstore_python_import")
count = cursor.fetchone()[0]

print("Rows imported into MySQL:", count)

cursor.close()
connection.close()
print("Import completed!")
