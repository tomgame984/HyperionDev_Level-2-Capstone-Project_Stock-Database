import sqlite3
db = sqlite3.connect('data/bookstore')
cursor = db.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS book
               (id INTEGER PRIMARY KEY, 
               title VARCHAR(100), 
               author VARCHAR(100), 
               qty INTEGER)
               ''')
db.commit()

# Book Data List
book_lst = [(3001,"A Tale of Two Cities","Charles Dickens",30),
            (3002,"Harry Potter and the Philosopher's Stone","J.K. Rowling",40),
            (3003,"The Lion, the Witch and the Wardrobe","C. S. Lewis",25),
            (3004,"The Lord of the Rings","J.R.R Tolkien",37),
            (3005,"Alice in Wonderland","Lewis Carroll",12)]

# Insert 'book_lst' into 'book' TABLE
cursor.executemany('''INSERT INTO book(id, title, author, qty)
                   VALUES(?,?,?,?)
                   ON CONFLICT (id) DO NOTHING''', book_lst)
db.commit()

# CLASSES
class Book:
    """
    Class for book details.
    id is self generated and incremental to last record in table.
    """
    def __init__(self):
        self.title = input('Enter book title:  ')
        self.author = input('Enter author:  ')
        while True:
            try:
                self.qty = int(input('Enter quantity:  '))
                break
            except ValueError:
                print('Invalid entry.  Please re-enter a number.')

    def __str__(self):
        return f'{self.title}, {self.author}, {self.qty}'

    def displayBook(self):
        print(f'''\nBook details entered:
Title:    {self.title}
Author:   {self.author}
Quantity: {self.qty}
''')

# VARIABLES
add_more = 'N'

# FUNCTIONS | GENERAL
def menu_return():
    """
    User input required to confrim that they are ready to return to menu
    option page.

    Returns:
        input: "Y" - confirmation to return to option menu.
    """
    ready = input('''\nPress "Y" to return to the option menu:  ''').upper()
    while ready not in ['Y']:
        print('''\n** Invalid entry **
Please enter "Y" to return to the  menu.''')
        ready = input('''\nReady to return to the option menu?
(Press "Y" to continue):  ''').upper()
    else:
        return

# FUNCTIONS | SEARCH
def print_table_all():
    """
    Printout of all table records terminal friendly format
    """
    cursor.execute('''SELECT * FROM book''')
    data = cursor.fetchall()
    data_list = [list(ele) for i,ele in enumerate(data)]
    for book_info in data_list:
        print(f'''
id: {book_info[0]} | Title: {book_info[1]} | Author: {book_info[2]} | QTY: {book_info[3]}
''')

# Solution to convert list of tuples into list found at:
# https://www.geeksforgeeks.org/python-convert-list-of-tuples-into-list/
def convert_to_list(tuple_list, result=None):
    """Converts list of tuple into list.

    Args:
        tuple_list (str and int): Includes id, title, author and qty.
        result (extend, optional): Checks tuple length. Defaults to None.

    Returns:
        list: list of record details.
    """
    if result is None:
        result = []
    if len(tuple_list) == 0:
        return result
    else:
        result.extend(tuple_list[0])
        return convert_to_list(tuple_list[1:], result)

def id_search():
    """
    user input - specific id.  
    Will check for ValueError 
    Will check if id exists in book table.
    If id exists - prints specific record for book table based on id.
    """
    while True:
        try:
            id = int(input(f'\nEnter book id:  '))
            break
        except ValueError:
            print('Invalid entry.  Please re-enter a number.')
            
    cursor.execute('''SELECT * FROM book
                    WHERE id = ?''', (id,))

    data = cursor.fetchall()
    
    while not data:
        print(f'\n** No record found, please retry **\n')
        while True:
            try:
                id = int(input(f'\nEnter book id:  '))
                break
            except ValueError:
                print('Invalid entry.  Please re-enter a number.')
        
        cursor.execute('''SELECT * FROM book
                        WHERE id = ?''', (id,))
        data = cursor.fetchall()

    data_list = convert_to_list(data)
    print(f'''\nSelected book details:
