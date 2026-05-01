import json
import csv
from connect import get_connection


# def insert_console(conn):
#     name = input("Name: ")
#     last_name = input("Last name: ")
#     phone = input("Phone: ")

#     cur = conn.cursor()
#     cur.execute("CALL upsert_user(%s, %s, %s, %s)", (name, last_name, phone))
#     conn.commit()
#     print("Saved!")
def insert_console(conn):
    cur = conn.cursor()

    # ввод всех данных
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    email = input("Email: ").strip()
    birthday = input("Birthday (YYYY-MM-DD): ").strip()

    phone = input("Phone: ").strip()
    phone_type = input("Phone type (home/work/mobile): ").strip()

    group_name = input("Group: ").strip()

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    group = cur.fetchone()

    if group is None:
        cur.execute(
            "INSERT INTO groups(name) VALUES (%s) RETURNING id",
            (group_name,)
        )
        group_id = cur.fetchone()[0]
    else:
        group_id = group[0]

    # --- вставка контакта ---
    cur.execute("""
        INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (first_name, last_name, email, birthday, group_id))

    contact_id = cur.fetchone()[0]

    # --- вставка телефона ---
    cur.execute("""
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
    """, (contact_id, phone, phone_type))

    conn.commit()
    print("Contact added successfully!")

def search(conn):
    q = input("Search: ")
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    rows = cur.fetchall()

    for r in rows:
        print(r)


def add_phone(conn):
    name = input("Name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    cur = conn.cursor()
    cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))
    conn.commit()
    print("Phone added!")


def move_group(conn):
    name = input("Name: ")
    group = input("Group: ")

    cur = conn.cursor()
    cur.execute("CALL move_to_group(%s,%s)", (name, group))
    conn.commit()
    print("Moved!")


def delete(conn):
    q = input("Name or phone: ")
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s)", (q,))
    conn.commit()
    print("Deleted!")


# def paginate(conn):
#     limit = int(input("Limit: "))
#     offset = int(input("Offset: "))

#     cur = conn.cursor()
#     cur.execute("SELECT * FROM get_contacts(%s,%s)", (limit, offset))

#     for row in cur.fetchall():
#         print(row)
def paginate(conn):
    cur = conn.cursor()

    limit = int(input("Items per page: "))
    offset = 0

    while True:
        cur.execute(
            "SELECT * FROM get_contacts(%s,%s)",
            (limit, offset)
        )
        rows = cur.fetchall()

        print("\n--- PAGE ---")
        if not rows:
            print("No data.")
        else:
            for r in rows:
                print(r)

        print("\nCommands: [n]ext | [p]rev | [q]uit")
        cmd = input("> ").lower()

        if cmd == 'n':
            offset += limit

        elif cmd == 'p':
            offset = max(0, offset - limit)

        elif cmd == 'q':
            break

        else:
            print("Invalid command")

def export_json(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT c.first_name, c.email, p.phone
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    data = cur.fetchall()

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Exported!")


def import_csv(conn):
    file = input("CSV file: ")

    cur = conn.cursor()

    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("CALL upsert_user(%s,%s,%s)", (row[0], row[1], row[2]))

    conn.commit()
    print("Imported!")


def menu():
    conn = get_connection()

    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Add contact")
        print("2. Search")
        print("3. Add phone")
        print("4. Move to group")
        print("5. Delete")
        print("6. Pagination")
        print("7. Export JSON")
        print("8. Import CSV")
        print("9. Exit")

        choice = input("> ")

        if choice == "1":
            insert_console(conn)
        elif choice == "2":
            search(conn)
        elif choice == "3":
            add_phone(conn)
        elif choice == "4":
            move_group(conn)
        elif choice == "5":
            delete(conn)
        elif choice == "6":
            paginate(conn)
        elif choice == "7":
            export_json(conn)
        elif choice == "8":
            import_csv(conn)
        elif choice == "9":
            break


if __name__ == "__main__":
    menu()