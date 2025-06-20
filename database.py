# NOTES: Accounts with Login + Edit
# INFO TO STORE - Username, *hashed password + salt*, salt
import random
# https://www.sqlitetutorial.net/sqlite-python/

import sqlite3
import string
from math import trunc

# open DB
conn = sqlite3.connect('Accounts.db')
cursor = conn.cursor()

# returns the hash of input string, must be consistent between sessions
def good_hash(data):
    # apply hash algorithm
    data_hash = data
    return data_hash

# generates a random string of characters of length "length"
def generateSalt(length):
    salt = ""
    for i in range(0, length):
        salt += random.choice(string.ascii_letters)
    return salt

# SQL query conditions should match sql language (ex: WHERE [condition]
def query(conditions=""):
    cursor.execute(conditions)
    return cursor.fetchall()

# Add column to users, auto salts password for security
def add_User(username, password):
    salt = generateSalt(random.randint(1, 10))
    data = (username,good_hash(password+salt),salt)
    insert_statement = '''INSERT INTO Users VALUES (?,?,?)'''
    cursor.execute(insert_statement, data)
    conn.commit()

def edit_user(username, new_username= "0", new_password= "0"):
    try:
        if new_username == "0" and new_password == "0":
            return False
        replace_statement = 'UPDATE Users '
        if new_username != "0":
            replace_statement += "SET Username = '" + new_username + "' "
        if new_password != "0":
            # this is another location where password would be hashed to prevent storing straight password data
            salt = generateSalt(random.randint(1, 10))
            new_password = good_hash(new_password + salt)
            replace_statement += "SET Password = '" + new_password + "', Salt = '" + salt + "' "
        replace_statement += "WHERE Username = '" + username + "'"
        print(replace_statement)
        cursor.execute(replace_statement)
        conn.commit()
        return True
    except sqlite3.OperationalError:
        print("Database error")
        return False

# Remove column
def delete_contact(bad):
    try:
        cursor.execute("DELETE FROM Users WHERE Username = '" + bad + "'")
        conn.commit()
        return True
    except sqlite3.OperationalError:
        print("Database error")
        return False

while True:
    print("Login - 1, Create Account - 2, View Accounts - 3, Edit Account - 4 EXIT - any other key")
    answer = input().upper()
    # login procedure
    if answer == "1":
        print("Enter Username:")
        username = input()
        print("Enter Password:")
        password = input()
        conditions = "SELECT * FROM Users WHERE Username = '" + username + "'"
        try:
            result = query(conditions)[0]
            # check hash of password with salt and compare it to stored hash, default python hash is not consistent across sessions
            if good_hash(password + result[2]) == result[1]:
                print("Login successful")
                print("Welcome " + username + "!")
                while True:
                    print("[Change username (You will be logged out) - 1], [Change password - 2], [DELETE ACCOUNT - 666], [Log Out - any other key]")
                    answer = input()
                    if answer == "1":
                        newUsername = input("Enter new Username: ")
                        name_taken = query("SELECT Username FROM Users WHERE Username = '" + newUsername + "'")
                        if len(name_taken) == 0:
                            if edit_user(username = result[0], new_username=newUsername):
                                print("Edit successful")
                            break
                        else:
                            print("Username already in use")
                    elif answer == "2":
                        newPassword = input("Enter new Password: ")
                        if edit_user(username = result[0], new_password = newPassword):
                            print("Edit successful")
                    elif answer == "666":
                        answer = input("Do you really want to DELETE THIS ACCOUNT? (y/n) ")
                        if answer == "y":
                            if delete_contact(result[0]):
                                print("Account deleted")
                            break
                    else:
                        print("Returning to main menu...")
                        break
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
        results = query("SELECT * FROM Users")
        for result in results:
            print(result)
    else:
        break

# Close the connection
conn.close()