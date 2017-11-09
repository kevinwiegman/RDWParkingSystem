from tkinter import *
from car import Car
from db import Database
import recognize
import config
kentekenbuttons = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ' ', '7', '8', '9', 'BACK',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ' ', ' ', '4', '5', '6', '  ',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ' ', ' ', ' ', ' ', '1', '2', '3', '  ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '0', ' ', '  ',
]

invoer = []
car = ''

def select(value):
    """"
    Functie van de keyboard code, pakt de input en voegt deze toe aan list(invoer)
    """
    if value == "BACK":
        entry.delete(len(entry.get()) - 1, END)
        invoer.pop()
        print(invoer)

    elif value == " " or value == "  ":
        None

    else:
        entry.insert(END, value)
        invoer.append(value)
        print(invoer)


def check_kenteken():
    # TODO: check of kenteken via Image Text Recognition gevonden kan worden
    """"
    Check of de Image Text Recognition een kenteken heeft gevonden
    """
    global kenteken
    kenteken = recognize.extract(config.imagePointer)
    #TODO: RegEX check
    print(len(kenteken))
    if len(kenteken) >= 7:  # Geen kenteken gevonden
        return found_screen(kenteken) # Kenteken gevonden
    else:
        return not_found_screen()

def check_kenteken_database(kenteken):
    """"
    Check of het kenteken in de huidige kenteken database aanwezig is
    """
    # TODO: Kenteken in huidige database zoeken
    db = Database()
    print(kenteken)
    if db.get_unreleased_car_record_by_number_plate(kenteken) is not None:
        check_payed(kenteken)
    else:
        kenteken_not_known_screen()


def check_payed(kenteken):
    """"
    Functie die checkt of er betaald is
    """
    # TODO: Check of er betaald is
    betaald = False  # test

    db = Database()
    car = db.get_car_by_number_plate(kenteken)
    if car.is_paid():
        exit_screen()
    else:
        not_payed_screen()


def start_screen():
    """"
    scherm: Start scherm
    String: Welkom
    Button: Start
    """""
    start = Tk()
    start.title('PayGUI')
    start.geometry('550x300+100+100')
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
    """"
    scherm: Kenteken checken
    String: Kenteken scannen...
    Sleep: 8 seconden
    """""
    checkscreen = Tk()
    checkscreen.title('EntryGUI')
    checkscreen.geometry('550x300+100+100')
    checkscreen.configure(background='white')

    def next():
        checkscreen.destroy()
        check_kenteken()

    w = Label(checkscreen, text="Kenteken scannen...", font=("Arial", 20), background="white")
    w.pack(side='top')
    w.after(2000, lambda: next())
    mainloop()


def not_found_screen():
    """"
    Scherm: Kenteken NIET gevonden
    String: Kenteken niet gevonden
    Button: Opnieuw
            Handmatig
    """
    denied = Tk()
    denied.title('EntryGUI')
    denied.geometry('550x300+100+100')
    denied.configure(background='white')
    w = Label(denied, text="Kenteken niet gevonden", font=("Arial", 20), background="white")
    w.pack(side='top')

    def handmatig():
        denied.destroy()
        invoer_kenteken_screen()

    def opnieuw():
        denied.destroy()
        check_screen()

    btn = Button(denied, text='Opnieuw', height=3, width=15, font=("Arial", 20), command=opnieuw)
    btn2 = Button(denied, text='handmatig', height=3, width=15, font=("Arial", 20), command=handmatig)
    btn.place(x=140, y=200, anchor="c")
    btn2.place(x=410, y=200, anchor="c")
    mainloop()