id:     {data_list[0]}
Title:  {data_list[1]}
Author: {data_list[2]}
qty:    {data_list[3]}
''')

    return(data_list)
    
def title_search():
    """
    user input - specific title.  
    Will check if title exists in book table.
    If title exists - prints all records from book table with matching title.
    """
    title = input(f'\nEnter book title:  ')
           
    cursor.execute('''SELECT * FROM book
                    WHERE title = ?''', (title,))

    data = cursor.fetchall()
    
    while not data:
        print(f'\nNo record found for {title}.\n')
        retry = input('Would you like to enter a different title (Y/N)?  ').upper()
        while retry not in ['Y', 'N']:
            print('\nInvalid entry. Please retry...\n')
            retry = input('Enter a different title (Y/N)?  ')
        
        if retry == 'Y':
            title = input(f'\nEnter book title:  ')
            cursor.execute('''SELECT * FROM book
                    WHERE title = ?''', (title,))
            data = cursor.fetchall()
        
        else:
            break

    # Solution for converting list of tuples to nested lists found at:
    # https://www.geeksforgeeks.org/python-convert-list-of-tuples-to-list-of-list/
    data_list = [list(ele) for i,ele in enumerate(data)]

    # Loop to printout all rcords with specific title.
    for book_info in data_list: 
        print(f'''\nSelected book details:
id:     {book_info[0]}
Title:  {book_info[1]}
Author: {book_info[2]}
qty:    {book_info[3]}
''')
    menu_return()
    return(data_list)

def author_search():
    """
    User input - specific author.  
    Will check if author exists in book table.
    If author exists - prints all records from book table with matching author.
    """
    author = input(f'\nEnter author name:  ')
           
    cursor.execute('''SELECT * FROM book
                    WHERE author = ?''', (author,))

    data = cursor.fetchall()
    
    while not data:
        print(f'\nNo record found for {author}.\n')
        retry = input('Would you like to enter a different author (Y/N)?  ').upper()
        while retry not in ['Y', 'N']:
            print('\nInvalid entry. Please retry...\n')
            retry = input('Add a diiferent author (Y/N)?  ')
        
        if retry == 'Y':
            author = input(f'\nEnter author name:  ')
            cursor.execute('''SELECT * FROM book
                    WHERE author = ?''', (author,))
            data = cursor.fetchall()

        else:
            break
        
    # converting list of tuples to nested lists 
    data_list = [list(ele) for i,ele in enumerate(data)]

    for book_info in data_list: #
        print(f'''\nSelected book details:
id:     {book_info[0]}
Title:  {book_info[1]}
Author: {book_info[2]}
qty:    {book_info[3]}
''')
    menu_return()
    return(data_list)

def search_options():
    """
    Search options menu.
    Allows user to print all table records as well as search for specific
    records by id, title or author.
    """
    while True:
        try:
            search_menu = int(input('''
--------------------------
Book Search | Option Menu
--------------------------

Select from the following:
1.  View All
2.  Select Search Criteria
0.  Exit
                                                                                
Enter Option Number:  '''))
            if search_menu == 1:
                print_table_all()
    
            elif search_menu == 2:
                search_crit()
            
            elif search_menu == 0:
                break

            else:
                print(f'\n** Invalid Entry. Please try again... **\n')
        
        except ValueError:
            print('Invalid entry.  Please re-enter a number.')

def search_crit():
    """
    Search criteria - allows user to specify search criteria for id, title 
    or author.
    
    """
    while True:
        try:
            criteria = int(input('''
----------------------
Book Search | Criteria
----------------------

Select search criteria:
1.  id
2.  Title
3.  Author
0.  Return to main menu
                                                    
Enter option number:  '''))
            if criteria == 1:
                id_search()

            elif criteria == 2:
                title_search()

            elif criteria == 3:
                author_search()

            elif criteria == 0:
                break
        
            else:
                print(f'\n** Invalid Entry. Please try again... **\n')
        
        except ValueError:
            print('Invalid entry.  Please re-enter a number.')


# FUNCTIONS | ENTER BOOK
def add_book():
    """
    Allows user to create a new record in book table.
    Call Class book to user input of book detials.
    Table will be checked for duplicate entry.

    """
    proceed = 'N'
    while proceed != 'Y':
        new_book = Book()
        new_book.displayBook()
        cursor.execute('''SELECT * FROM book WHERE title=?''', (new_book.title,))
        data = cursor.fetchall()
        data_list = [list(ele) for i,ele in enumerate(data)]
        if data:
            for book in data_list:
                print(f'''The following book with the same title is already stored:
id:     {book[0]}
Title:  {book[1]}
Author: {book[2]} ''')
        proceed = conf_add_book()
            
        if proceed == 'Y':
            cursor.execute('''INSERT INTO book(title, author, qty)
                  VALUES(?,?,?)''', (new_book.title, new_book.author, new_book.qty))
            db.commit()
            print('''
