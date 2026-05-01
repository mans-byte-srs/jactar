def make_pizza(size, *toppings, **details):
    """
    *toppings собирает любое кол-во добавок в кортеж.
    **details собирает дополнительные параметры в словарь.
    """
    print(f"\nГотовим пиццу размером {size} см.")
    print(f"Добавки: {toppings}")
    for key, value in details.items():
        print(f"- {key}: {value}")

# Передаем размер, список добавок и детали (адрес, время)
make_pizza(30, "пепперони", "грибы", "сыр", address="ул. Пушкина", delivery_time="20:00")

# Сложение всех чисел (*args)
def sum_all(*numbers):
    return sum(numbers)

# Логгер событий (**kwargs)
def log_event(event_name, **details):
    print(f"Событие: {event_name}")
    for key, value in details.items():
        print(f"  - {key}: {value}")

# Комбинированный вариант
def print_order(customer, *items, **shipping_info):
    print(f"Заказ для {customer}: {', '.join(items)}")
    print(f"Доставка: {shipping_info.get('method', 'Стандарт')}")

print(f"Сумма: {sum_all(10, 20, 30, 40)}")
log_event("Вход в систему", user="admin", ip="192.168.1.1", status="success")
print_order("Анна", "Книга", "Ручка", method="Курьер", address="Офис")