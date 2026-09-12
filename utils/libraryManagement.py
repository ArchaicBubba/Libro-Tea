from . import settings
import sqlite3
from pathlib import Path

# Creates Library to store audiobook information in. Only stores ISBN, Title, and download status
def create_library() -> None:
    settings.debug_mes(1, "Running", f"Intializing Database")

    Path(settings.config["database_dir"]).mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(f"{settings.config["database_dir"]}/{settings.config["database_file"]}") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS library (
                ISBN INTEGER PRIMARY KEY, 
                Title TEXT NOT NULL, 
                Downloaded BOOLEAN)
            ''')
        conn.commit()
    
    return

# Adds book to database
def add_book(ISBN: int, Title: str) -> bool:
    settings.debug_mes(1, "Running", f"ISBN:{ISBN} - Adding Book {Title} to library.")
    
    if check_book_exists(ISBN):
        return False
    
    with sqlite3.connect(f"{settings.config["database_dir"]}/{settings.config["database_file"]}") as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO library (ISBN, Title, Downloaded)
            VALUES (?, ?, False)
            ''', (ISBN, Title))
        conn.commit()

    settings.debug_mes(1, "Running", f"ISBN:{ISBN} - Book {Title} added to library.")
    return True

# Checks if a book is already in the database
def check_book_exists(ISBN: int) -> bool:
    settings.debug_mes(1, "Running", f"ISBN:{ISBN} - Checking if book exists in library")
    
    with sqlite3.connect(f"{settings.config["database_dir"]}/{settings.config["database_file"]}") as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT ISBN
            FROM library 
            WHERE ISBN={ISBN}
            ''')
        book = cursor.fetchone()

    if book:
        settings.debug_mes(2, "Running", f"ISBN:{ISBN} - Found in library.")
        return True

    settings.debug_mes(2, "Running", f"ISBN:{ISBN} - Not found in library.")
    return False

# gets list of books that have not been downloaded
def get_not_downloaded_books() -> list:
    settings.debug_mes(1, "Running", f"Getting books that have not been downloaded.")

    with sqlite3.connect(f"{settings.config["database_dir"]}/{settings.config["database_file"]}") as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT ISBN, Title, Downloaded
            FROM library 
            WHERE Downloaded=False
            ''')
        books = cursor.fetchall()
        library = []
        for book in books:
            library.append(book[0])
        
        settings.debug_mes(0, 'Running', f'{len(library)} waiting to be downloaded.' )
    return library

# Checks if a book has been downloaded
def is_book_downloaded(ISBN: int) -> bool:
    settings.debug_mes(1, "Running", f"ISBN:{ISBN} - Checking if the book has been downloaded previously.")

    with sqlite3.connect(f"{settings.config["database_dir"]}/{settings.config["database_file"]}") as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT Downloaded
            FROM library 
            WHERE ISBN={ISBN}
            ''')
        book = cursor.fetchone()

    if book[0]==0:
        settings.debug_mes(2, "Running", f"ISBN:{ISBN} - Book Hasn't been downloaded yet.")
        return False

    if book[0]==1:
        settings.debug_mes(2, "Running", f"ISBN:{ISBN} - Book has been downloaded.")
        return True

    return False

# Sets the current books download status to downloaded
def set_book_downloaded(ISBN: int) -> None:
    settings.debug_mes(2, "Running", f"ISBN:{ISBN} - Marking book as being downloaded.")

    with sqlite3.connect(f"{settings.config["database_dir"]}/{settings.config["database_file"]}") as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE library
            SET Downloaded=True
            WHERE ISBN={ISBN}
            ''')
        conn.commit()
        
    return
