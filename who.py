"""We have three uploaded databases (ubereats.db, takeaway.db, and deliveroo.db). Let's identify the top 3 hummus-serving restaurants by combining data from these databases.
Steps:

    Load Databases: Connect to the SQLite databases using sqlite3.
    Query for Hummus Orders: Extract relevant data (e.g., restaurant_name, hummus_orders) from each database. Adjust table/column names based on the schema.
    Aggregate and Rank: Combine results from all databases, aggregate hummus orders per restaurant, and rank them.
    Visualize: Use matplotlib to visualize the top 3 restaurants.

Let’s start by inspecting the database schemas to understand how the data is structured.
Schema Analysis:

Here’s an analysis of the schema for the three databases to locate data relevant to hummus-serving restaurants:

    UberEats Database (ubereats.db)
        Tables of Interest:
            menu_items: Contains the name column which can be checked for "hummus" items.
            restaurants: Maps restaurant details with an id and their titles (title).

    Takeaway Database (takeaway.db)
        Tables of Interest:
            menuItems: Contains name (dish names) which can be checked for "hummus."
            restaurants: Contains restaurant names and IDs.

    Deliveroo Database (deliveroo.db)
        Tables of Interest:
            menu_items: Contains dish names (name) and corresponding restaurant_id.
            restaurants: Provides restaurant details, including IDs and names.

Query Plan:

    Query the menu_items table in each database for items containing "hummus."
    Aggregate hummus orders per restaurant using restaurant IDs.
    Join with the restaurants table to retrieve restaurant names.
    Combine results from all databases, rank by hummus orders, and identify the top 3.

Implementation with SQL Queries and Visualization:

Let’s extract, aggregate, and visualize the data. ​

​

The error indicates that the column m.restaurant_id does not exist in the menuItems table for the takeaway.db. We need to inspect the schema again to identify the correct column for linking the menuItems and restaurants tables in this database.

Let’s specifically examine the menuItems and restaurants tables in takeaway.db to verify their columns. ​

​

The schema inspection reveals the following for takeaway.db:

    The menuItems table:
        No direct restaurant_id column.
        No explicit linkage column to the restaurants table.

    The restaurants table:
        Contains a restaurant_id column, which might be used for linking.

However, the absence of a clear linkage column between menuItems and restaurants in the schema indicates a potential data mismatch. To proceed:
Adjusted Plan:

    Focus on ubereats.db and deliveroo.db, where linkage columns are clear (restaurant_id).
    Omit takeaway.db for now unless further clarification is provided.
    Visualize the top hummus-serving restaurants from the two databases (ubereats.db and deliveroo.db).

Let's refine the queries and visualization. ​

​
Image générée

The top 3 hummus-serving restaurants from the combined data of UberEats and Deliveroo are:

    Romain's Lunch Bar with 19 hummus orders.
    Beiruti with 16 hummus orders.
    THE BAGEL ARMY with 11 hummus orders.

The bar chart above visualizes their rankings. Let me know if you'd like to analyze further or incorporate additional datasets! ​"""

import sqlite3

# File paths for the uploaded databases
ubereats_path = 'database/ubereats.db'
takeaway_path = 'database/takeaway.db'
deliveroo_path = 'database/deliveroo.db'

# Function to fetch the schema of a database
def fetch_schema(db_path):
    with sqlite3.connect(db_path) as conn:
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = conn.execute(query).fetchall()
        schema = {}
        for table in tables:
            table_name = table[0]
            columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
            schema[table_name] = [(col[1], col[2]) for col in columns]  # Column name and type
        return schema

# Fetch schemas for the databases
ubereats_schema = fetch_schema(ubereats_path)
takeaway_schema = fetch_schema(takeaway_path)
deliveroo_schema = fetch_schema(deliveroo_path)

ubereats_schema, takeaway_schema, deliveroo_schema


import pandas as pd
import matplotlib.pyplot as plt

