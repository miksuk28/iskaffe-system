from random import choice
# TinyDB
from tinydb import TinyDB, Query

users_db = TinyDB("users.json")

CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!#¤%&/()=?-.,"


def validate(keys, dict):
    '''
    Checks if keys exist in dict,
    and if they are not equal to False

    :return:    True on OK, False on bad params
    '''
    for key in keys:
        if key in dict.keys():
            if not bool(dict[key]):
                return False

        else:
            return False

    return True


def user_exists(user, db=users_db):
    '''
    Checks if user exists in database

    :param user:    user dict to check
    :param db:      tinydb instance
    :return:        True if exists, else: False

    '''
    User = Query()
    return users_db.search(User.username == user)


def generate_salt(length=16):
    '''
    Generates a salt to be used in password hashing

    :param length:  length of salt, default 16
    :return:        salt
    '''
    salt = []
    for i in range(length):
        salt.append(choice(CHARS))

    return "".join(salt)

def add_user(user, db=users_db):
    new_user = {"fname": user["fname"], "lname": user["lname"], "username": user["username"], "password": user["password"]}
    users_db.insert(new_user)