import telebot
import sqlite3

TOKEN = "7648931145:AAEn2p6FBVbzqgLhivlpTdZTLBcrxLcqNE0"  # Вставь сюда токен бота
bot = telebot.TeleBot(TOKEN)

# Подключение к базе данных
conn = sqlite3.connect("clicker.db", check_same_thread=False)
cursor = conn.cursor()

# Создаем таблицу, если ее нет
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    clicks INTEGER DEFAULT 0
)
""")
conn.commit()

# Функция для получения количества кликов пользователя
def get_clicks(user_id):
    cursor.execute("SELECT clicks FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO users (user_id, clicks) VALUES (?, ?)", (user_id, 0))
        conn.commit()
        return 0

# Функция для увеличения количества кликов
def add_click(user_id):
    cursor.execute("UPDATE users SET clicks = clicks + 1 WHERE user_id = ?", (user_id,))
    conn.commit()

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    get_clicks(user_id)  # Создаем запись, если ее нет

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_profile = telebot.types.KeyboardButton("📜 Профиль")
    btn_click = telebot.types.KeyboardButton("👆 Кликать")
    markup.add(btn_profile, btn_click)

    bot.send_message(message.chat.id, "Добро пожаловать в кликер! 👇", reply_markup=markup)

# Обработчик кнопок
@bot.message_handler(func=lambda message: message.text in ["📜 Профиль", "👆 Кликать"])
def handle_buttons(message):
    user_id = message.from_user.id

    if message.text == "📜 Профиль":
        clicks = get_clicks(user_id)
        bot.send_message(message.chat.id, f"📝 Ваш профиль:\n👆 Кликов: {clicks}")

    elif message.text == "👆 Кликать":
        add_click(user_id)
        clicks = get_clicks(user_id)
        bot.send_message(message.chat.id, f"🔼 +1 клик!\n👆 Всего кликов: {clicks}")

# Запуск бота
bot.polling(none_stop=True)