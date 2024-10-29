import telebot
import buttons as bt
import database as db
from geopy import Photon

# Инициализация базы данных и бота
db.init_db()
geolocator = Photon(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0")
bot =telebot.TeleBot(token="7880901995:AAEyWZDyn3-3YUz_9Y3yW-untNYIZzPCvxM")

# db.add_product("Бургер", 20000, "лучший бургер", 10, "https://d2jx2rerrg6sh3.cloudfront.net/images/news/ImageForNews_746157_1682409689757379.jpg")
# db.add_product("Чизбургер", 25000, "лучший чизбургер", 10, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf2535-40OVw2m6L8Auogu_w8LFXJfvV_XNw&s")
# db.add_product("Хотдог", 15000, "лучший хотдог", 0, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf2535-40OVw2m6L8Auogu_w8LFXJfvV_XNw&s")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Добро пожаловать! Выберите язык:", reply_markup=bt.language_buttons())

@bot.callback_query_handler(lambda call: call.data in ["lang_ru", "lang_uz"])
def choose_language(call):
    user_id = call.message.chat.id
    language = "ru" if call.data == "lang_ru" else "uz"
    db.update_user_language(user_id, language)  # Обновление языка в базе данных
    welcome_text = "Введите своё имя для регистрации" if language == "ru" else "Ro'yxatdan o'tish uchun ismingizni kiriting"
    bot.send_message(user_id, welcome_text)
    bot.register_next_step_handler(call.message, get_name, language)

def get_name(message, language):
    user_id = message.from_user.id
    name = message.text
    prompt_text = "Теперь поделитесь своим номером" if language == "ru" else "Telefon raqamingizni ulashing"
    bot.send_message(user_id, prompt_text, reply_markup=bt.phone_buttons(language))
    bot.register_next_step_handler(message, get_phone_number, name, language)

def get_phone_number(message, name, language):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        location_text = "Отправьте свою локацию" if language == "ru" else "Joylashuvingizni yuboring"
        bot.send_message(user_id, location_text, reply_markup=bt.location_button(language))
        bot.register_next_step_handler(message, get_location, name, phone_number, language)
    else:
        retry_text = "Отправьте свой номер через кнопку меню" if language == "ru" else "Telefon raqamingizni menyu tugmasi orqali yuboring"
        bot.send_message(user_id, retry_text)
        bot.register_next_step_handler(message, get_phone_number, name, language)

def get_location(message, name, phone_number, language):
    user_id = message.from_user.id
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        address = geolocator.reverse((latitude, longitude)).address
        db.add_user(name=name, phone_number=phone_number, user_id=user_id, address=address, language=language)
        confirmation_text = "Вы успешно зарегистрировались!" if language == "ru" else "Ro'yxatdan muvaffaqiyatli o'tdingiz!"
        bot.send_message(user_id, confirmation_text)
        bot.send_message(user_id, "Главное меню: " if language == "ru" else "Bosh menyu: ", reply_markup=bt.main_menu_kb(language))
    else:
        retry_location = "Отправьте свою локацию через кнопку меню" if language == "ru" else "Joylashuvingizni menyu tugmasi orqali yuboring"
        bot.send_message(user_id, retry_location)
        bot.register_next_step_handler(message, get_location, name, phone_number, language)

@bot.callback_query_handler(lambda call: call.data in ["cart", "back"])
def all_calls(call):
    user_id = call.message.user.id
    language = db.get_user_language(user_id)  # Получаем язык пользователя из БД
    if call.data == "cart":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Ваша корзина" if language == "ru" else "Savatchangiz")
    elif call.data == "back":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Главное меню: " if language == "ru" else "Bosh menyu: ", reply_markup=bt.main_menu_kb(language))

@bot.callback_query_handler(lambda call: "prod_" in call.data)
def get_prod_info(call):
    user_id = call.from_user.id  # Исправлено: используйте from_user вместо user
    language = db.get_user_language(user_id)  # Получаем язык пользователя из БД
    bot.delete_message(user_id, call.message.message_id)
    product_id = call.data.replace("prod_", "")
    product_info = db.get_exact_product(product_id)
    print(product_info)
    # Сохраняем инфу о продукте и его кол-ве
    bot.send_photo(user_id, photo=product_info[3], caption=f"{product_info[0]}\n\n"
                   f"{product_info[2]}\n"
                   f"Цена: {product_info[1]}",
                   reply_markup=bt.plus_minus_in(language=language))  # Передаем язык

@bot.message_handler(content_types=["text"])
def main_menu(message):
    user_id = message.from_user.id
    language = db.get_user_language(user_id)  # Получаем язык пользователя из БД
    if message.text == "🍴Меню":
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт:" if language == "ru" else "Tanlang:", reply_markup=bt.products_in(all_products, language=language))
    elif message.text == "🛒Корзина" if language == "ru" else "Savatcha":
        bot.send_message(user_id, "Ваша корзина" if language == "ru" else "Savatchangiz")
    elif message.text == "✒️Отзыв" if language == "ru" else "Fikr bildirish":
        bot.send_message(user_id, "Напишите текст вашего отзыва: " if language == "ru" else "Fikringizni yozing:")

bot.infinity_polling()
