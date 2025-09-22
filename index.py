import pandas as pd
import numpy as np

# Create a sample DataFrame that mimics the raw data with inconsistencies
data = {
    'Customer_ID': [101, 102, 103, 104, None, 106, 102],
    'Order Date': ['15-08-2023', '8/25/2023', '01-10-2023', '2023-11-05', '07-07-2023', '08/09/2023', '8/25/2023'],
    'Region': ['West', 'west', 'East', 'Central', 'West', 'West', 'west'],
    'Product Name': ['Laptop ', 'Mouse', 'Keyboard', 'Webcam', 'Mouse', 'Laptop', 'Mouse'],
    'Price ($)': [1200, 25, 75, np.nan, 25, 1200, 25],
    'Quantity': [1, -1, 2, 1, 1, 1, 1],
    'Sales Rep': ['John', 'Jane', 'Paul', 'Mary', 'Jane', 'John', 'Jane']
}
df = pd.DataFrame(data)
print(df)

# --- Data Cleaning and Preprocessing ---

## 1. Clean Column Headers
df.columns = (
    df.columns.str.lower()
              .str.strip()
              .str.replace(' ', '_')
              .str.replace(r'[\(\)\$]', '', regex=True)
)

# Rename trailing price_ → price
df.rename(columns={"price_": "price"}, inplace=True)

## 2. Remove Duplicate Rows
df.drop_duplicates(inplace=True)

## 3. Handle Missing Values
median_price = df['price'].median()
df['price'].fillna(median_price, inplace=True)

df['customer_id'].fillna(method='ffill', inplace=True)

## 4. Standardize Data Formats
df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True, errors='coerce')
df['region'] = df['region'].str.title().str.strip()
df['product_name'] = df['product_name'].str.strip()
df['quantity'] = df['quantity'].abs()

## 5. Check and Fix Data Types
df['price'] = pd.to_numeric(df['price'])
df['quantity'] = pd.to_numeric(df['quantity'])

# --- Display the Cleansed Dataset ---
print("Cleansed Dataset:")
print(df.reset_index(drop=True))