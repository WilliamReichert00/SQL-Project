# NOTES: functional contact book
# INFO TO STORE - *NAME*, EMAIL, PHONE - [name] and [email or phone]
# OPTIONAL INFO: GROUPS[work, affiliations], DOB
import random
# https://www.sqlitetutorial.net/sqlite-python/

import sqlite3
import string

# open DB
conn = sqlite3.connect('Accounts.db')
cursor = conn.cursor()


# generates a random string of characters of length "length"
def generateSalt(length):
    salt = ""
    for i in range(0, length):
        salt += random.choice(string.ascii_letters)
    return salt

# SQL query conditions should match sql language (ex: WHERE [condition]
def query(conditions=""):
    cursor.execute("SELECT * FROM " + conditions)
    return cursor.fetchall()

# Add column to users, auto salts password for security
# Currently no usable hash function, add one later and also to login line
def add_User(username, password):
    salt = generateSalt(random.randint(1, 10))
    data = (username,(password+salt),salt)
    insert_statement = '''INSERT INTO Users VALUES (?,?,?)'''
    cursor.execute(insert_statement, data)
    conn.commit()

# Remove column
def delete_contact(bad):
    try:
        cursor.execute("DELETE FROM Users WHERE Name == " + bad)
        conn.commit()
        return True
    except sqlite3.OperationalError:
        return False

while True:
    print("Login - 1, Create Account - 2, View Accounts - 3, EXIT - any other key")
    answer = input().upper()
    # login procedure
    if answer == "1":
        print("Enter Username:")
        username = input()
        print("Enter Password:")
        password = input()
        conditions = "Users WHERE Username == '" + username + "'"
        try:
            result = query(conditions)[0]
            print(result)
            # checks hash of password with salt and compares it to stored hash
            if (password + result[2]) == result[1]:
                print("Login successful")
            else:
                print("Password Incorrect")
        except IndexError:
            print("No such Username")

    # account creation
    elif answer == "2":
        print("Enter Username:")
        username = input()
        print("Enter Password:")
        password = input()
        print("Verify Password:")
        while input() != password:
            print("Passwords do not match...")
            print("Re-enter Password:")
        #try:
        add_User(username, password)
        #except sqlite3.OperationalError:
            #print("Oops all spaghetti code")
    elif answer == "3":
        results = query("Users")
        for result in results:
            print(result)
    else:
        break

# Close the connection
conn.close()