--------------------
** New Book Added **
--------------------
                  ''')
            return(1)
        else:
            return(0)

def conf_add_book():
    """
    User input to confirm that they wish to add record to book table.
    """
    add_book = input(f'\nWould you like to add this to the book inventory (Y/N)?  ').upper()
    while add_book not in ['Y','N']:
            print('Invalid entry.  Please enter "Y" or "N".')
            add_book = input('Add book (Y/N)?  ').upper()
    return(add_book)

def valid_add_more():
    """
    User input to confirm whether they wish to add more records to the book table.
    """
    add_more = input('Add another book (Y/N)?  ').upper()
    while add_more not in ['Y', 'N']:
        print('Invalid entry.  Please enter "Y" or "N".')
    return(add_more)


# FUCNTIONS | UPDATE BOOK
def conf_update():
    """
    User input to confirm they wish to proceed with amendment.
    """
    update = input(f'\nProceed with amendment(Y/N)?  ').upper()
    while update not in ['Y','N']:
            print('Invalid entry.  Please enter "Y" or "N".')
            update = input('Amend (Y/N)?  ').upper()
    return(update)

def update_title():
    """
    Specific fucntion for the update of book titles on exisitng records.
    """
    amend = input('Amend title (Y/N):  ').upper()
    while amend not in ['Y', 'N']:
        print('\nInvalid entry. Please retry...\n')
        amend = input('Amend title (Y/N):  ').upper()

    if amend == 'Y':
        confirm = 'N'
        while confirm != 'Y':
            print(f'Current title: {update_book[1]}')
            new_title = input('Enter new title:  ')
            confirm = conf_update()

        cursor.execute('''UPDATE book SET title=? WHERE id=?''', (new_title, id_selected))
        db.commit()

        print('''
-----------------------
Title Update Successful
-----------------------
              ''')

    else:
        print('''
------------------------
No changes made to title
------------------------
              ''')

def update_author():
    """
    Specific fucntion for the update of book author on exisitng records.
    """
    amend = input('Amend author (Y/N):  ').upper()
    while amend not in ['Y', 'N']:
        print('\nInvalid entry. Please retry...\n')
        amend = input('Amend author (Y/N):  ').upper()

    if amend == 'Y':
        confirm = 'N'
        while confirm != 'Y':
            print(f'Current author: {update_book[2]}')
            new_author = input('Enter new author:  ')
            confirm = conf_update()

        cursor.execute('''UPDATE book SET author=? WHERE id=?''', (new_author, id_selected))
        db.commit()

        print('''
------------------------
Author Update Successful
------------------------
              ''')
    else:
        print('''
-------------------------
No changes made to Author
-------------------------
              ''')

def update_qty():
    """
    Specific fucntion for the update of book qty on exisitng records.
    """
    amend = input('Amend quantity (Y/N):  ').upper()
    while amend not in ['Y', 'N']:
        print('/nInvalid entry. Please retry.../n')
        amend = input('Amend quantity (Y/N):  ').upper()

    if amend == 'Y':
        confirm = 'N'
        while confirm != 'Y':
            print(f'Current quantity: {update_book[3]}')
            new_qty = int(input('Enter new quantity:  '))
            confirm = conf_update()
        cursor.execute('''UPDATE book SET qty=? WHERE id=?''', (new_qty, id_selected))
        db.commit()

        print('''
--------------------------
Quantity Update Successful
--------------------------
              ''')
    else:
        print('''
---------------------------
No changes made to Quantity
---------------------------
              ''')

def update_review(x_id):
    """
    Provides user with confirmation and summary of amendments.

    Args:
        x_id (int): id selected by user when selecting record to update.
    """
    id = x_id
    cursor.execute('''SELECT * FROM book
                    WHERE id = ?''', (id,))
    
    data = cursor.fetchall()

    data_list = convert_to_list(data)
    
    print(f'''
--------------------
Book Update Complete
--------------------
Book details updated to:
id:     {data_list[0]}
Title:  {data_list[1]}
Author: {data_list[2]}
qty:    {data_list[3]}
''')
    menu_return()


# FUNCTIONS | DELETE BOOK
def del_opt_menu():
    """
    User Input - select option from menu to determine method to identify and
    delete records for book table.
    """
    while True:
        try:
            delete_opt = int(input('''\n 
--------------------------
Delete Book | Menu Options
--------------------------
1.  Delete Book (id required)
2.  Search Database and Delete
3.  Delete All Books
0.  Return to Main Menu
                       
