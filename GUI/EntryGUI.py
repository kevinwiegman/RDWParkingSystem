from tkinter import *


buttons = [
    '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '',
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '\\', '7', '8', '9', 'BACK',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '[', ']', '4', '5', '6'
    , 'SHIFT',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?', '/', '1', '2', '3', 'SPACE',
]
invoer = []


def select(value):
    if value == "BACK":
        entry.delete(len(entry.get()) - 1, END)
        invoer.pop()
        print(invoer)

    elif value == "SPACE":
        entry.insert(END, ' ')
    elif value == " Tab ":
        entry.insert(END, '    ')
    else:
        # entry.insert(tkinter.END, value)
        entry.insert(END, value)
        invoer.append(value)
        print(invoer)


def check_kenteken():
    # checkt kenteken
    kenteken = "aaa"
    # if kenteken == "NOTALLOWED":  # Check if the car release is after 2001 AND uses a Diesel engine
    #     return not_allowed_screen()
    if len(kenteken) == 0:  # Geen kenteken gevonden
        return not_found_screen()
    else:
        return found_screen(kenteken)  # Kenteken gevonden


def start_screen():
    # Start scherm ('Welkom', BTN: Start)
    start = Tk()
    start.title('')
    start.geometry('550x300')
    start.configure(background='white')
    start.columnconfigure(1, minsize=150)
    start.rowconfigure(1, minsize=50)
    start.rowconfigure(3, minsize=30)
    w = Label(start, text="Welkom", font=("Arial", 20), background="white")
    w.grid(row=1, column=3)
    btn = Button(start, text='Start', height=3, width=15, font=("Arial", 20), command=start.destroy)
    btn.grid(row=4, column=3, sticky=W)
    mainloop()


def check_screen():
    # Kenteken check scherm ('Kenteken scannen...')
    checkscreen = Tk()
    checkscreen.title('')
    checkscreen.geometry('550x300')
    checkscreen.configure(background='white')
    w = Label(checkscreen, text="Kenteken scannen...", font=("Arial", 20), background="white")
    w.pack(side='top')
    w.after(2000, lambda: checkscreen.destroy())
    mainloop()


def not_allowed_screen():
    # Kenteken niet toegestaan ('Uw auto is niet toegestaan')
    notallowed = Tk()
    notallowed.title('')
    notallowed.geometry('550x300')
    notallowed.configure(background='white')
    btn = Button(notallowed, text='NOT ALLOWED', height=6, width=20, font=("Arial", 20), command=notallowed.destroy)
    btn.place(relx=.5, rely=.5, anchor="c")
    mainloop()


def found_screen(kenteken):
    # Kenteken gevonden ('Kenteken: XX-XX-XX' 'Is dit juist?', BTN: JA. BTN: Handmatig)
    found = Tk()
    found.title('')
    found.geometry('550x300')
    found.configure(background='white')
    w = Label(found, text="Kenteken: "+ kenteken, font=("Arial", 20), background="white")
    w.pack(side='top')
    k = Label(found, text='Is dit juist?', font=("Arial", 20), background="white")
    k.pack(side='top')

    global test2
    test2 = 0

    def handmatig():
        global test2
        test2 = 1
        found.destroy()
        handmatig_screen()

    btn = Button(found, text='Ja', height=3, width=15, font=("Arial", 20), command=found.destroy)
    btn2 = Button(found, text='Handmatig', height=3, width=15, font=("Arial", 20), command=handmatig)
    btn.place(x=200, y=350, anchor="c")
    btn2.place(x=600, y=350, anchor="c")
    mainloop()


def not_found_screen():
    # Kenteken niet gevonden ('Kenteken niet gevonden', BTN: Opnieuw, BTN: Handmatig)
    denied = Tk()
    denied.title('')
    denied.geometry('550x300')
    denied.configure(background='white')
    btn = Button(denied, text='NOT FOUND', height=6, width=20, font=("Arial", 20), command=denied.destroy)
    btn.place(relx=.5, rely=.5, anchor="c")
    mainloop()


def handmatig_screen():
    kb = Tk()
    kb.title("HosoKeys")
    kb.geometry('550x300')
    kb.resizable(0, 0)
    #kb.columnconfigure(0, minsize=230)
    kb.rowconfigure(0, minsize=80)
    kb.rowconfigure(2, minsize=20)
    global entry
    entry = Entry(kb, width=50)
    entry.grid(row=1, columnspan=15)
    varRow = 3
    varColumn = 0

    for button in buttons:

        command = lambda x=button: select(x)

        if button == "SPACE" or button == "SHIFT" or button == "BACK":
            Button(kb, text=button, width=6, bg="#3c4987", fg="#ffffff",
                           activebackground="#ffffff", activeforeground="#3c4987", relief='raised', padx=1,
                           pady=1, bd=1, command=command).grid(row=varRow, column=varColumn)

        else:
            Button(kb, text=button, width=4, bg="#3c4987", fg="#ffffff",
                           activebackground="#ffffff", activeforeground="#3c4987", relief='raised', padx=1,
                           pady=1, bd=1, command=command).grid(row=varRow, column=varColumn)

        varColumn += 1

        if varColumn > 14 and varRow == 3:
            varColumn = 0
            varRow += 1
        if varColumn > 14 and varRow == 4:
            varColumn = 0
            varRow += 1
        if varColumn > 14 and varRow == 5:
            varColumn = 0
            varRow += 1
    kb.mainloop()


while True:
    start_screen()
    check_screen()

    check_kenteken()
    print(test2)
    # handmatig_screen()
