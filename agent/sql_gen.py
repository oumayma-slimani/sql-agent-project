import duckdb
import os
from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conn = duckdb.connect()

def load_data():
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers AS 
        SELECT * FROM 'data/olist_customers_dataset.csv'
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders AS 
        SELECT * FROM 'data/olist_orders_dataset.csv'
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS order_items AS 
        SELECT * FROM 'data/olist_order_items_dataset.csv'
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS payments AS 
        SELECT * FROM 'data/olist_order_payments_dataset.csv'
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products AS 
        SELECT * FROM 'data/olist_products_dataset.csv'
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sellers AS 
        SELECT * FROM 'data/olist_sellers_dataset.csv'
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews AS 
        SELECT * FROM 'data/olist_order_reviews_dataset.csv'
    """)

def get_schema():
    tables = ['customers', 'orders', 'order_items', 
              'payments', 'products', 'sellers', 'reviews']
    schema = ""
    for table in tables:
        result = conn.execute(f"DESCRIBE {table}").fetchall()
        schema += f"\nTable: {table}\n"
        for row in result:
            schema += f"  - {row[0]} ({row[1]})\n"
    return schema

def generate_sql(question):
    schema = get_schema()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""You are a SQL expert working with DuckDB.
Here is the database schema:
{schema}

Rules:
- Return ONLY the SQL query, nothing else
- No markdown, no backticks, no explanation
- Always use table names exactly as shown above
- Write clean, efficient SQL"""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    return response.choices[0].message.content.strip()

def run_query(sql):
    try:
        df = conn.execute(sql).df()
        return df, None
    except Exception as e:
        return None, str(e)

def fix_sql(sql, error, question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a SQL expert. Fix the broken SQL query. Return ONLY the fixed SQL, nothing else."
            },
            {
                "role": "user",
                "content": f"Question: {question}\nBroken SQL: {sql}\nError: {error}"
            }
        ]
    )
    return response.choices[0].message.content.strip() 