Enter option number:  '''))
            return(delete_opt)
        except ValueError:
            print('Invalid entry.  Please re-enter a number.')

def id_del_book():
    """
    Specific function to identify record with id and delete associated record.
    """
    select_conf = 'N'
    while select_conf != 'Y':
        del_book = id_search()
        id_selected = int(del_book[0])
        select_conf = input('''Is this the correct book for deleting?
"Y" to continue
"N" to re-enter detials
Enter selection:  ''').upper()

    return(id_selected)        

def search_del_book():
    """
    Specific function to identify record with specific criteria (id, title, author) and 
    confirm id of the record for deletion.
    """
    select_conf = 'N'
    while select_conf != 'Y':
        search_options()
        del_book = id_search()
        id_selected = int(del_book[0])
        select_conf = input('''Is this the correct book for deleting?
"Y" to continue
"N" to re-enter detials
Enter selection:  ''').upper()
    return(id_selected)

def delete_book(x):
    """
    Delete specific book based on id entered by user.

    Args:
        x (int): book id base on user input.
    """
    cursor.execute('''DELETE FROM book WHERE id = ?''', (x,))
    db.commit()
    print('''
-------------------------
Book successfully deleted
-------------------------
''')

def delete_all():
    """
    Deletes all records within book table, but the table remains in existence.
    """
    delete_all = input('''
---------------
*** WARNING ***
---------------
You are about to delete all informationfrom the Bookstore Data.
Enter "Y" to continue.
Enter "N' to cancel and return to the main menue.
Are you sure you want to continue (Y/N):  ''').upper()
    while delete_all not in ['Y', 'N']:
        print('Invalid entry.  Please enter "Y" or "N".')
        delete_all = input('Are you sure you want to delete ALL records:  ').upper()

    if delete_all == 'Y':
        cursor.execute('''DELETE FROM book''')
        db.commit()
        print('''
--------------------------------
All records successfully deleted
--------------------------------
                      ''')
    else:
        menu_return()


# PROGRAM | MAIN MENU
while True:
    menu = int(input('''
------------------------------
Bookstore Database | Main Menu
------------------------------
Select menu option:
1.  Enter Book
2.  Update Book
3.  Delete Book
4.  Search Books
0.  Exit
                     
Enter Option Number:  '''))
    
    if menu == 1:
        print('''
----------------------
Enter New Book Details
----------------------
              ''')
        count = add_book()
        add_more = valid_add_more()

        while add_more != 'N': # Loop to allow user to add multiple books.
                add_book()
                count += 1
                add_more = valid_add_more()

        print(f'''\n ** Upload Complete **
Number of books added:  {count}
''')
        continue
            
    elif menu == 2:
        update_opt = int(input('''\n 
--------------------------
Update Book | Menu Options
--------------------------
1.  Update Book (id required)
2.  Search Database and Update
3.  Return to main menu
                       
Enter option number:  '''))
        if update_opt == 1:
            select_conf = 'N'
            while select_conf != 'Y':
                update_book = id_search()
                id_selected = (update_book[0])

                #User input to allow review and apporval
                select_conf = input('''Is this the correct book for updating?
"Y" to continue
"N" to re-enter detials
Enter selection:  ''').upper()
            # Functions called to allow user to update each record field.
            update_title()
            update_author()
            update_qty()
            update_review(id_selected)
        
        elif update_opt == 2:
            select_conf = 'N'
            while select_conf != 'Y':
                #Using the search function to allow users to find ID number.
                search_options()
                update_book = id_search()
                id_selected = int(update_book[0])
                select_conf = input('''Is this the correct book for updating?
"Y" to continue
"N" to re-enter detials
Enter selection:  ''').upper()
            
            # Functions called to allow user to update each record field.
            update_title()
            update_author()
            update_qty()
            update_review(id_selected)
            
        elif update_opt == 3:
            menu_return()

        else:
            print('\nInvalid entry.  Please retry...\n')

    elif menu == 3:
        delete_opt = del_opt_menu()
        
        if delete_opt == 1:
            delete_book(id_del_book())
                
        elif delete_opt == 2:
            delete_book(search_del_book())

        elif delete_opt == 3:
            delete_all()

        elif delete_opt == 0:
            menu_return()

        else:
            print('\nInvalid entry.  Please retry...\n')

    elif menu == 4:
        search_options()

    elif menu == 0:
        #CLOSE 'bookstore' DB
        db.commit()
        db.close()
        print(f'''
-----------------------------
Connection to database closed
-----------------------------
              ''')
        exit()

    else:
        print(f'\nInvalid Entry. Please try again...')
