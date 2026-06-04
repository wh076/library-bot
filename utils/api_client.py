import requests

def get_book_info(title):
    url = f"https://openlibrary.org/search.json?q={title}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("docs"):
                book = data["docs"][0]
                
                # Собираем данные, подставляя заглушки, если какого-то поля нет
                return {
                    "title": book.get("title", "Неизвестно"),
                    "author": ", ".join(book.get("author_name", ["Неизвестно"])),
                    "year": book.get("first_publish_year", "Неизвестно"),
                    # Ссылка на книгу на самом сайте Open Library
                    "link": f"https://openlibrary.org{book.get('key', '')}",
                    # ID обложки (может быть None, если обложки нет)
                    "cover_id": book.get("cover_i")
                }
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
    return None