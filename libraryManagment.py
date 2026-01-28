import settings, sqlite3

# Creates Library to store audiobook information in. Only stores ISBN, Title, and download status
def create_library():
    conn = sqlite3.connect("library.db")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS library (
            ISBN INTEGER PRIMARY KEY, 
            Title TEXT NOT NULL, 
            Downloaded BOOLEAN)
        ''')
    conn.commit()
    if settings.config["debug"]>=1:
        print("DEBUG 1 - RUNNING - Database Found")
    return

# Adds book to database
def add_book(ISBN, Title):
    if settings.config["debug"]>=1:
        print(f"DEBUG 1 - RUNNING - ISBN:{ISBN} - Adding Book {Title} to library.")
    if check_book_exists(ISBN):
        if settings.config["debug"]>=1:
            print(f"DEBUG 1 - RUNNING - ISBN:{ISBN} - Book already exists in library.")
        return
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute(f'''
        INSERT INTO library (ISBN, Title, Downloaded)
        VALUES (?, ?, False)
        ''', 
        (ISBN, Title)
    )
    conn.commit()
    conn.close()
    if settings.config["debug"]>=1:
        print(f"DEBUG 1 - RUNNING - ISBN:{ISBN} - Book {Title} added to library.")
    return

# Checks if a book is already in the database
def check_book_exists(ISBN) -> bool:
    if settings.config["debug"]==2:
        print(f"DEBUG 2 - RUNNING - ISBN:{ISBN} - Checking if book exists in library")
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT ISBN
        FROM library 
        WHERE ISBN={ISBN}
        '''
    )
    book = cursor.fetchone()
    conn.close()
    if book:
        if settings.config["debug"]>=1:
            print(f"DEBUG 1 - RUNNING - ISBN:{ISBN} - found in library.")
        return True
    if settings.config["debug"]>=1:
        print(f"DEBUG 1 - RUNNING - ISBN:{ISBN} - not found in library.")
    return False

# Checks if a book has been downloaded
def is_book_downloaded(ISBN):
    if settings.config["debug"]>=1:
        print(f"DEBUG 1 - RUNNING - ISBN:{ISBN} - Checking if book downloaded.")
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT Downloaded
        FROM library 
        WHERE ISBN={ISBN}
        '''
    )
    book = cursor.fetchone()
    conn.close()
    if book[0]==0:
        if settings.config["debug"]>=2:
            print(f"DEBUG 2 - RUNNING - ISBN:{ISBN} - Book Hasn't been downloaded.")
        return False
    if book[0]==1:
        if settings.config["debug"]>=2:
            print(f"DEBUG 2 - RUNNING - ISBN:{ISBN} - Book has been downloaded.")
        return True
    return book

# Sets the current books download status to downloaded
def set_book_downloaded(ISBN):
    if settings.config["debug"]==2:
        print(f"DEBUG 2 - RUNNING - ISBN:{ISBN} - Setting download status")
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute(f'''
        UPDATE library
        SET Downloaded=True
        WHERE ISBN={ISBN}
        '''
    )
    conn.commit()
    conn.close()
    return
