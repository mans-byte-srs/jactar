def create_profile(username, city):
    print(f"Пользователь: {username}, Город: {city}")

def format_text(text, uppercase=False):
    return text.upper() if uppercase else text.lower()

def final_price(base_price, discount=0):
    return base_price * (1 - discount / 100)

print(create_profile("Ivan_99", "Москва"))
print(format_text("Hello Python", True))
print(f"К оплате: {final_price(1000, 15)} руб.")