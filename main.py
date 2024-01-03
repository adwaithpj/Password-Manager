# ---------------------------- PASSWORD GENERATOR ------------------------------- #
import random
import string
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame,ttk,messagebox
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pyperclip
from jsondic import JsonDict
import json

def generate_password(length=12):
    entry_3.delete(0, 'end')
    characters = string.ascii_letters + string.digits + string.punctuation
    pass_word = ''.join(random.choice(characters) for _ in range(length))
    entry_3.insert(0,pass_word)
    pyperclip.copy(pass_word)



# cred_path = r"credientials.json"
#
# # Set up credentials
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
# gc = gspread.authorize(credentials)
#
# # Open the Google Sheet by title
# sheet = gc.open("Password_Manager").sheet1

# ---------------------------- SAVE PASSWORD ------------------------------- #

def clear_field():
    entry_1.delete(0,"end")
    entry_2.delete(0,"end")
    entry_3.delete(0,"end")
    return 1
def save_password():
    website_data = entry_1.get()
    email_or_username_data = entry_2.get()
    password_data = entry_3.get()

    # Check if all required fields are provided before saving
    if website_data and email_or_username_data and password_data:
        is_ok = messagebox.askokcancel(title=website_data,message=f"These are the details entered: \nEmail: {email_or_username_data}\nPassword: {password_data}\nIs it ok to save?")
        if is_ok:
            # --------------------------------- JSON SAVE FILE ---------------------------------#
            json_data = JsonDict(website_data,email_or_username_data,password_data)

            # Append the data to the Google Sheet
            # data_to_append = [website_data, email_or_username_data,password_data]
            # sheet.append_row(data_to_append)

            # If you want to save the password locally , uncomment the below code
            # with open("Password.csv", "a") as file:
            #     file.write(f"{website_data}\t|\t{email_or_username_data}\t|\t{password_data}\n")
            #
            #     file.close()

            save_ok = messagebox.showinfo(title="Password Saved",message="Password saved successfully!")
            window.after(0, lambda: clear_field())
            window.after(0, lambda: entry_1.focus())

    else:
        if not website_data:
            entry_1.config(highlightcolor="red",highlightthickness=1)
            window.after(3000, lambda: entry_1.config(highlightcolor="white",highlightthickness=0))
        if not email_or_username_data:
            entry_2.config(highlightcolor="red", highlightthickness=1)
            window.after(3000, lambda: entry_2.config(highlightcolor="white", highlightthickness=0))
        if not password_data:
            entry_3.config(highlightcolor="red", highlightthickness=1)
            window.after(3000, lambda: entry_3.config(highlightcolor="white", highlightthickness=0))

# ---------------------------- PASSWORD SEARCH SETUP ------------------------------- #
def search_password():
    website_to_search = entry_1.get()
    try:
        with open('pass.json', 'r') as json_file:
            data = json.load(json_file)
            if website_to_search in data:
                print_email = data[website_to_search]["email"]
                print_password = data[website_to_search]["password"]
                print_password = JsonDict.decode_password(JsonDict,print_password)
                messagebox.showinfo(title=website_to_search,
                                    message=f"Email: {print_email}\nPassword: {print_password}")
                pyperclip.copy(print_password)
            else:
                messagebox.showerror(title="Error",message="No Website  Found!")
    except FileNotFoundError:
        messagebox.showerror(title="Error",message="No Data File Found!")

# ---------------------------- UI SETUP ------------------------------- #

# from tkinter import *
# Explicit imports to satisfy Flake8


# OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")
#
#
# def relative_to_assets(path: str) -> Path:
#     return ASSETS_PATH / Path(path)


window = Tk()
window.title("Password Manager")
icon_path = r"assets\icon.ico"
window.iconbitmap(icon_path)
window.geometry("767x464")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=464,
    width=767,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=r"assets\frame0\image_1.png")
image_1 = canvas.create_image(
    135.0,
    232.0,
    image=image_image_1
)

canvas.create_text(
    54.0,
    153.0,
    anchor="nw",
    text="Guard.\nManage.\nSimplify.",
    fill="#FFFFFF",
    font=("Montserrat Bold", 33 * -1)
)

canvas.create_rectangle(
    334.0,
    135.0,
    722.0,
    178.0,
    fill="#FFFFFF",
    outline="")

entry_image_1 = PhotoImage(
    file=r"assets\frame0\entry_1.png")
entry_bg_1 = canvas.create_image(
    496.5,
    156.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#F3F3F3",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=340.0,
    y=137.0,
    width=213.0,
    height=41.0
)

canvas.create_rectangle(
    333.0,
    208.0,
    721.0,
    251.0,
    fill="#FFFFFF",
    outline="")

entry_image_2 = PhotoImage(
    file=r"assets\frame0\entry_2.png")
entry_bg_2 = canvas.create_image(
    527.0,
    229.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#F3F3F3",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=339.0,
    y=210.0,
    width=376.0,
    height=41.0
)

canvas.create_rectangle(
    334.0,
    281.0,
    559.0,
    324.0,
    fill="#FFFFFF",
    outline="")

entry_image_3 = PhotoImage(
    file=r"assets\frame0\entry_3.png")
entry_bg_3 = canvas.create_image(
    446.5,
    302.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#F3F3F3",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=340.0,
    y=283.0,
    width=213.0,
    height=41.0,
)

canvas.create_text(
    334.0,
    113.0,
    anchor="nw",
    text="Website name",
    fill="#8D8D8D",
    font=("DMSans Regular", 11 * -1)
)

canvas.create_text(
    333.0,
    186.0,
    anchor="nw",
    text="Email/Username",
    fill="#8D8D8D",
    font=("DMSans Regular", 11 * -1)
)

canvas.create_text(
    334.0,
    259.0,
    anchor="nw",
    text="Password",
    fill="#8D8D8D",
    font=("DMSans Regular", 11 * -1)
)

canvas.create_rectangle(
    586.0,
    291.0,
    684.0,
    334.0,
    fill="#FFFFFF",
    outline="")

button_image_1 = PhotoImage(
    file=r"assets\frame0\button_1.png")
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    # command=lambda: print("button_1 clicked"),
    relief="flat",
    command=generate_password
)
button_1.place(
    x=576.0,
    y=281.0,
    width=146.0,
    height=43.0
)

canvas.create_rectangle(
    319.0,
    370.0,
    630.0,
    416.0,
    fill="#FFFFFF",
    outline="")

button_image_2 = PhotoImage(
    file=r"assets\frame0\button_2.png")
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=save_password,
    relief="flat"
)
button_2.place(
    x=334.0,
    y=347.0,
    width=388.0,
    height=46.0
)
button_image_3 = PhotoImage(
    file=r"assets\frame0\button_3.png")
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=search_password,
    relief="flat"
)
button_3.place(
    x=679.0,
    y=135.0,
    width=43.0,
    height=43.0
)
canvas.create_text(
    405.0,
    47.0,
    anchor="nw",
    text="Password Manager",
    fill="#000000",
    font=("FreeSans Bold", 25 * -1)
)

# Changes
entry_1.focus()
# entry_2.insert(0,"adwaithleans616@")
window.resizable(False, False)
window.mainloop()
