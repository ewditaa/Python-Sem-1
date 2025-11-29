import json
import logging
from pathlib import Path


# Logging Setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)



# Task 1 — Book Class

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status if status in ("available", "issued") else "available"

    def __str__(self):
        return f"{self.title} — {self.author} (ISBN: {self.isbn}) [{self.status}]"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        """Marks the book as issued."""
        if self.status == "issued":
            return False
        self.status = "issued"
        return True

    def return_book(self):
        """Marks the book as available."""
        if self.status == "available":
            return False
        self.status = "available"
        return True

    def is_available(self):
        return self.status == "available"



# Task 2 — LibraryInventory

class LibraryInventory:
    def __init__(self, storage_path):
        self.storage_path = Path(storage_path)
        self.books = []
        self.load()

    # Load catalog from JSON

    def load(self):
        try:
            if not self.storage_path.exists():
                logger.info("Catalog file not found — starting new inventory.")
                self.books = []
                return

            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            self.books = [Book(**item) for item in data]
            logger.info("Catalog loaded.")
        except json.JSONDecodeError:
            logger.error("Corrupted JSON file — starting with empty inventory.")
            self.books = []
        except Exception as e:
            logger.error(f"Unexpected error loading inventory: {e}")
            self.books = []

    # Save catalog to JSON

    def save(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            data = [b.to_dict() for b in self.books]
            self.storage_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            logger.info("Catalog saved.")
        except Exception as e:
            logger.error(f"Failed to save catalog: {e}")
            raise

    # Operations

    def add_book(self, book):
        if self.search_by_isbn(book.isbn):
            raise ValueError("Book with this ISBN already exists.")
        self.books.append(book)
        logger.info(f"Added book: {book}")

    def search_by_title(self, title_query):
        query = title_query.lower().strip()
        return [b for b in self.books if query in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return [str(b) for b in self.books]



# Task 4 — CLI interface

def prompt_nonempty(message):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Value cannot be empty.")


def run_cli():
    inventory = LibraryInventory("catalog.json")

    while True:
        print("\nLibrary Inventory Manager")
        print("-------------------------")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search by Title")
        print("6. Search by ISBN")
        print("7. Exit")

        choice = input("Enter choice (1-7): ").strip()

        try:
            if choice == "1":
                title = prompt_nonempty("Title: ")
                author = prompt_nonempty("Author: ")
                isbn = prompt_nonempty("ISBN: ")

                book = Book(title, author, isbn)
                inventory.add_book(book)
                inventory.save()

                print("Book added successfully.")

            elif choice == "2":
                isbn = prompt_nonempty("ISBN to issue: ")
                book = inventory.search_by_isbn(isbn)

                if not book:
                    print("Book not found.")
                else:
                    if book.issue():
                        print("Book issued.")
                        inventory.save()
                    else:
                        print("Book is already issued.")

            elif choice == "3":
                isbn = prompt_nonempty("ISBN to return: ")
                book = inventory.search_by_isbn(isbn)

                if not book:
                    print("Book not found.")
                else:
                    if book.return_book():
                        print("Book returned.")
                        inventory.save()
                    else:
                        print("Book was already available.")

            elif choice == "4":
                books = inventory.display_all()
                if not books:
                    print("No books in catalog.")
                else:
                    print("\nCatalog:")
                    for b in books:
                        print(" -", b)

            elif choice == "5":
                title_query = prompt_nonempty("Enter title: ")
                matches = inventory.search_by_title(title_query)
                if matches:
                    for b in matches:
                        print(b)
                else:
                    print("No matches found.")

            elif choice == "6":
                isbn = prompt_nonempty("Enter ISBN: ")
                book = inventory.search_by_isbn(isbn)
                print(book if book else "Book not found.")

            elif choice == "7":
                print("Exiting...")
                inventory.save()
                break

            else:
                print("Invalid choice. Enter a number 1–7.")

        except Exception as e:
            logger.error(f"Error during operation: {e}")
            print("An error occurred. Check logs for details.")



# Run program

if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\nInterrupted — saving and exiting.")
