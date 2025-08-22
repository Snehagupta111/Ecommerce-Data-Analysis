import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Connect to MySQL
dbcon = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Reyansh@2017",
    database="ecommerce_db"
)

# 2. Load tables into Pandas

df_customers = pd.read_sql("SELECT * FROM customers", con=dbcon)
df_products = pd.read_sql("SELECT * FROM products", con=dbcon)
df_orders = pd.read_sql("SELECT * FROM orders", con=dbcon)

print("Customers Table:")
print(df_customers.head())
print("\nProducts Table:")
print(df_products.head())
print("\nOrders Table:")
print(df_orders.head())


# 3. Total revenue per customer
df_customer_revenue = pd.read_sql("""
    SELECT c.Customer_ID, c.Name, SUM(o.Quantity * p.Price) AS Total_Revenue
    FROM Customers c
    JOIN Orders o ON c.Customer_ID = o.Customer_ID
    JOIN Products p ON o.Product_ID = p.Product_ID
    GROUP BY c.Customer_ID, c.Name
    ORDER BY Total_Revenue DESC
""", con=dbcon)

print("\nTop Customers by Revenue:")
print(df_customer_revenue.head(10))


# 4. Top 5 products by revenue

df_top_products = pd.read_sql("""
    SELECT p.Product_Id, p.Name, SUM(o.Quantity * p.Price) AS Product_Revenue
    FROM Products p
    JOIN Orders o ON p.Product_Id = o.Product_id
    GROUP BY p.Product_Id, p.Name
    ORDER BY Product_Revenue DESC
    LIMIT 5
""", con=dbcon)

print("\nTop 5 Products by Revenue:")
print(df_top_products)

# 5. Top 5 customers by revenue

df_top_customers = df_customer_revenue.head(5)
print("\nTop 5 Customers:")
print(df_top_customers)

# 6. Top 5 products by revenue (with category)

df_top_products_category = pd.read_sql("""
    SELECT p.Name, p.Category, SUM(p.Price*o.Quantity) AS Product_Revenue
    FROM Products p
    JOIN Orders o ON p.Product_Id= o.Product_Id
    GROUP BY p.Product_Id, p.Name, p.Category
    ORDER BY Product_Revenue DESC
    LIMIT 5
""", con=dbcon)

print("\nTop 5 Products with Category:")
print(df_top_products_category)

# 7. Monthly revenue
df_monthly_revenue = pd.read_sql("""
    SELECT 
        YEAR(o.Order_date) AS Year,
        MONTH(o.Order_date) AS Month,
        SUM(o.Quantity * p.Price) AS Total_Revenue
    FROM Orders o
    JOIN Products p ON o.Product_Id = p.Product_Id
    GROUP BY YEAR(o.Order_date), MONTH(o.Order_date)
    ORDER BY Year, Month
""", con=dbcon)

print("\nMonthly Revenue:")
print(df_monthly_revenue)


# 8. Visualizations
sns.set_style("whitegrid")

# a Top 5 Products by Revenue
plt.figure(figsize=(8,5))
sns.barplot(x='Product_Revenue', y='Name', data=df_top_products, palette='viridis')
plt.title("Top 5 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product Name")
plt.show()

# b Top 5 Customers by Revenue
plt.figure(figsize=(8,5))
sns.barplot(x='Total_Revenue', y='Name', data=df_top_customers, palette='magma')
plt.title("Top 5 Customers by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Customer Name")
plt.show()

# c Monthly Revenue Trend
plt.figure(figsize=(10,5))
df_monthly_revenue['Month_Year'] = df_monthly_revenue['Year'].astype(str) + '-' + df_monthly_revenue['Month'].astype(str)
sns.lineplot(x='Month_Year', y='Total_Revenue', data=df_monthly_revenue, marker='o', color='green')
plt.xticks(rotation=45)
plt.title("Monthly Revenue Trend")
plt.ylabel("Revenue")
plt.xlabel("Month-Year")
plt.show()
