# TinyDB
from tinydb import TinyDB, Query

users_db = TinyDB("users.json")


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
    User = Query()
    return users_db.search(User.username == user)


def add_user(user, db=users_db):
    user.