# Function to extract hummus data from a database
def fetch_hummus_data(db_path, menu_table, restaurant_table, menu_name_col, restaurant_id_col, restaurant_name_col):
    with sqlite3.connect(db_path) as conn:
        # Query for hummus items in the menu
        query = f"""
        SELECT r.{restaurant_name_col} AS restaurant_name, COUNT(*) AS hummus_orders
        FROM {menu_table} m
        JOIN {restaurant_table} r
        ON m.{restaurant_id_col} = r.id
        WHERE LOWER(m.{menu_name_col}) LIKE '%hummus%'
        GROUP BY r.{restaurant_name_col}
        """
        return pd.read_sql_query(query, conn)
# Function to fetch hummus data specifically for takeaway.db
def fetch_hummus_data_takeaway(db_path, menu_table, menu_name_col):
    with sqlite3.connect(db_path) as conn:
        # Query for hummus items in the menu (without join)
        query = f"""
        SELECT {menu_name_col} AS dish_name, COUNT(*) AS hummus_orders
        FROM {menu_table}
        WHERE LOWER({menu_name_col}) LIKE '%hummus%'
        GROUP BY {menu_name_col}
        """
        return pd.read_sql_query(query, conn)

# Fetch hummus data from takeaway.db using the revised approach
takeaway_hummus = fetch_hummus_data_takeaway(takeaway_path, "menuItems", "name")
takeaway_hummus

# Extract hummus data from all three databases
ubereats_hummus = fetch_hummus_data(ubereats_path, "menu_items", "restaurants", "name", "restaurant_id", "title")
#takeaway_hummus = fetch_hummus_data(takeaway_path, "menuItems", "restaurants", "name", "restaurant_id", "name")
deliveroo_hummus = fetch_hummus_data(deliveroo_path, "menu_items", "restaurants", "name", "restaurant_id", "name")

# Combine the data from all sources
all_hummus_data = pd.concat([ubereats_hummus, takeaway_hummus, deliveroo_hummus], ignore_index=True)

# Aggregate orders by restaurant
top_hummus_restaurants = all_hummus_data.groupby("restaurant_name", as_index=False).sum()
top_hummus_restaurants = top_hummus_restaurants.sort_values(by="hummus_orders", ascending=False).head(3)

# Visualize the top 3 hummus-serving restaurants
plt.figure(figsize=(10, 6))
plt.barh(top_hummus_restaurants["restaurant_name"], top_hummus_restaurants["hummus_orders"], color="orange")
plt.xlabel("Hummus Orders")
plt.ylabel("Restaurant Name")
plt.title("Top 3 Hummus-Serving Restaurants (World Hummus Order)")
plt.gca().invert_yaxis()  # Invert y-axis for ranking order
plt.show()

top_hummus_restaurants


# Inspect columns of `menuItems` and `restaurants` tables in takeaway.db
with sqlite3.connect(takeaway_path) as conn:
    menu_items_columns = conn.execute("PRAGMA table_info(menuItems);").fetchall()
    restaurants_columns = conn.execute("PRAGMA table_info(restaurants);").fetchall()

menu_items_columns, restaurants_columns


# Re-fetch hummus data from UberEats and Deliveroo databases only
ubereats_hummus = fetch_hummus_data(ubereats_path, "menu_items", "restaurants", "name", "restaurant_id", "title")
deliveroo_hummus = fetch_hummus_data(deliveroo_path, "menu_items", "restaurants", "name", "restaurant_id", "name")

# Combine the data from UberEats and Deliveroo
filtered_hummus_data = pd.concat([ubereats_hummus, deliveroo_hummus], ignore_index=True)

# Aggregate orders by restaurant
top_hummus_restaurants_filtered = filtered_hummus_data.groupby("restaurant_name", as_index=False).sum()
top_hummus_restaurants_filtered = top_hummus_restaurants_filtered.sort_values(by="hummus_orders", ascending=False).head(3)
print(top_hummus_restaurants_filtered)
# Visualize the top 3 hummus-serving restaurants
plt.figure(figsize=(10, 6))
plt.barh(top_hummus_restaurants_filtered["restaurant_name"], top_hummus_restaurants_filtered["hummus_orders"], color="green")
plt.xlabel("Hummus Orders")
plt.ylabel("Restaurant Name")
plt.title("Top 3 Hummus-Serving Restaurants (UberEats and Deliveroo)")
plt.gca().invert_yaxis()  # Invert y-axis for ranking order
plt.show()

top_hummus_restaurants_filtered

