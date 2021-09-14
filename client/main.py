import PySimpleGUI as sg
import requests
import json
import operations as ops

from requests import status_codes

#sg.theme("DarkBlue5")
credentials = {}
url = "https://api.sukhanik.no/"
sg.theme()

def login_window():
    layout = [
        [sg.Text("Please sign in", font="default 16")],
        [sg.Text("Username", size=(10,1)), sg.InputText(key="-USERNAME-")],
        [sg.Text("Password", size=(10,1)), sg.InputText(key="-PASSWORD-", password_char="*")],
        [sg.Submit("Sign In", size=(10,1)), sg.Button("Register", size=(10,1))]
    ]

    window = sg.Window("Sign in", layout, icon="icon.ico", keep_on_top=False)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Sign In":
            if values["-USERNAME-"] == "" or values["-PASSWORD-"] == "":
                sg.popup("Please enter a valid username and password", title="Error", keep_on_top=True)
            else:
                body = {"username": values["-USERNAME-"], "password": values["-PASSWORD-"]}
                
                try:
                    r = requests.post(url+"auth", json = body)
                    if r.status_code == 200:
                        data = r.json()
                        credentials["token"] = data["token"]
                        credentials["username"] = values["-USERNAME-"]
                        #print(credentials)
                        break
                    elif r.status_code == 404:
                        print(r.text)
                        sg.popup("User does not exist. Please check your username and try again", title="Wrong credentials", keep_on_top=True)
                    elif r.status_code == 401:
                        sg.popup("Incorrect password. Please try again", title="Incorrect password")
                        window["-PASSWORD-"].update("")
                except requests.exceptions.ConnectionError as e:
                    sg.popup("Cannot connect to server. Please check your internet connection and try again", title="No connection", keep_on_top=True)
        
        elif event == "Register":
            window.close()
            register_user()

    window.close()


def register_user():
    w = 15
    layout = [
        [sg.Text("Register", font="default 16")],
        [sg.Text("First Name", size=(w,1)), sg.InputText(key="-FNAME-")],
        [sg.Text("Last Name", size=(w,1)), sg.InputText(key="-LNAME-")],
        [sg.Text("Username", size=(w,1)), sg.InputText(key="-USERNAME-")],
        [sg.Text("Password", size=(w,1)), sg.InputText(key="-PASSWORD-", password_char="*")],
        [sg.Text("Confirm Password", size=(w,1)), sg.InputText(key="-CONFIRMPASSWORD-", password_char="*")],
        [sg.Submit("Register", size=(10,1)), sg.Button("Clear Fields", size=(10,1)), sg.Button("Cancel", size=(10,1))]
    ]

    window = sg.Window("Register", layout, icon="icon.ico")

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Register":
            if not ops.validate(("-FNAME-", "-LNAME-", "-USERNAME-", "-PASSWORD-", "-CONFIRMPASSWORD-"), values):
                sg.popup("Please fill out all the fields", title="Error", keep_on_top=True)
            else:
                errors = ops.check_reg_errors(values)
                if not errors:
                    print("All good")
                    registration_status = ops.register_user(values)

                    if registration_status == "OK":
                        sg.popup("User successfully created. You may now sign in", title="User Created", keep_on_top=True)
                        break
                    else:
                        sg.popup(registration_status, title="Error", keep_on_top=True)
                else:
                    print("Error")
                    sg.popup("There are errors in the entered fields:\n\n" + errors, title="Error", keep_on_top=True)
        elif event == "Clear Fields":
            pass

        elif event == "Cancel":
            window.close()
            login_window()


def get_data():
    layout = [
        [sg.Text("Loading data...")]
    ]


if __name__ == "__main__":
    login_window()
    print(credentials)