from tkinter import *
import recognize
import config
from car import Car
from API import RDWAPI
from db import Database
buttons = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ' ', '7', '8', '9', 'BACK',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ' ', ' ', '4', '5', '6', '  ',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ' ', ' ', ' ', ' ', '1', '2', '3', '  ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '0', ' ', '  ',
]

invoer = []
car = None

# TODO: variable "kenteken" -> "licenseplate"


def select(value):
    """"
    Keyboard function. Takes de input and adds it to list(input)
    """
    # TODO: variable "invoer" -> "input"
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

# TODO: def check_kenteken() -> def check_licenseplace()
def check_kenteken():
    """"
    Check if the Image Text Recognition found a license plate
    """
    global kenteken
    kenteken = recognize.extract(config.imagePointer)
    #TODO: RegEX check
    if len(kenteken) > 7:
        return found_screen(kenteken)
    else:
        return not_found_screen()


def check_rdw():
    """"
    Check if the license plate is allowed
    """
    global kenteken
    print(kenteken)
    rdw = RDWAPI(kenteken)
    global car
    car = rdw.get_car()
    car.set_file_location(config.imagePointer)

    if car.parking_allowed():  # Check if the car release is after 2001 AND uses a Diesel engine
        return entry_screen()
    else:
        return not_allowed_screen()


def start_screen():
    """"
    Screen: Start
    String: Welkom
    Button: Start
    """""
    start = Tk()
    start.title('EntryGUI')
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
    Screen: license plate check
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


def not_allowed_screen():
    """"
    Screen: License plate not allowed
    String: Helaas, uw voertuig voldoent niet aan de eisen...
    Sleep: 8 seconden
    """
    notallowed = Tk()
    notallowed.title('EntryGUI')
    notallowed.geometry('550x300+100+100')
    notallowed.configure(background='white')
    w = Label(notallowed, text="Helaas, uw voertuig voldoet niet aan de", font=("Arial", 20), background="white")
    w2 = Label(notallowed, text="eisen om in het centrum van Utrecht te", font=("Arial", 20), background="white")
    w3 = Label(notallowed, text="rijden. Hierom mogen wij u geen toegang", font=("Arial", 20), background="white")
    w4 = Label(notallowed, text="verlenen aan Parkeergarage de Kruisstraat", font=("Arial", 20), background="white")
    w.place(x=10, y=50, anchor="w")
    w2.place(x=10, y=100, anchor="w")
    w3.place(x=10, y=150, anchor="w")
    w4.place(x=10, y=200, anchor="w")
    w.after(8000, lambda: notallowed.destroy())
    mainloop()


def found_screen(kenteken):
    """"
    Screen: License plate found
    String: Kenteken: XX-XX-XX
            is dit juist?
    Button: Ja
            Handmatig
    """
    found = Tk()
    found.title('EntryGUI')
    found.geometry('550x300+100+100')
    found.configure(background='white')
    w = Label(found, text="Kenteken: " + kenteken, font=("Arial", 20), background="white")
    w.pack(side='top')
    k = Label(found, text='Is dit juist?', font=("Arial", 20), background="white")
    k.pack(side='top')

    def handmatig():
        found.destroy()
        handmatig_screen()

    def entry():
        found.destroy()
        check_rdw()

    btn = Button(found, text='Ja', height=3, width=15, font=("Arial", 20), command=entry)
    btn2 = Button(found, text='Handmatig', height=3, width=15, font=("Arial", 20), command=handmatig)
    btn.place(x=140, y=200, anchor="c")
    btn2.place(x=410, y=200, anchor="c")
    mainloop()


def not_found_screen():
    """"
    Screen: License plate NOT found
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

    def manual():
        denied.destroy()
        handmatig_screen()

    def retry():
        denied.destroy()
        check_screen()

    btn = Button(denied, text='Opnieuw', height=3, width=15, font=("Arial", 20), command=retry)
    btn2 = Button(denied, text='handmatig', height=3, width=15, font=("Arial", 20), command=manual)
    btn.place(x=140, y=200, anchor="c")
    btn2.place(x=410, y=200, anchor="c")
    mainloop()


def handmatig_screen():
    """"
    Screen: Manual input of license plate
    String: Kenteken:
    Button: Keyboard layout
            Annuleren
            Bevestigen
    """
    # TODO: variable "invoer" -> "input"
    global invoer
    invoer = []
    kb = Tk()
    kb.title('EntryGUI')
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

    for button in buttons:

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
            check_rdw()

    w = Label(kb, text="Kenteken:", font=("Arial", 20), background="white")
    w.place(x=270, y=50, anchor="c")
    test2 = Button(kb, text='Annuleren', height=1, width=15, font=("Arial", 20), command=kb.destroy)
    test3 = Button(kb, text='Bevestigen', height=1, width=15, font=("Arial", 20), command=nextscreen)
    test2.place(x=140, y=250, anchor="c")
    test3.place(x=410, y=250, anchor="c")
    kb.mainloop()


def entry_screen():
    """"
    Screen: Entry
    String: U kunt inrijden
    Sleep: 8 seconden
    """
    print(kenteken)
    global car
    store = Database()
    store.insert_car(car)

    entryscreen = Tk()
    entryscreen.title('EntryGUI')
    entryscreen.geometry('550x300+100+100')
    entryscreen.configure(background='white')
    w = Label(entryscreen, text="U kunt inrijden", font=("Arial", 20), background="white")
    w.pack(side='top')
    w.after(8000, lambda: entryscreen.destroy())
    mainloop()


while True:
    start_screen()
    check_screen()
    check_kenteken()
