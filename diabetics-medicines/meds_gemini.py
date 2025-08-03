import pandas as pd
import numpy as np

# --- 1. Pharmacy Collection Data (Inflows) ---
collected_data = {
    'Date': pd.to_datetime([
        '2025-05-12', '2025-05-12', '2025-06-04', '2025-06-04',
        '2025-06-17', '2025-07-01', '2025-07-01', '2025-07-01',
        '2025-07-23', '2025-07-23'
    ]),
    'Name': [
        'Metformin', 'Atorvastatin', 'Metformin', 'Atorvastatin',
        'Metformin', 'Metformin', 'Atorvastatin', 'Dapagliflozin',
        'Atorvastatin', 'Dapagliflozin'
    ],
    'Quantity': [56.0, 28.0, 56.0, 28.0, 84.0, 56.0, 28.0, 28.0, 28.0, 28.0],
    'Size (mg)': [500.0, 20.0, 500.0, 20.0, 500.0, 1000.0, 40.0, 5.0, 40.0, 5.0]
}
df_collected_raw = pd.DataFrame(collected_data)
df_collected_raw['Total_Mg_Collected'] = df_collected_raw['Quantity'] * df_collected_raw['Size (mg)']
df_collected_inflows = df_collected_raw.pivot_table(
    index='Date',
    columns='Name',
    values='Total_Mg_Collected',
    aggfunc='sum'
).fillna(0) # Fill NaN collections with 0

print("Pharmacy Collection (Inflows) - Total Mg:")
print(df_collected_inflows)

# --- 2. Prescribed Dose Change Data (Daily Consumption Rate from second table) ---
prescribed_data = {
    'Datetime': [ # Using the exact data you provided for this part
        '2025-05-12 06:00:00', '2025-05-12 18:00:00', '2025-05-19 06:00:00',
        '2025-05-19 18:00:00', '2025-05-26 06:00:00', '2025-05-26 12:00:00',
        '2025-05-26 18:00:00', '2025-06-17 06:00:00', '2025-06-17 18:00:00',
        '2025-07-01 06:00:00', '2025-07-01 12:00:00', '2025-07-01 18:00:00',
        '2025-07-01 18:00:00'
    ],
    'Name': [
        'Metformin', 'Atorvastatin', 'Metformin', 'Metformin',
        'Metformin', 'Metformin', 'Metformin', 'Metformin',
        'Metformin', 'Metformin', 'Dapagliflozin', 'Atorvastatin',
        'Metformin' # For the duplicate
    ],
    'Dose (mg)': [
        500.0, 20.0, 500.0, 500.0, 500.0, 500.0, 500.0, 1000.0, 500.0,
        1000.0, 5.0, 40.0, 1000.0
    ]
}
df_prescribed_raw = pd.DataFrame(prescribed_data)
df_prescribed_raw['Datetime'] = pd.to_datetime(df_prescribed_raw['Datetime'])

# Handle duplicates (same timestamp, same medicine, take last dose) and pivot
df_prescribed_changes = df_prescribed_raw.groupby(['Datetime', 'Name'])['Dose (mg)'].last().unstack()

print("\nPrescribed Dose Changes (raw unstacked - source of daily rate):")
print(df_prescribed_changes)

# --- Define the full date range for the inventory ---
# Start from earliest collection date or earliest prescription date, whichever is first
start_inventory_date = min(df_collected_raw['Date'].min().normalize(), df_prescribed_raw['Datetime'].min().normalize())
end_inventory_date = pd.to_datetime('2025-07-31').normalize()

# Create a dense daily timeline for consumption
full_daily_timeline_index = pd.date_range(start=start_inventory_date, end=end_inventory_date, freq='D')

# Reindex the prescribed changes to the daily timeline and forward-fill
# This makes the prescribed dose continuous until a new change occurs.
df_daily_prescribed_dose = df_prescribed_changes.reindex(full_daily_timeline_index)
df_daily_prescribed_dose = df_daily_prescribed_dose.ffill()

# For medicines that have *never* had a prescription recorded *before* the start date of our range,
# their initial ffilled value will be NaN. We should treat this as 0 consumption.
df_daily_consumption = df_daily_prescribed_dose.fillna(0) # Fill initial NaNs with 0

print("\nDaily Prescribed Dose (Daily Consumption Rate - after ffill and initial fillna(0)):")
print(df_daily_consumption.head(10)) # Show more to see the ffill effect
print("\n... (continues until 2025-07-31)")
print(df_daily_consumption.tail())


# --- 3. Inventory Calculation ---

# Get all unique medicine names from both datasets to ensure all columns are present
all_medicines = pd.Index(list(df_collected_inflows.columns) + list(df_daily_consumption.columns)).unique()
all_medicines = all_medicines.sort_values() # Consistent column order

# Reindex both inflows and consumption to ensure they have the same columns and fill missing with 0
df_collected_inflows = df_collected_inflows.reindex(columns=all_medicines, fill_value=0)
df_daily_consumption = df_daily_consumption.reindex(columns=all_medicines, fill_value=0)

# Create an empty DataFrame to hold all daily transactions (inflows and outflows)
df_transactions = pd.DataFrame(0.0, index=full_daily_timeline_index, columns=all_medicines)

# Add inflows (positive)
# Ensure collection dates are aligned to the daily index.
df_transactions.loc[df_collected_inflows.index, df_collected_inflows.columns] += df_collected_inflows

# Add outflows (negative)
# Subtract the daily consumption from the transaction DataFrame
df_transactions -= df_daily_consumption # Consumption is positive, so subtract it from stock

print("\nDaily Transactions (Inflows - Outflows):")
print(df_transactions.head(10))
print("...")


# 4. Calculate the cumulative sum to get the running balance (inventory)
# We assume starting inventory is 0 for all medicines.
df_inventory = df_transactions.cumsum()

# Fill any remaining NaNs with 0 (e.g., if a medicine was never collected/prescribed but is in all_medicines)
df_inventory = df_inventory.fillna(0)

print("\nInventory at the End of Each Day (Left for Next Day):")
print(df_inventory)
