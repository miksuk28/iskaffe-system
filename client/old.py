import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Input

sg.theme("Reddit")

def login_window():
    layout = [
        [sg.Text("Username")],
        [sg.Input(key="USERNAME", size=(40,1))],
        [sg.Text("Password")],
        [sg.Input(key="PASSWORD", size=(40,1), password_char="*")],
        [sg.Button("Sign In", key="SIGN-IN", size=(10,1)), sg.Button("Exit", size=(10,1))]
    ]

    window = sg.Window("Sign in", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "SIGN-IN":
            if values["USERNAME"] == "" or values["PASSWORD"] == "":
                sg.Popup("Please enter a valid username and password", keep_on_top=True)

    window.close()



if __name__ == "__main__":
    login_window()