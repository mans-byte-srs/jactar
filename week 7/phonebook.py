import psycopg2
import csv

def connect():
    return psycopg2.connect(
        host="localhost",
        database="phonebook_db",
        user="postgres",
        password="12345678"
    )

# --- INSERT ---
def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()

    print("Added!")

# --- SELECT ---
def show_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()

# --- SEARCH ---
def search():
    name = input("Search name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", ('%' + name + '%',))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()

# --- UPDATE ---
def update():
    old_name = input("Old name: ")
    new_name = input("New name (Enter to skip): ")
    new_phone = input("New phone (Enter to skip): ")

    conn = connect()
    cur = conn.cursor()

    if new_name and new_phone:
        cur.execute(
            "UPDATE phonebook SET name=%s, phone=%s WHERE name=%s",
            (new_name, new_phone, old_name)
        )
    elif new_name:
        cur.execute(
            "UPDATE phonebook SET name=%s WHERE name=%s",
            (new_name, old_name)
        )
    elif new_phone:
        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE name=%s",
            (new_phone, old_name)
        )
    else:
        print("Nothing to update")

    conn.commit()
    cur.close()
    conn.close()

    print("Updated!")

# --- DELETE ---
def delete():
    name = input("Name to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE name=%s", (name,))

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted!")

# --- CSV IMPORT ---
def insert_from_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cur.execute(
                    "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                    (row["name"], row["phone"])
                )
            except:
                print("Skipped:", row)

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported!")

# --- MENU ---
def menu():
    while True:
        print("\n1 Add")
        print("2 Show all")
        print("3 Search")
        print("4 Update")
        print("5 Delete")
        print("6 Exit")
        print("7 Import from CSV")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            show_all()
        elif choice == "3":
            search()
        elif choice == "4":
            update()
        elif choice == "5":
            delete()
        elif choice == "6":
            break
        elif choice == "7":
            insert_from_csv()

menu()