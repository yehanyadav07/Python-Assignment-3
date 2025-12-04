import json
import logging
from pathlib import Path

from .book import Book

CATALOG_FILE = Path("books_catalog.json")

logger = logging.getLogger(__name__)


class LibraryInventory:
    def __init__(self):
        self.books = []
        self.load_catalog()

    def add_book(self, title, author, isbn):
        # check duplicate isbn
        for b in self.books:
            if b.isbn == isbn:
                logger.warning("Book with same ISBN already exists")
                return False
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        logger.info(f"Book added: {title}")
        self.save_catalog()
        return True

    def search_by_title(self, title):
        result = []
        for b in self.books:
            if title.lower() in b.title.lower():
                result.append(b)
        return result

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        if not self.books:
            print("No books in library yet.")
        else:
            for b in self.books:
                print(b)

    def issue_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if book is None:
            print("Book not found.")
            logger.error("Issue failed. Book not found.")
            return
        if book.issue():
            print("Book issued successfully.")
            logger.info(f"Book issued: {isbn}")
            self.save_catalog()
        else:
            print("Book is already issued.")
            logger.warning(f"Book already issued: {isbn}")

    def return_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if book is None:
            print("Book not found.")
            logger.error("Return failed. Book not found.")
            return
        if book.return_book():
            print("Book returned successfully.")
            logger.info(f"Book returned: {isbn}")
            self.save_catalog()
        else:
            print("Book was not issued.")
            logger.warning(f"Book was not issued: {isbn}")

    def to_list_of_dicts(self):
        return [b.to_dict() for b in self.books]

    def save_catalog(self):
        try:
            data = self.to_list_of_dicts()
            with CATALOG_FILE.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logger.info("Catalog saved to file")
        except Exception as e:
            logger.error(f"Error saving catalog: {e}")

    def load_catalog(self):
        if not CATALOG_FILE.exists():
            logger.info("Catalog file not found. Starting with empty list.")
            self.books = []
            return
        try:
            with CATALOG_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = []
            for item in data:
                book = Book(
                    item.get("title", ""),
                    item.get("author", ""),
                    item.get("isbn", ""),
                    item.get("status", "available"),
                )
                self.books.append(book)
            logger.info("Catalog loaded from file")
        except json.JSONDecodeError:
            logger.error("Catalog file is corrupted. Starting fresh.")
            self.books = []
        except Exception as e:
            logger.error(f"Error loading catalog: {e}")
            self.books = []
