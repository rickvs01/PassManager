from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']


def generate_password() :
    pwd_input.delete(0, END)
    # Create empty list to store items of the password
    pxwd = []

    while len(pxwd) < int(length_input.get()) :
        pick_l = random.randint(0, len(letters) - 1)
        pxwd.append(letters[pick_l])
        pick_n = random.randint(0, len(numbers) - 1)
        pxwd.append(numbers[pick_n])
        if symbols_selected.get() :
            pick_s = random.randint(0, len(symbols) - 1)
            pxwd.append(symbols[pick_s])

        # Randomize the selected characters
    random.shuffle(pxwd)

    # Convert list into a printable string
    password = "".join(pxwd)
    pyperclip.copy(password)
    pwd_input.insert(END, password)
    messagebox.showinfo(title="Copy", message="Password has been copied to your clipboard")
    # print(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_values() :
    website = website_input.get()
    username = emun_input.get()
    password = pwd_input.get()

    # messagebox.showinfo(title="Confirm", message="Record is about to be added to the master record")

    if website != "" and username != "" and password != "" :
        is_ok = messagebox.askokcancel(title="Confirm Information", message=f"These are the details entered\n\n"
                                                                            f"User: {username}\n"
                                                                            f"Password: {password}\n"
                                                                            f"Site: {website}\n\n"
                                                                            f"Is it ok to save?")
    if is_ok :
        json_data = {
            website : {
                "username" : username,
                "password" : password,
            }
        }
        try :
            with open("data.json", "r") as data :
                # Reading the new Data
                old_data = json.load(data)
        except FileNotFoundError :
            with open("data.json", "w") as data :
                json.dump(json_data, data, indent=4)
        else :
            # Updating old data with new data
            old_data.update(json_data)

            with open("data.json", "w") as data :
                # Saving the updated data
                json.dump(old_data, data, indent=4)
        finally :
            website_input.delete(0, END)
            pwd_input.delete(0, END)
    else :
        messagebox.showinfo(title="Oops", message="Please make sure all the information is complete before proceeding")


# ---------------------------- FIND STORED DATA ------------------------------- #
def search_password() :
    website = website_input.get()
    if website != "" :
        try :
            with open("data.json") as data :
                stored_data = json.load(data)
        except FileNotFoundError :
            messagebox.showinfo(title="Error", message="No Data File found")
        else :
            if website in stored_data :
                username = stored_data[website]["username"]
                password = stored_data[website]["password"]
                messagebox.showinfo(title=website, message=f"Email: {username}\n Password: {password}")
            else :
                messagebox.showinfo(title=website, message=f"No details for {website} exists.")
    else:
        messagebox.showwarning(title="Warning",message=f"Website cannot be blank")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=100, bg="white")
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)  #
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
# timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Labels

website_label = Label(text="Website:  ", bg="white", fg="black")
website_label.grid(column=0, row=2)

emun_label = Label(text="Email/Username: ", bg="white", fg="black")
emun_label.grid(column=0, row=3)

pwd_label = Label(text="Password: ", bg="white", fg="black")
pwd_label.grid(column=0, row=5)

length_label = Label(text="Length of password: ", bg="white", fg="black")
length_label.grid(column=0, row=4)

# Input/Outputs

website_input = Entry(width=23)
website_input.grid(column=1, row=2, columnspan=1, sticky='w')
website_input.focus()

emun_input = Entry(width=40)
emun_input.grid(column=1, row=3, columnspan=2, sticky='w')
emun_input.insert(END, "email@domain.com")

pwd_input = Entry(width=23)
pwd_input.grid(column=1, row=5, sticky='w')

length_input = Entry(width=8)
length_input.insert(END, 15)
length_input.grid(column=1, row=4, sticky='w')

# Buttons

gen_pwd = Button(text="Generate New", justify="left", command=generate_password, width=13)
gen_pwd.grid(column=2, row=5)

search_data = Button(text="Search", justify="left", width=13, bg="lightblue", fg="black", command=search_password)
search_data.grid(column=2, row=2, columnspan=1, sticky="w")

add_record = Button(text="Add", width=38, bg="darkred", fg="white", command=save_values)
add_record.grid(column=1, row=6, columnspan=2)

symbols_selected = IntVar()
symbols_c = Checkbutton(text="Include Symbols", bg="white", variable=symbols_selected, highlightthickness=0)
symbols_c.select()
symbols_c.grid(column=2, row=4, columnspan=1)

# Scale
# length_s = Scale(from_=5, to=35, orient=HORIZONTAL, bg="white", length=168)  # command=scale_used
# length_s.set(10)
# length_s.grid(column=1, row=4, )  # sticky='w'

window.mainloop()
