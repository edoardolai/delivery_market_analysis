import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


conn1 = sqlite3.connect("./database/deliveroo.db")
conn2 = sqlite3.connect("./database/takeaway.db")
conn3 = sqlite3.connect("./database/ubereats.db")
# Create cursors
cur1 = conn1.cursor()
cur2 = conn2.cursor()
cur3 = conn3.cursor()


# Queries for fetching data from both databases
query = "SELECT name, delivery_fee, latitude, longitude FROM restaurants"
query1 = "SELECT deliveryFee, latitude, longitude FROM restaurants"

# Fetching data from the two connections
data = pd.read_sql_query(query, conn1)
data1 = pd.read_sql_query(query1, conn2)

# Renaming columns for consistency
data.rename(columns={'delivery_fee': 'deliveryFee'}, inplace=True)

# Ensure deliveryFee columns are numeric
data['deliveryFee'] = pd.to_numeric(data['deliveryFee'], errors='coerce')
data1['deliveryFee'] = pd.to_numeric(data1['deliveryFee'], errors='coerce')

# Merging the two datasets based on latitude and longitude
merged_data = pd.merge(data, data1, on=['latitude', 'longitude'], suffixes=('_deliveroo', '_takeaway'))

# Adding a column to calculate the numeric difference
merged_data['fee_difference'] = merged_data['deliveryFee_deliveroo'] - merged_data['deliveryFee_takeaway']

Fees = merged_data[merged_data['fee_difference'] != 0]
Fees = Fees.drop(columns=['latitude', 'longitude'])

# Export the Fees to a CSV file
Fees.to_csv('Fees.csv', index=False)
plt.bar(Fees['name'], Fees['deliveryFee_deliveroo'], Fees['deliveryFee_takeaway'], color='red')
plt.show()
