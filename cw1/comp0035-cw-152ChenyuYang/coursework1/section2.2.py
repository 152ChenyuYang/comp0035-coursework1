import sqlite3
import pandas as pd
from pathlib import Path

# Define file paths
housing_supply_path = Path(
    r'C:\Users\YANG\Desktop\cw1\comp0035-cw-152ChenyuYang\dclg-affordable-housing-borough.xlsx'
)
waiting_list_path = Path(
    r'C:\Users\YANG\Desktop\cw1\comp0035-cw-152ChenyuYang\households-on-local-authority-waiting-list.xlsx'
)

# Connect to SQLite database (creates a new one if it doesn't exist)
conn = sqlite3.connect('affordable_housing_project.db')
cursor = conn.cursor()

# Step 1: Create the database table structure
cursor.execute('''
CREATE TABLE IF NOT EXISTS AREA (
    code TEXT PRIMARY KEY,
    name TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS YEAR (
    year INTEGER PRIMARY KEY
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS WAITING_LIST (
    waiting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER,
    areaCode TEXT,
    householdsCount INTEGER,
    FOREIGN KEY (year) REFERENCES YEAR(year),
    FOREIGN KEY (areaCode) REFERENCES AREA(code)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS AFFORDABLE_HOUSING (
    housing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER,
    areaCode TEXT,
    housingUnits INTEGER,
    FOREIGN KEY (year) REFERENCES YEAR(year),
    FOREIGN KEY (areaCode) REFERENCES AREA(code)
)
''')
conn.commit()

# Step 2: Read data from the Excel files
affordable_housing_data = pd.read_excel(housing_supply_path, sheet_name=1, dtype=str)
waiting_list_data = pd.read_excel(waiting_list_path, sheet_name=1, dtype=str)

# Clean column names
affordable_housing_data.columns = (
    affordable_housing_data.columns.str.strip()
    .str.replace('\n', '').str.replace(' ', '')
)
waiting_list_data.columns = (
    waiting_list_data.columns.str.strip()
    .str.replace('\n', '').str.replace(' ', '')
)

# Dynamically generate column names based on actual columns
affordable_housing_data.columns = ['Code', 'current_code', 'Area'] + list(
    range(1997, 1997 + affordable_housing_data.shape[1] - 3)
)
waiting_list_data.columns = ['Code', 'current_code', 'Area'] + list(
    range(1997, 1997 + waiting_list_data.shape[1] - 3)
)

# Convert to long format for affordable housing data
affordable_housing_long = affordable_housing_data.melt(
    id_vars=['Code', 'current_code', 'Area'],
    var_name='year',
    value_name='housingUnits'
)
affordable_housing_long.dropna(subset=['housingUnits'], inplace=True)
affordable_housing_long.rename(columns={'current_code': 'areaCode', 'Area': 'name'}, inplace=True)

# Convert to long format for waiting list data
waiting_list_long = waiting_list_data.melt(
    id_vars=['Code', 'current_code', 'Area'],
    var_name='year',
    value_name='householdsCount'
)
waiting_list_long.dropna(subset=['householdsCount'], inplace=True)
waiting_list_long.rename(columns={'current_code': 'areaCode', 'Area': 'name'}, inplace=True)

# Step 3: Insert data into the database
# Insert AREA data
areas = pd.concat([
    affordable_housing_long[['areaCode', 'name']],
    waiting_list_long[['areaCode', 'name']]
]).drop_duplicates()
areas.to_sql('AREA', conn, if_exists='replace', index=False)

# Insert YEAR data
years = pd.concat([
    affordable_housing_long['year'],
    waiting_list_long['year']
]).drop_duplicates().astype(int)
years_df = pd.DataFrame(years, columns=['year'])
years_df.to_sql('YEAR', conn, if_exists='replace', index=False)

# Insert AFFORDABLE_HOUSING data
affordable_housing_long['year'] = affordable_housing_long['year'].astype(int)
affordable_housing_long.to_sql('AFFORDABLE_HOUSING', conn, if_exists='replace', index=False)

# Insert WAITING_LIST data
waiting_list_long['year'] = waiting_list_long['year'].astype(int)
waiting_list_long.to_sql('WAITING_LIST', conn, if_exists='replace', index=False)

# Step 4: Verify data import
affordable_count = pd.read_sql_query(
    "SELECT COUNT(*) as count FROM AFFORDABLE_HOUSING", conn
)
waiting_list_count = pd.read_sql_query(
    "SELECT COUNT(*) as count FROM WAITING_LIST", conn
)

# Display the total number of records imported
print(f"Affordable Housing Data Count: {affordable_count['count'].values[0]}")
print(f"Waiting List Data Count: {waiting_list_count['count'].values[0]}")

# Close the database connection
conn.close()
