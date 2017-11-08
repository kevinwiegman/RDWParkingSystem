from tkinter import *


def check_kenteken():
    # checkt kenteken
    kenteken = "aaa"
    if kenteken == "NOTALLOWED":  # Check if the car release is after 2001 AND uses a Diesel engine
        return not_allowed_screen()
    if len(kenteken) == 0:  # Geen kenteken gevonden
        return not_found_screen()
    else:
        return found_screen(kenteken)  # Kenteken gevonden


def start_screen():
    # Start scherm ('Welkom', BTN: Start)
    start = Tk()
    start.title('')
    start.geometry('800x600')
    start.configure(background='white')
    start.columnconfigure(1, minsize=230)
    start.rowconfigure(1, minsize=100)
    w = Label(start, text="Welkom", font=("Arial", 50), background="white")
    w.grid(row=0, column=3)
    btn = Button(start, text='Start', height=6, width=20, font=("Arial", 20), command=start.destroy)
    btn.grid(row=2, column=3, sticky=W)
    mainloop()


def check_screen():
    # Kenteken check scherm ('Kenteken scannen...')
    checkscreen = Tk()
    checkscreen.title('')
    checkscreen.geometry('800x600')
    checkscreen.configure(background='white')
    w = Label(checkscreen, text="Kenteken scannen...", font=("Arial", 50), background="white")
    w.pack(side='top')
    w.after(2000, lambda: checkscreen.destroy())
    mainloop()


def not_allowed_screen():
    # Kenteken niet toegestaan ('Uw auto is niet toegestaan')
    notallowed = Tk()
    notallowed.title('')
    notallowed.geometry('800x600')
    notallowed.configure(background='white')
    btn = Button(notallowed, text='NOT ALLOWED', height=6, width=20, font=("Arial", 20), command=notallowed.destroy)
    btn.place(relx=.5, rely=.5, anchor="c")
    mainloop()


def found_screen(kenteken):
    # Kenteken gevonden ('Kenteken: XX-XX-XX' 'Is dit juist?', BTN: JA. BTN: Handmatig)
    found = Tk()
    found.title('')
    found.geometry('800x600')
    found.configure(background='white')
    w = Label(found, text="Kenteken: "+ kenteken, font=("Arial", 50), background="white")
    w.pack(side='top')
    k = Label(found, text='Is dit juist?', font=("Arial", 30), background="white")
    k.pack(side='top')
    btn = Button(found, text='Ja', height=6, width=20, font=("Arial", 20), command=found.destroy)
    btn2 = Button(found, text='Handmatig', height=6, width=20, font=("Arial", 20), command=found.destroy)
    btn.place(x=200, y=350, anchor="c")
    btn2.place(x=600, y=350, anchor="c")
    mainloop()


def not_found_screen():
    # Kenteken niet gevonden ('Kenteken niet gevonden', BTN: Opnieuw, BTN: Handmatig)
    denied = Tk()
    denied.title('')
    denied.geometry('800x600')
    denied.configure(background='white')
    btn = Button(denied, text='NOT FOUND', height=6, width=20, font=("Arial", 20), command=denied.destroy)
    btn.place(relx=.5, rely=.5, anchor="c")
    mainloop()

def handmatig_screen():
    # Handmatige invoer kenteken


while True:
    start_screen()
    check_screen()
    check_kenteken()
