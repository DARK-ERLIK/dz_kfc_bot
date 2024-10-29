from telebot import types

def language_buttons():
    kb = types.InlineKeyboardMarkup()
    btn_ru = types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
    btn_uz = types.InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang_uz")
    kb.add(btn_ru, btn_uz)
    return kb

def phone_buttons(language):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Поделиться номером" if language == "ru" else "Telefon raqamingizni ulashing", request_contact=True)
    kb.add(button)
    return kb

def location_button(language):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Поделиться локацией" if language == "ru" else "Joylashuvingizni yuboring", request_location=True)
    kb.add(button)
    return kb

def main_menu_kb(language=None):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if language == "ru":
        menu = types.KeyboardButton(text="🍴Меню")
        cart = types.KeyboardButton(text="🛒Корзина")
        feedback = types.KeyboardButton(text="✒️Отзыв")
    elif language == "uz":
        menu = types.KeyboardButton(text="🍴Menyu")
        cart = types.KeyboardButton(text="🛒Savatcha")
        feedback = types.KeyboardButton(text="✒️Fikr bildirish")
    else:
        menu = types.KeyboardButton(text="🍴Меню")
        cart = types.KeyboardButton(text="🛒Корзина")
        feedback = types.KeyboardButton(text="✒️Отзыв")

    kb.add(menu, cart)
    kb.row(feedback)
    return kb

def products_in(products, language="ru"):  # Убедитесь, что language передается в параметры
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Статичные кнопки
    cart = types.InlineKeyboardButton(text="Корзина" if language == "ru" else "Savatcha", callback_data="cart")
    back = types.InlineKeyboardButton(text="Назад" if language == "ru" else "Ortga", callback_data="back")

    # Динамичные кнопки
    all_products = [types.InlineKeyboardButton(text=f"{product[1]}", callback_data=f"prod_{product[0]}")
                    for product in products]

    kb.add(*all_products)
    kb.row(cart)
    kb.row(back)
    return kb

def plus_minus_in(plus_or_minus="", current_amount=1, language="ru"):  # Добавьте language в параметры
    kb = types.InlineKeyboardMarkup(row_width=3)
    back = types.InlineKeyboardButton(text="назад" if language == "ru" else "ortga", callback_data="main_menu")
    to_cart = types.InlineKeyboardButton(text="Добавить в корзину" if language == "ru" else "Savatchaga qo'shish", callback_data="to_cart")
    minus = types.InlineKeyboardButton(text="-", callback_data="minus")
    plus = types.InlineKeyboardButton(text="+", callback_data="plus")
    count = types.InlineKeyboardButton(text=f"{current_amount}", callback_data="none")

    # Логика для изменения кнопок
    if plus_or_minus == "plus":
        new_amount = current_amount + 1
        count = types.InlineKeyboardButton(text=f"{new_amount}", callback_data="none")
    elif plus_or_minus == "minus":
        if current_amount > 1:
            new_amount = current_amount - 1
            count = types.InlineKeyboardButton(text=f"{new_amount}", callback_data="none")

    kb.row(minus, count, plus)
    kb.row(to_cart)
    kb.row(back)
    return kb
