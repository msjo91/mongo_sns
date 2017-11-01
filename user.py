from datetime import datetime

from pymongo import MongoClient

from main import *
from post import *


online = []

def signin(db):

    while(1):
        print("\n::::SIGN IN::::\n")
        username = input("Enter username: ")
        password = input("Enter password: ")
        if db.users.find_one({"username": username, "password": password}):
            online.append(username)
            print("Welcome, %s" % username)
            break

        else:
            print("    User does not exist or wrong password input!")
            k=input("1 is re mainpage :")
            if k=="1": # EXIT
                break

def signup(db):
    while(1):
        print("\n::::SIGN UP::::\n")
        username = input("Enter username: ")
        password = input("Enter password: ")
        if not password:
            print("    You must insert a password!")
        password_confirm = input("Confirm password: ")
        if password == password_confirm:
            if db.users.find_one({"username": username}):
                print("    User already exists!")
            else:
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                full_name = first_name + ' ' + last_name
                bday, bmonth, byear = map(int, input("Enter birthday in DD-MM-YYYY format: ").split('-'))
                try:
                    birth = datetime(byear, bmonth, bday)
                except ValueError as e:
                    print('    ' + str(e))
                email = input("Enter email: ")
                phone = input("Enter phone number: ")
                address = input("Enter address: ")
                db.users.insert({
                    "username": username,
                    "password": password,
                    "name": full_name,
                    "first name": first_name,
                    "last name": last_name,
                    "birth": birth,
                    "email": email,
                    "phone": phone,
                    "address": address
                })
                print("User creation success!")
                break
        else:
            print("Passwords don't match!")


def signout(db):
    print("See you again, %s" % online.pop())


def profile(db):
    print("\n::::MY STATUS::::\n")
    username = online[0]
    cursor = db.users.find_one({"username": username})
    print("""
    Username: {username}
    Name: {name}
    Birthday: {birth}
    Email: {email}
    Phone: {phone}
    Address: {address}
    """.format(
        username=username,
        name=cursor['name'],
        birth=str(cursor['birth']).split()[0],
        email=cursor['email'],
        phone=cursor['phone'],
        address=cursor['address']
        ))


def update_profile(db,act):
        d = {"1": "first name", "2": "last name", "3": "birth", "4": "email", "5": "phone", "6": "address", "9": "password"}
        print("\n::::UPDATE PROFILE::::\n")
        username = online[0]
        password = input("Enter password: ")
        if db.users.find_one({"username": username, "password": password}):
            if act == "3":
                bday, bmonth, byear = map(int, input("Enter new birthday in DD-MM-YYYY format: ").split('-'))
                try:
                    birth = datetime(byear, bmonth, bday)
                    db.users.update({"username": username}, {"$set": {"birth": birth}})
                    print("Update Success!")
                except ValueError as e:
                    print('    ' + str(e))
                    update_profile(act)
            else:
                new = input("Enter new %s: " % d[act])
                db.users.update({"username": username}, {"$set": {d[act]: new}})
                if act == "1" or act == "2":
                    first_name = db.users.find_one({"username": username})["first name"]
                    last_name = db.users.find_one({"username": username})["last name"]
                    full_name = first_name + ' ' + last_name
                    db.users.update({"username": username}, {"$set": {"name": full_name}})
                    print("Update Success!")
                elif act == "9":
                    new_confirm = input("Confirm password: ")
                    if new == new_confirm:
                        print("Update Success!")
                    else:
                        print("Passwords don't match!")
                        update_profile(act)
                else:
                    print("Update Success!")
        else:
            print("    Wrong password input!")




def delete_account(db):
    k=123
    while True:
        print("\n::::DELETE ACCOUNT::::\n")
        username = online[0]
        password = input("Enter password: ")
        if db.users.find_one({"username": username, "password": password}):
            verification = input("Are you sure? ")
            if verification in ['y', 'Y', 'yes', 'Yes']:
                db.users.remove({'username': username})
                print("We had a good run, %s! We'll miss you :(" % online.pop())
                break
        else:
            print("    Wrong password input!")
            k=input("0 is exit and 1 is re")
            break
    if k=="1":
        delete_account(db)
    elif k=="0":
        pass

