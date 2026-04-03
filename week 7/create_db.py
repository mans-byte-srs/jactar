import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="12345678"
)

conn.autocommit = True
cur = conn.cursor()

cur.execute("CREATE DATABASE phonebook_db")

print("Database created!")

cur.close()
conn.close()