def invoer_kenteken_screen():
    """"
    Scherm: kenteken invoeren
    String: Kenteken:
    Button: Keyboard layout
            Annuleren
            Bevestigen
    """
    global invoer
    invoer = []
    kb = Tk()
    kb.title("PayGUI")
    kb.geometry('550x300+100+100')
    kb.resizable(0, 0)
    kb.configure(background='white')
    kb.rowconfigure(0, minsize=80)
    kb.rowconfigure(2, minsize=20)
    global entry
    entry = Entry(kb, width=50)
    entry.grid(row=1, columnspan=15)
    varrow = 3
    varcolumn = 0

    for button in kentekenbuttons:

        command = lambda x=button: select(x)

        if button == "SPACE" or button == "SHIFT" or button == "BACK" or button == "  ":
            Button(kb, text=button, width=6, bg="#3c4987", fg="#ffffff",
                           activebackground="#ffffff", activeforeground="#3c4987", relief='raised', padx=1,
                           pady=1, bd=1, command=command).grid(row=varrow, column=varcolumn)

        else:
            Button(kb, text=button, width=4, bg="#3c4987", fg="#ffffff",
                           activebackground="#ffffff", activeforeground="#3c4987", relief='raised', padx=1,
                           pady=1, bd=1, command=command).grid(row=varrow, column=varcolumn)

        varcolumn += 1

        if varcolumn > 14 and varrow == 3:
            varcolumn = 0
            varrow += 1
        if varcolumn > 14 and varrow == 4:
            varcolumn = 0
            varrow += 1
        if varcolumn > 14 and varrow == 5:
            varcolumn = 0
            varrow += 1

    def nextscreen():
        global kenteken
        kenteken = ''.join(invoer)
        print(kenteken)
        if len(kenteken) < 1:
            None
        else:
            kb.destroy()
            check_kenteken_database(kenteken.upper())

    w = Label(kb, text="Kenteken:", font=("Arial", 20), background="white")
    w.place(x=270, y=50, anchor="c")
    test2 = Button(kb, text='Annuleren', height=1, width=15, font=("Arial", 20), command=kb.destroy)
    test3 = Button(kb, text='Bevestigen', height=1, width=15, font=("Arial", 20), command=nextscreen)
    test2.place(x=140, y=250, anchor="c")
    test3.place(x=410, y=250, anchor="c")
    kb.mainloop()


def found_screen(kenteken):
    """"
    Scherm: Kenteken gevonden
    String: Kenteken: XX-XX-XX
            is dit juist?
    Button: Ja
            Handmatig
    """
    found = Tk()
    found.title('EntryGUI')
    found.geometry('550x300+100+100')
    found.configure(background='white')
    w = Label(found, text="Kenteken: "+ kenteken, font=("Arial", 20), background="white")
    w.pack(side='top')
    k = Label(found, text='Is dit juist?', font=("Arial", 20), background="white")
    k.pack(side='top')

    def handmatig():
        found.destroy()
        invoer_kenteken_screen()

    def entry():
        found.destroy()
        return check_kenteken_database(kenteken)

    btn = Button(found, text='Ja', height=3, width=15, font=("Arial", 20), command=entry)
    btn2 = Button(found, text='Handmatig', height=3, width=15, font=("Arial", 20), command=handmatig)
    btn.place(x=140, y=200, anchor="c")
    btn2.place(x=410, y=200, anchor="c")
    mainloop()


def kenteken_not_known_screen():
    """"
    Scherm: Kenteken is niet gevonden
    String: Kenteken niet gevonden
    Button: Opnieuw
    """
    notknown = Tk()
    notknown.title('PayGUI')
    notknown.geometry('550x300+100+100')
    notknown.configure(background='white')
    w = Label(notknown, text="Kenteken niet gevonden", font=("Arial", 20), background="white")
    w.pack(side='top')
    w.after(3000, lambda: notknown.destroy())
    mainloop()


def not_payed_screen():
    """"
    Scherm: Niet betaald
    String: U heeft nog niet betaald, ga terug
    Sleep: 6 seconden
    """
    notpayedscreen = Tk()
    notpayedscreen.title('EntryGUI')
    notpayedscreen.geometry('550x300+100+100')
    notpayedscreen.configure(background='white')
    w = Label(notpayedscreen, text="U heeft nog niet betaald, ga terug", font=("Arial", 20), background="white")
    w.pack(side='top')
    w.after(6000, lambda: notpayedscreen.destroy())
    mainloop()


def exit_screen():
    """"
    Scherm: exit scherm
    String: U kunt uitrijden
    Sleep: 6 seconden
    """
    exitscreen = Tk()
    exitscreen.title('EntryGUI')
    exitscreen.geometry('550x300+100+100')
    exitscreen.configure(background='white')
    w = Label(exitscreen, text="U kunt uitrijden", font=("Arial", 20), background="white")
    w.pack(side='top')
    w.after(6000, lambda: exitscreen.destroy())
    mainloop()


while True:
    start_screen()
    check_screen()
    invoer_kenteken_screen()

