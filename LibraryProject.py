from datetime import datetime
import os

class User:
    new_id = 1
    def __init__(self, username, password):
        self.user_id = User.new_id
        self.username = username
        self.password = password
        self.role = "user"  # 'user' or 'admin'

        User.new_id += 1

    def __str__(self):
        return f"User ID: {self.user_id}, Username: {self.username}, Role: {self.role}"

    def get_user_id(self):
        return self.user_id

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_role(self):
        return self.role


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role = "admin"

class Book:
    next_book_id = 1
    def __init__(self, book_id, title, author, quantity):
        self.book_id = Book.next_book_id
        self.title = title
        self.author = author
        self.quantity = quantity
        # Increment the next_book_id for the next book
        Book.next_book_id += 1

class Transaction:
    new_transaction_id = 1
    def __init__(self, user, book, issue_date, return_date=None):
        self.transaction_id = Transaction.new_transaction_id
        self.user = user
        self.book = book
        self.issue_date = issue_date
        self.return_date = return_date
        Transaction.new_transaction_id += 1
    
    def return_book(self, return_date):
        self.return_date = return_date
        self.book.quantity += 1
        print(f"User '{self.user.username}' returned '{self.book.title}' book.")
        
class Library:
    def __init__(self):
        # ... (previous code remains the same)
        self.books = []
        self.users = []  # Array to store user objects
        self.admins = []  # Array to store admin objects
        self.borrowed_books = []  # Store borrowed book records (user_id, book_id)
        self.returned_books = []  # Store returned book records (user_id, book_id)
        self.transactions = []
    
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.show_library_name()

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    
    def get_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def show_library_name(self):
        print("\n\n--------------------------------------------")
        print("Welcome to the Library Management System!")
        print("--------------------------------------------")

    def get_transaction_by_user_id_and_book_id(self, user_id, book_id):
        user = self.get_user_by_id(user_id)
        book = self.get_book_by_id(book_id)

        if user and book:
            transaction = []
            for transaction in self.transactions:
                if transaction.user == user and transaction.book == book:
                    return transaction
            return transaction
        else:
            return None
        
    def show_all_transactions(self):
        self.clear_terminal()
        if self.transactions: 
            print("\n\nAll Transactions:")
            print("-------------------------------------------")
            for transaction in self.transactions:
                print(f"Transaction ID: {transaction.transaction_id}")
                print(f"User ID: {transaction.user.user_id}, Book ID: {transaction.book.book_id}")
                print(f"Username: {transaction.user.username}, Title: {transaction.book.title}")
                print(f"Issue Date: {transaction.issue_date}")
                if transaction.return_date:
                    print(f"Return Date: {transaction.return_date}")
                print("----------------------------------------")
        else:
            print(" NO Transactions Till Now.")

    def not_yet_returned_books(self):
        self.clear_terminal()
        not_returned_books = []
        for user_id, book_id in self.borrowed_books:
            transaction = self.get_transaction_by_user_id_and_book_id(user_id, book_id)
            if transaction and (transaction.return_date == None):
                not_returned_books.append((user_id, book_id))

        if not_returned_books:
            print("\n\nNot Yet Returned Books:")
            print("--------------------------------")
            for user_id, book_id in not_returned_books:
                user = self.get_user_by_id(user_id)
                book = self.get_book_by_id(book_id)
                print(f"User ID: {user.user_id}, Username: {user.username}")
                print(f"Book ID: {book.book_id}, Title: {book.title}")
                print("--------------------------------")
        else:
            print("All Books are returned.")

    def take_book_details_from_admin(self):
        self.clear_terminal()
        print("------------------------------")
        title = input("Enter book title: ")
        author = input("Enter author name: ")
        quantity = int(input("Enter book quantity: "))
        print("------------------------------")
        return title, author, quantity

    def add_book(self):
        self.clear_terminal()
        title, author, quantity = self.take_book_details_from_admin()
        book = Book(self, title, author, quantity)
        self.books.append(book)
        print(f"'{title}' Book added successfully with quantity {quantity}.")

    def display_books(self):
        for book in self.books:
            print(f"Title: {book.title}, Author: {book.author}")


    def remove_book(self, book_id):
        self.clear_terminal()
        book = next((b for b in self.books if b.book_id == book_id), None)
        if book:
            self.books.remove(book)
            print(f"Book '{book.title}' removed from the library.")
        else:
            print("Invalid book ID.")

    def borrow_book(self, user_id, book_id):
        self.clear_terminal()
        user = None
        for u in self.users:
            if u.user_id == user_id:
                user = u
                break

        book = None
        for b in self.books:
            if b.book_id == book_id and b.quantity > 0:
                book = b
                break
        

        if user and book:
            issue_date = datetime.now().strftime("%d-%m-%Y")  # Get current date in "year-month-day" format
            transaction = Transaction(user, book, issue_date)
            self.transactions.append(transaction)
            book.quantity -= 1
            self.borrowed_books.append((user.user_id, book.book_id))
            print(f"User '{user.username}' borrowed '{book.title}' book.")
        else:
            print("Invalid user ID or book ID. Or the book is out of stock.")

    def return_book(self, user_id, book_id):
        self.clear_terminal()
        user_book_pair = (user_id, book_id)
        if user_book_pair in self.borrowed_books:
            returned_transaction = None
            for t in self.transactions:
                if t.user.user_id == user_id and t.book.book_id == book_id:
                    returned_transaction = t
                    break

            if returned_transaction:
                return_date = datetime.now().strftime("%d-%m-%Y")  # Get current date in "year-month-day" format
                returned_transaction.return_book(return_date)
                self.returned_books.append(user_book_pair)
                self.borrowed_books.remove(user_book_pair)
                print(f"User '{returned_transaction.user.username}' returned '{returned_transaction.book.title}' book.")
            else:
                print("Invalid transaction record.")
        else:
            print("No record found for the given user ID and book ID.")

    def view_borrowed_books(self, user_id=None):
        self.clear_terminal()
        if user_id:
            borrowed_books = []
            for u_id, b_id in self.borrowed_books:
                if u_id == user_id:
                    borrowed_books.append((u_id, b_id))
        else:
            borrowed_books = self.borrowed_books
        if borrowed_books:
            print("\n\nBorrowed Books:")
            print("----------------------------------------")
            for user_id, book_id in borrowed_books:
                book = self.get_book_by_id(book_id)
                t = self.get_transaction_by_user_id_and_book_id(user_id,book_id)
                print(f"User ID: {user_id}, Book ID: {book_id}, Issue Date: {t.issue_date}")
                print(f"Book Title: {book.title}, author: {book.author}")
                print("----------------------------------------")
        else:
            print("No borrowed Books.")

    def view_returned_books(self, user_id=None):
        self.clear_terminal()
        if user_id:
            returned_books = []
            for u_id, b_id in self.returned_books:
                if u_id == user_id:
                    returned_books.append((u_id, b_id))
        else:
            returned_books = self.returned_books

        if returned_books:
            print("\n\nReturned Books:")
            print("----------------------------------------")
            for user_id, book_id in returned_books:
                book = self.get_book_by_id(book_id)
                t = self.get_transaction_by_user_id_and_book_id(user_id,book_id)
                print(f"User ID: {user_id}, Book ID: {book_id}, Return Date: {t.return_date}")
                print(f"Book Title: {book.title}, author: {book.author}")
                print("----------------------------------------")
        else:
            print("No Returned Books.")

    def show_admin_menu(self, admin):
        self.clear_terminal()
        while True:
            print("---------------------------------")
            print("\nWelcome",admin.username)
            print("\n -- Admin Menu --")
            print("1. View Available Books")
            print("2. Add Book")
            print("3. Remove Book")
            print("4. View Borrowed Books")
            print("5. View Returned Books")
            print("6. View All Transactions")
            print("7. View Not yet Returned Books")
            print("8. Logout")
            print("---------------------------------")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_available_books()
            elif choice == "2":
                self.add_book()
            elif choice == "3":
                self.view_available_books()
                book_id = int(input("Enter book ID to remove: "))
                self.remove_book(book_id)
            elif choice == "4":
                self.view_borrowed_books()
            elif choice == "5":
                self.view_returned_books()
            elif choice == "6":
                self.show_all_transactions()
            elif choice == "7":
                self.not_yet_returned_books()
            elif choice == "8":
                print("Logging out...")
                break 
            else:
                print("Invalid choice. Please try again.")
        self.show_login_menu()

    def show_user_menu(self, user):
        self.clear_terminal()
        while True:
            print("\n\n---------------------------------")
            print("Hello",user.username)
            print("\n -- User Menu --")
            print("1. View Available Books")
            print("2. Borrow Book")
            print("3. Return Book")
            print("4. My borrowed Books")
            print("5. My Returned Books")
            print("6. Logout")
            print("---------------------------------")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_available_books()
            elif choice == "2":
                self.view_available_books()
                book_id = int(input("Enter book ID to borrow book: "))
                self.borrow_book(user.user_id,book_id)
            elif choice == "3":
                self.clear_terminal()
                self.view_borrowed_books(user.user_id)
                book_id = int(input("Enter book ID to return book: "))
                self.return_book(user.user_id,book_id)
            elif choice == "4":
                self.view_borrowed_books(user.user_id)
            elif choice == "5":
                self.view_returned_books(user.user_id)
            elif choice == "6":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")
        self.show_login_menu()

   
    def view_available_books(self):
        self.clear_terminal()
        available_books = [book for book in self.books if book.quantity > 0]
        if available_books:
            print("\n\nAvailable Books:")
            print("------------------------------")
            for book in available_books:
                print(f"Book ID: {book.book_id}")
                print(f"Title: {book.title}")
                print(f"Author: {book.author}")
                print(f"Available books : {book.quantity}")
                print("------------------------------")
        else:
            print("Books not available in the library.")

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                user.role = "user"
                return user
        for admin in self.admins:
            if admin.username == username and admin.password == password:
                admin.role = "admin"
                return admin
        return None

    def show_login_menu(self):
        self.clear_terminal()
        print("\n1. Login")
        print("2. Create Account")
        print("3. Exit")
        print("--------------------------------------------")

        choice = input("Enter your choice: ")
        if choice == "1":
            count = 3
            while(count):
                self.clear_terminal()
    
                print("------------------------------")
                username = input("Enter username: ")
                password = input("Enter password: ")
                print("------------------------------")
                user = self.login(username, password)
                if user:
                    if user.role == "user":
                        self.show_user_menu(user)
                    elif user.role == "admin":
                        self.show_admin_menu(user)
                    else:
                        print("Invalid user role.")
                else:
                    print("Invalid username or password. Please try again.")
                    count = count - 1
            self.show_login_menu()
        elif choice == "2":
            self.create_account()  # Call the create_account method
        elif choice == "3":
            print("Exiting the system. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")
            self.show_login_menu()

    def create_account(self):
        self.clear_terminal()
        print("\n\nCreating a new account.")
        print("----------------------------")
        print("Select Account Type:")
        print("1. User")
        print("2. Admin")
        print("---------------------------------")
        choice = input("Enter your choice: ")

        if choice == "1":
            self.clear_terminal()
            print("------------------------------")
            username = input("Enter username: ")
            password = input("Enter password: ")
            print("------------------------------")
            user = User(username, password)  # Assuming User class exists
            self.users.append(user)
            print("User account created successfully.")
        elif choice == "2":
            self.clear_terminal()

            print("------------------------------")
            admin_name = input("Enter admin username: ")
            admin_password = input("Enter admin password: ")
            print("------------------------------")
            admin = Admin(admin_name, admin_password)  # Assuming Admin class exists
            self.admins.append(admin)
            print("Admin account created successfully.")
        else:
            print("Invalid choice. Please try again.")
            self.create_account()

        self.show_login_menu()  # Redirect to login menu after successful account creation


if __name__ == "__main__":
    library = Library()
    library.show_login_menu()
