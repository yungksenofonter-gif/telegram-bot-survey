import os
import telebot
import datetime
from datetime import datetime as dt

# Замени на свой токен
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TARGET_CHAT_ID = -1002159699404

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

QUESTIONS = [
    ("Как вас зовут?", "name"),
    ("Какой автомобиль вас интересует?", "car_model"),
    ("Какой ценовой диапазон?", "price_range"),
]

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_data[user_id] = {'step': 0, 'answers': {}}
    bot.send_message(user_id, "Привет! Ответьте пожалуйста на несколько вопросов")
    bot.send_message(user_id, QUESTIONS[0][0])

@bot.message_handler(commands=['cancel'])
def cancel(message):
    user_id = message.chat.id
    if user_id in user_data:
        del user_data[user_id]
    bot.send_message(user_id, "Опрос отменен")

@bot.message_handler(func=lambda message: message.chat.id in user_data)
def handle_answer(message):
    user_id = message.chat.id
    step = user_data[user_id]['step']
    
    if step < len(QUESTIONS):
        question, field = QUESTIONS[step]
        user_data[user_id]['answers'][field] = message.text
        user_data[user_id]['step'] += 1
        
        if user_data[user_id]['step'] < len(QUESTIONS):
            bot.send_message(user_id, QUESTIONS[step + 1][0])
        else:
            answers = user_data[user_id]['answers']
            username = f"@{message.from_user.username}" if message.from_user.username else f"id{user_id}"
            time_str = datetime.now().strftime("%H:%M, %d %b %Y")
            
            form_text = f"Ответ пользователя {username}\nВремя: {time_str}\n\n"
            for question, field in QUESTIONS:
                form_text += f"Вопрос: {question}\nОтвет: {answers.get(field, 'N/A')}\n\n"
            
            bot.send_message(TARGET_CHAT_ID, form_text)
            bot.send_message(user_id, "✅ Спасибо! Заявка отправлена, мы свяжемся с вами в ближайшее время.")
            del user_data[user_id]

if __name__ == "__main__":
    print("Бот работает...")
    bot.infinity_polling()
