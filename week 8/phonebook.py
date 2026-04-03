from connect import get_connection

def search_contacts(pattern):
    """Функция 1 — поиск по паттерну"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    print(f"\n--- Результаты поиска '{pattern}' ---")
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def get_paginated(limit, offset):
    """Функция 2 — пагинация"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    print(f"\n--- Страница (limit={limit}, offset={offset}) ---")
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def upsert_contact(name, phone):
    """Процедура 1 — вставить или обновить"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print(f"Upsert выполнен: {name} — {phone}")
    cur.close()
    conn.close()

def bulk_insert(names, phones):
    """Процедура 2 — массовая вставка с валидацией"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL bulk_insert_contacts(%s, %s)", (names, phones))
    conn.commit()
    print("Массовая вставка выполнена")
    cur.close()
    conn.close()

def delete_contact(name=None, phone=None):
    """Процедура 3 — удаление"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s, %s)", (name, phone))
    conn.commit()
    print(f"Удалено: name={name}, phone={phone}")
    cur.close()
    conn.close()

# ===== ТЕСТИРУЕМ =====
if __name__ == "__main__":
    # Тест 1: upsert
    upsert_contact("Aliya", "+77001234567")
    upsert_contact("Aliya", "+77009999999")  # обновит телефон

    # Тест 2: массовая вставка
    bulk_insert(
        ["Bekzat", "Dana", "WrongGuy"],
        ["+77001112233", "+77003334455", "abc-wrong"]
    )

    # Тест 3: поиск
    search_contacts("Ali")

    # Тест 4: пагинация
    get_paginated(3, 0)   # первые 3
    get_paginated(3, 3)   # следующие 3

    # Тест 5: удаление
    delete_contact(name="WrongGuy")