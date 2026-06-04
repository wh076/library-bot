import os
import telebot
from dotenv import load_dotenv
from utils.logger import log_user_action
from utils.api_client import get_book_data
from utils.scraper import scrape_book_quote

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "📚 Добро пожаловать в Library Bot!\n\n"
        "Доступные функции:\n"
        "1️⃣ /book <название> — Информация о книге (HTTP API)\n"
        "2️⃣ /cover <название> — Обложка книги (HTTP API)\n"
        "3️⃣ /quote — Книжная цитата дня (HTML Скрапинг)\n"
        "4️⃣ /history — История ваших запросов (Локальные файлы)"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['book'])
def action_book(message):
    query = message.text.replace('/book', '').strip()
    if not query:
        bot.reply_to(message, "Использование: /book Название")
        return
    data = get_book_data(query)
    if data.get("found"):
        response_text = f"📖 Книга: {data['title']}\n✍️ Автор: {data['author']}\n📅 Год: {data['year']}"
        status_msg = "Success"
    else:
        response_text = f"Книга '{query}' не найдена."
        status_msg = "Not Found"
    bot.reply_to(message, response_text)
    log_user_action(message.from_user.id, message.text, "API Book Search", status_msg)

@bot.message_handler(commands=['cover'])
def action_cover(message):
    query = message.text.replace('/cover', '').strip()
    if not query:
        bot.reply_to(message, "Использование: /cover Название")
        return
    data = get_book_data(query)
    if data.get("found") and data.get("cover_id"):
        cover_url = f"https://covers.openlibrary.org/b/id/{data['cover_id']}-L.jpg"
        bot.send_photo(message.chat.id, cover_url, caption=f"Обложка книги: {data['title']}")
        status_msg = "Cover sent"
    else:
        bot.reply_to(message, "Обложка не найдена.")
        status_msg = "Cover missing"
    log_user_action(message.from_user.id, message.text, "API Cover Search", status_msg)

@bot.message_handler(commands=['quote'])
def action_quote(message):
    res = scrape_book_quote()
    if res["status"]:
        response_text = f"💬 \"{res['text']}\"\n— {res['author']}"
        status_msg = "Quote sent"
    else:
        response_text = "Не удалось загрузить цитату."
        status_msg = "Scraping failed"
    bot.reply_to(message, response_text)
    log_user_action(message.from_user.id, message.text, "HTML Scraping Quote", status_msg)

@bot.message_handler(commands=['history'])
def action_history(message):
    filename = f"logs/{message.from_user.id}.log"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read().split('-'*40)
            last_records = "".join(content[-4:]).strip()
            response_text = f"📋 Последние логи взаимодействия:\n\n{last_records}"
    else:
        response_text = "История пуста."
    bot.reply_to(message, response_text)
    log_user_action(message.from_user.id, message.text, "Read Local Logs File", "History displayed")

if __name__ == '__main__':
    bot.polling(none_stop=True)