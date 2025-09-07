import psycopg2

conn = psycopg2.connect(
    dbname="finance_db",
    user="postgres",
    password="admin123",
    host="localhost",
    port="5432"
)
print("Connected!")
