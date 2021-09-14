import requests
import json

api_url = "https://api.sukhanik.no/"

CHARS = {
    "numbers": "01234567890",
    "letters": " abcdefghijklmnopqrstuvwxyzæøåABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ'",
}

def validate(keys, dict):
    for key in keys:
        if key in dict.keys():
            if not bool(dict[key]):
                return False

        else:
            return False

    return True


def check_reg_errors(values):
    message = ""
    errors = []

    # chech password length
    if len(values["-PASSWORD-"]) < 6:
        errors.append("• Password must be 6 characters minimum")

    # check if name contains illegal chars
    names_total = values["-FNAME-"] + values["-LNAME-"]
    for letter in names_total:
        if letter not in CHARS["letters"]:
            errors.append("• First and last name may only contain the letters A-Å")
            break
    
    # check if passwords match
    if values["-PASSWORD-"] != values["-CONFIRMPASSWORD-"]:
        errors.append("• Passwords do not match")

    if len(values["-USERNAME-"]) < 4:
        errors.append("• Username must contain at least four characters")

    if len(errors) == 0:
        return False
    else:
        for error in errors:
            message += error + "\n"

        return message
    

def register_user(values):
    def bad_error(blame, code):
        return f"The {blame} has encountered a fatal error. Please contact the administrator.\nError code: {code}"

    try:
        data = {"fname": values["-FNAME-"], "lname": values["-LNAME-"], "username": values["-USERNAME-"], "password": values["-PASSWORD-"]}
        r = requests.post(api_url + "create_user", json=data)
    except requests.exceptions.ConnectionError:
        return "Cannot connect to server. Please check your internet connection and try again"

    if r.status_code == 200:
        return "OK"
    elif r.status_code == 409:
        return "A user with this username already exists. Please pick another one"
    elif r.status_code == 400:
        return bad_error("client", 404)
    elif r.status_code == 405:
        return bad_error("client", 405)
    else:
        return "The server shat its pants trying to handle the request"