"""
调用各种新闻 API，获取新闻数据。
"""
import os
import json
import random
import traceback

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
books_path = os.path.join(CUR_PATH, "../data/books")


class BooksFetcher(object):
    
    all_books = {}
    for book in os.listdir(books_path):
        
        if book.endswith(".jsonl"):
            book_name = f'《{book.split(".")[0]}》'
            all_books[book_name] = []
            
            with open(os.path.join(books_path, book), "r") as f:
                for line in f:
                    line = json.loads(line)
                    all_books[book_name].append(line)

    @staticmethod
    def fetch_book_contents(
        book_name: str = "",
        paragrah_num: int = 1
    ) -> list:
        """随机获取当前一本书中的内容。

        Args:
            num (int, optional): _description_. Defaults to 1.

        Returns:
            list: book list -> {
                "book_name": book_name,
                "paragraphs": ["paragraph1", "paragraph2", ...]
            }
        """
        if not book_name:
            book_name = random.choice(list(BooksFetcher.all_books.keys()))
        
        random_paragraphs = random.sample(
            BooksFetcher.all_books[book_name], 
            paragrah_num
        )
        
        return {
            "book_name": book_name,
            "paragraphs": random_paragraphs
        }
    

if __name__ == '__main__':
    print(
        json.dumps(
            BooksFetcher.fetch_book_contents(paragrah_num=2),
            ensure_ascii=False,
            indent=4
        )
    )