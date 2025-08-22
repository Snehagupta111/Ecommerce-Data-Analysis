CREATE DATABASE ecommerce_db;
USE ecommerce_db;
CREATE table customers(
Customer_Id int Primary key,
Name VARCHAR(50),
Email VARCHAR(50),
City varchar(20),
Join_Date Date
);
CREATE table products(
Product_Id int primary key,
Name  varchar(50),
Category varchar(30),
Price decimal(10,2)
);

CREATE table orders(
Order_Id int primary key,
Customer_id int,
Product_id int,
Order_date date ,
Quantity int,
FOREIGN  KEY  (Customer_Id) references customers(Customer_Id),
FOREIGN KEY (Product_Id) references products(Product_Id)
);
insert into customers (Customer_Id,Name,Email,City,Join_Date) 
values(1, 'Amit Sharma', 'amit@example.com', 'Delhi', '2021-05-10'),
(2, 'Priya Singh', 'priya@example.com', 'Mumbai', '2022-07-15'),
(3, 'Rahul Mehta', 'rahul@example.com', 'Bangalore', '2023-01-20'),
(4, 'Neha Kapoor', 'neha@example.com', 'Pune', '2021-11-30'),
(5, 'Rohit Verma', 'rohit@example.com', 'Delhi', '2023-03-12');

insert into products(Product_Id,Name,Category,Price)
values(101, 'Laptop', 'Electronics', 55000.00),
(102, 'Smartphone', 'Electronics', 25000.00),
(103, 'Headphones', 'Accessories', 2000.00),
(104, 'Chair', 'Furniture', 3500.00),
(105, 'Desk', 'Furniture', 7000.00);

 SELECT c.Name, 
       SUM(o.Quantity * p.Price) AS total_spent
FROM Orders o
JOIN Customers c ON o.Customer_Id = c.Customer_Id
JOIN Products p ON o.Product_Id = p.Product_Id
GROUP BY c.Name
ORDER BY total_spent DESC
LIMIT 5;

select p.name from products p left join orders o 
on p.Product_Id=o.Product_Id where o.Order_Id  is null;

SELECT 
    YEAR(o.Order_Date) AS year,
    MONTH(o.Order_Date) AS month,
    SUM(o.Quantity * p.Price) AS month_revenue
FROM Orders o
INNER JOIN Products p ON o.Product_Id = p.Product_Id
GROUP BY YEAR(o.Order_Date), MONTH(o.Order_Date)
ORDER BY year, month;

SELECT 
    p.Name AS Product_Name,
    SUM(o.Quantity) AS Total_Quantity_Sold
FROM Products p
INNER JOIN Orders o ON p.Product_Id = o.Product_Id
GROUP BY p.Name
ORDER BY Total_Quantity_Sold DESC
LIMIT 1;

SELECT 
    c.Name AS Customer_Name,
    p.Name AS Product_Name,
    o.Order_Date AS Date,
    o.Quantity AS Quantity
FROM Orders o
INNER JOIN Customers c ON o.Customer_Id = c.Customer_Id
INNER JOIN Products p ON o.Product_Id = p.Product_Id
WHERE p.Name = 'Laptop';

SELECT 
    c.Name AS Customer_Name,
    AVG(o.Quantity * p.Price) AS Avg_Order_Value
FROM Orders o
INNER JOIN Customers c ON o.Customer_Id = c.Customer_Id
INNER JOIN Products p ON o.Product_Id = p.Product_Id
GROUP BY c.Name
ORDER BY Avg_Order_Value DESC;

SELECT 
    p.Category,
    SUM(o.Quantity * p.Price) AS Total_Sales
FROM Orders o
INNER JOIN Products p ON o.Product_Id = p.Product_Id
GROUP BY p.Category
ORDER BY Total_Sales DESC;
