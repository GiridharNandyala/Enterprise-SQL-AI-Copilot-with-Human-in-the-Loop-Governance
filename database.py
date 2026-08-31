import sqlite3
import pandas as pd

DB_NAME = "enterprise.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Customers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        region TEXT,
        join_date DATE
    )
    """)

    # Products Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        price REAL
    )
    """)

    # Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        order_date DATE,
        amount REAL,
        status TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """)

    # Sample Data Insertions
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM orders")

    customers_data = [
        (101, 'Aarav Sharma', 'South', '2023-01-15'),
        (102, 'Priya Reddy', 'South', '2023-02-20'),
        (103, 'Vikram Verma', 'North', '2023-03-10'),
        (104, 'Ananya Patel', 'West', '2023-04-05'),
        (105, 'Rohan Gupta', 'East', '2023-05-12'),
        (106, 'Sai Kumar', 'South', '2023-06-18'),
        (107, 'Kavya Singh', 'North', '2023-07-22')
    ]
    cursor.executemany("INSERT INTO customers VALUES (?,?,?,?)", customers_data)

    products_data = [
        (201, 'Enterprise AI Platform', 'Software', 15000.0),
        (202, 'Cloud Data Analytics Suite', 'Software', 8000.0),
        (203, 'Hardware Server Rack', 'Hardware', 25000.0),
        (204, 'Cybersecurity Audit Service', 'Services', 12000.0),
        (205, 'Database Storage License', 'Software', 5000.0)
    ]
    cursor.executemany("INSERT INTO products VALUES (?,?,?,?)", products_data)

    orders_data = [
        (1, 101, 201, '2024-01-10', 15000.0, 'Completed'),
        (2, 102, 202, '2024-01-15', 8000.0, 'Completed'),
        (3, 103, 203, '2024-02-01', 25000.0, 'Pending'),
        (4, 101, 205, '2024-02-14', 5000.0, 'Completed'),
        (5, 104, 204, '2024-02-20', 12000.0, 'Cancelled'),
        (6, 105, 201, '2024-03-05', 15000.0, 'Completed'),
        (7, 106, 202, '2024-03-12', 8000.0, 'Completed'),
        (8, 102, 204, '2024-03-22', 12000.0, 'Completed'),
        (9, 107, 203, '2024-04-01', 25000.0, 'Pending')
    ]
    cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", orders_data)

    conn.commit()
    conn.close()
    print("Database enterprise.db initialized with sample data successfully.")

def execute_query(sql_query: str):
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df, None
    except Exception as e:
        conn.close()
        return None, str(e)

if __name__ == "__main__":
    init_db()