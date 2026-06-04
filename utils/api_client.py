import requests

def get_book_data(title: str) -> dict:
    url = f"https://openlibrary.org/search.json?title={title}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("docs"):
                book = data["docs"][0]
                return {
                    "found": True,
                    "title": book.get("title"),
                    "author": book.get("author_name", ["Неизвестно"])[0],
                    "year": book.get("first_publish_year", "N/A"),
                    "cover_id": book.get("cover_i")
                }
            return {"found": False, "error": "Book not found"}
        return {"found": False, "error": f"API error: {response.status_code}"}
    except Exception as e:
        return {"found": False, "error": str(e)}