import logging
from library_inventory.inventory import LibraryInventory
logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
def print_menu():
    print("\n===== Library Inventory Menu =====")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")
def add_book_flow(inventory):
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    isbn = input("Enter ISBN: ").strip()
    if not title or not author or not isbn:
        print("All fields are required.")
        return
    ok = inventory.add_book(title, author, isbn)
    if ok:
        print("Book added successfully.")
    else:
        print("Could not add book. Maybe ISBN already exists?")
def issue_book_flow(inventory):
    isbn = input("Enter ISBN to issue: ").strip()
    if not isbn:
        print("ISBN cannot be empty.")
        return
    inventory.issue_book(isbn)
def return_book_flow(inventory):
    isbn = input("Enter ISBN to return: ").strip()
    if not isbn:
        print("ISBN cannot be empty.")
        return
    inventory.return_book(isbn)
def search_book_flow(inventory):
    print("1. Search by Title")
    print("2. Search by ISBN")
    choice = input("Enter your choice: ").strip()
    if choice == "1":
        title = input("Enter part of title: ").strip()
        result = inventory.search_by_title(title)
        if not result:
            print("No books found with that title.")
        else:
            print("Search results:")
            for b in result:
                print(b)
    elif choice == "2":
        isbn = input("Enter ISBN: ").strip()
        book = inventory.search_by_isbn(isbn)
        if book is None:
            print("No book found with that ISBN.")
        else:
            print("Book found:")
            print(book)
    else:
        print("Invalid choice.")
def main():
    inventory = LibraryInventory()
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_book_flow(inventory)
        elif choice == "2":
            issue_book_flow(inventory)
        elif choice == "3":
            return_book_flow(inventory)
        elif choice == "4":
            inventory.display_all()
        elif choice == "5":
            search_book_flow(inventory)
        elif choice == "6":
            print("Exiting program. Goodbye.")
            break
        else:
            print("Invalid option. Please try again.")
if __name__ == "__main__":
    main()
