'''
File is not very tidy
Could benefit from separating functions
into more modules
'''

from random import choice
import hashlib
import datetime
# TinyDB
from tinydb import TinyDB, Query

users_db = TinyDB("users.json")

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
SYMBOLS = "!#¤%&/()=?-.,"
CHARS = ALPHABET + SYMBOLS

# to be changed to a dict
tokens = {}


def get_ip(headers):
    try:
        ip = headers["X-Real-IP"]
    except KeyError:
        ip = "NO IP HEADER"

    return ip


def get_time():
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


def log_action(string):
    with open("log.txt", "a") as file:
        file.write(f"\n{get_time()} - {string}")


def validate(keys, dict):
    '''
    Checks if keys exist in dict,
    and if they are not equal to False

    :return:    True on OK, False on bad params
    '''
    if dict == None:
        return False

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
    return db.search(User.username == user)


def hash_password(password, salt=""):
    '''
    Concatenates the password and salt
    and hashes it

    :param password:    password to hash
    :salt:              salt to add to password
    :return:            hash of password + salt
    '''
    salted_pass = password + salt

    hashed_string = hashlib.sha256(salted_pass.encode("utf-8")).hexdigest()
    return hashed_string


def compare_password(username, raw_password, db=users_db):
    '''
    Adds the salt to the password
    and compares the hash to the one
    in the db

    :param username:    password of user to check
    :raw_password:      unhashed password entered by user
    :return:            True on matching hashes, False otherwise
    '''
    User = Query()
    user = db.search(User.username == username)
    user = user[0]

    hashed = hash_password(raw_password, user["salt"])

    if hashed == user["password"]:
        return True
    else:
        return False


def token_exists(token):
    '''
    Cycles through list of tokens
    and checks if token is there

    :param token:      token to check
    :return:           True if token exists, else: False
    '''
    if token in tokens:
        return True
    else:
        return False


def delete_tokens(token):
    '''
    Deletes a single token

    :param token:       token key to delete
    '''
    if token in tokens.keys():
        del tokens[token]
        return True

    return False


def get_balance(token, db=users_db):
    username = tokens[token]["username"]

    UserQuery = Query()
    user = db.search(UserQuery.username == username)
    user = user[0]

    print(user)
    return user["balance"]



def generate_token(username):
    '''
    Generates an access token for
    a user and adds it to the tokens list

    :param username:    user to generate token for
    :return:            generated token
    '''
    user_token = []
    for i in range(20):
        user_token.append(choice(ALPHABET))

    user_token = "".join(user_token)

    tokens[user_token] = {"username": username, "expires": datetime.datetime.now() + datetime.timedelta(hours=1)}

    print(tokens[user_token])
    return user_token


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
    '''
    Generates salt, hashed password
    and adds user to the database

    :param user:    user dict
    '''
    salt = generate_salt()
    password = hash_password(user["password"], salt)

    new_user = {"fname": user["fname"], "lname": user["lname"],
                "username": user["username"], "password": password, "salt": salt, "balance": 0}
    db.insert(new_user)
