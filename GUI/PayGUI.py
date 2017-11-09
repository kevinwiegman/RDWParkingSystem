from tkinter import *
from db import Database
import config

kentekenbuttons = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ' ', '7', '8', '9', 'BACK',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ' ', ' ', '4', '5', '6', '  ',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ' ', ' ', ' ', ' ', '1', '2', '3', '  ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '0', ' ', '  ',
]

invoicebuttons = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ' ', '7', '8', '9', 'BACK',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ' ', ' ', '4', '5', '6', '  ',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ' ', ' ', ' ', ' ', '1', '2', '3', '  ',
    '!', '@', '#', '$', '%', '^', '&', '*', ',', '.', ' ', ' ', '0', ' ', '  ',
]

invoicebuttons_numbers = [
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '7', '8', '9', 'BACK',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '4', '5', '6', '  ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '2', '3', '  ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ',', '.', ' ', ' ', '0', ' ', '  ',
]

invoer = []


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


def check_kenteken_database(kenteken):
    """"
    Check of het kenteken in de huidige kenteken database aanwezig is
    """
    # TODO: Kenteken in huidige database zoeken
    db = Database()
    if db.get_unreleased_car_record_by_number_plate(kenteken) is not None:
        pay_or_invoice_screen(kenteken)
    else:
        kenteken_not_known_screen()


def check_factuur_database(kenteken):
    """"
    Check of het kenteken al bekend is in de database en gekoppeld is aan een account
    """
    # TODO: Kenteken in factuur database zoeken
    db = Database()
    user = db.check_if_user_details_known_by_number_plate(kenteken)

    # TODO: Prettify
    if user is not None:
        return [True, user]
    else:
        return [False]


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
            check_kenteken_database(kenteken)

    w = Label(kb, text="Kenteken:", font=("Arial", 20), background="white")
    w.place(x=270, y=50, anchor="c")
    test2 = Button(kb, text='Annuleren', height=1, width=15, font=("Arial", 20), command=kb.destroy)
    test3 = Button(kb, text='Bevestigen', height=1, width=15, font=("Arial", 20), command=nextscreen)
    test2.place(x=140, y=250, anchor="c")
    test3.place(x=410, y=250, anchor="c")
    kb.mainloop()

# Avoiding name collision
def pay_or_invoice_screen(number_plate):
    """"
    Scherm: Keuze tussen gelijk betalen of factuur
    String: Betaalwijze
    Button: Cash / Pin
            Factuur
    """
    global kenteken
    kenteken = number_plate
    choose = Tk()
    choose.title('PayGUI')
    choose.geometry('550x300+100+100')
    choose.configure(background='white')
    w = Label(choose, text="Betaalwijze", font=("Arial", 20), background="white")
    w.pack(side='top')

    def cashpin():
        choose.destroy()
        pay_screen()

    def factuur():
        global kenteken
        if check_factuur_database(kenteken)[0]:
            choose.destroy()
            make_invoice_screen()
        else:
            choose.destroy()
            kenteken_not_in_factuur_database_screen(kenteken)

    btn = Button(choose, text='Cash / Pin', height=3, width=15, font=("Arial", 20), command=cashpin)
    btn2 = Button(choose, text='Factuur', height=3, width=15, font=("Arial", 20), command=factuur)
    btn.place(x=140, y=200, anchor="c")
    btn2.place(x=410, y=200, anchor="c")
    mainloop()


def pay_screen():
    """"
    Scherm: Bedrag en manier van betalen
    String: Parkeertijd:
            Bedrag:
    Button: Betalen
            Annuleren
    """
    global kenteken
    db = Database()
    car = db.get_car_by_number_plate(kenteken)
    print(car.get_number_plate())
    db.set_unrealeased_car_to_released_by_car(car)
    parking_duration = str(db.get_released_car_duration_by_car(car))
    price = str(10 * parking_duration) # TODO: Bedrag berekenen en importeren

    pay = Tk()
    pay.title('PayGUI')
    pay.geometry('550x300+100+100')
    pay.configure(background='white')
    w = Label(pay, text="Parkeertijd: " + parking_duration, font=("Arial", 20), background="white")
    w2 = Label(pay, text="Bedrag: €" + price, font=("Arial", 20), background="white")
    w.place(x=10, y=50, anchor="w")
    w2.place(x=10, y=100, anchor="w")

    def betalen():
        pay.destroy()
        payment_done_screen()

    def annuleren():
        pay.destroy()

    btn = Button(pay, text='Betalen', height=3, width=15, font=("Arial", 20), command=betalen)
    btn2 = Button(pay, text='Annuleren', height=3, width=15, font=("Arial", 20), command=annuleren)
    btn.place(x=140, y=200, anchor="c")
    btn2.place(x=410, y=200, anchor="c")
    mainloop()


def payment_done_screen():
    """"
    Scherm: betaald + uitrijtijd
    String: U heeft Betaald
    sleep: 5 seconden
    """
    pay = Tk()
    pay.title('PayGUI')
    pay.geometry('550x300+100+100')
    pay.configure(background='white')
    pay.columnconfigure(1, minsize=150)
    pay.rowconfigure(1, minsize=50)
    pay.rowconfigure(3, minsize=30)
    w = Label(pay, text="U heeft betaald", font=("Arial", 30), background="white")
    w.after(5000, lambda: pay.destroy())
    w.pack(side='top')


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

    def opnieuw():
        notknown.destroy()
        invoer_kenteken_screen()

    btn = Button(notknown, text='Opnieuw', height=3, width=15, font=("Arial", 20), command=opnieuw)
    btn.place(x=270, y=200, anchor="c")
    mainloop()


def kenteken_not_in_factuur_database_screen():
    """"
    Scherm: Kenteken is niet gekoppeld aan account
    String: Het kenteken is nog niet gekoppeld aan een account
    Button: Account maken
            Annuleren
    """
    choose = Tk()
    choose.title('PayGUI')
    choose.geometry('550x300+100+100')
    choose.configure(background='white')
    w = Label(choose, text="Factuurgegevens niet bekend", font=("Arial", 20), background="white")
    w.pack(side='top')

    def company_fun():
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

        for button in invoicebuttons:

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
            global company
            company = ''.join(invoer)
            print(company)
            kb.destroy()

        w = Label(kb, text="Bedrijfsnaam: ", font=("Arial", 20), background="white")
        w.place(x=275, y=25, anchor="c")
        w2 = Label(kb, text="(niet verplicht)", font=("Arial", 10), background="white")
        w2.place(x=270, y=60, anchor="c")
        test3 = Button(kb, text='Volgende', height=1, width=15, font=("Arial", 20), command=nextscreen)
        test3.place(x=270, y=250, anchor="c")
        kb.mainloop()

    def name_fun():
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

        for button in invoicebuttons:

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
            global name
            name = ''.join(invoer)
            print(name)
            if len(name) < 1:
                None
            else:
                kb.destroy()

        w = Label(kb, text="Volledige naam: ", font=("Arial", 20), background="white")
        w.place(x=275, y=25, anchor="c")
        test3 = Button(kb, text='Volgende', height=1, width=15, font=("Arial", 20), command=nextscreen)
        test3.place(x=270, y=250, anchor="c")
        kb.mainloop()

    def email_fun():
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

        for button in invoicebuttons:

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
            global email
            email = ''.join(invoer)
            print(email)
            if len(email) < 1:
                None
            else:
                if '@' in invoer and '.' in invoer:
                    kb.destroy()
                else:
                    w2 = Label(kb, text="Vul een geldig e-mailadres in!", font=("Arial", 10), background="white")
                    w2.place(x=270, y=60, anchor="c")

        w = Label(kb, text="E-mailadres", font=("Arial", 20), background="white")
        w.place(x=275, y=25, anchor="c")
        test3 = Button(kb, text='Volgende', height=1, width=15, font=("Arial", 20), command=nextscreen)
        test3.place(x=270, y=250, anchor="c")
        kb.mainloop()

    def phonenumber_fun():
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

        for button in invoicebuttons_numbers:

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
            global phonenumber
            phonenumber = ''.join(invoer)
            print(phonenumber)
            if len(phonenumber) < 1:
                None
            else:
                kb.destroy()

        w = Label(kb, text="Telefoonnummer:", font=("Arial", 20), background="white")
        w.place(x=275, y=25, anchor="c")
        test3 = Button(kb, text='Volgende', height=1, width=15, font=("Arial", 20), command=nextscreen)
        test3.place(x=270, y=250, anchor="c")
        kb.mainloop()

    def streetname_fun():
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

        for button in invoicebuttons:

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
            global streetname
            streetname = ''.join(invoer)
            print(streetname)
            if len(streetname) < 1:
                None
            else:
                kb.destroy()

        w = Label(kb, text="Straat:", font=("Arial", 20), background="white")
        w.place(x=275, y=25, anchor="c")
        test3 = Button(kb, text='Volgende', height=1, width=15, font=("Arial", 20), command=nextscreen)
        test3.place(x=270, y=250, anchor="c")
        kb.mainloop()

    def number_fun():
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

        for button in invoicebuttons_numbers:

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
            global number
            number = ''.join(invoer)
            print(number)
            if len(number) < 1:
                None
            else:
                kb.destroy()

        w = Label(kb, text="Huisnummer:", font=("Arial", 20), background="white")
        w.place(x=275, y=25, anchor="c")
        test3 = Button(kb, text='Volgende', height=1, width=15, font=("Arial", 20), command=nextscreen)
        test3.place(x=270, y=250, anchor="c")
        kb.mainloop()

    def postalcode_fun():
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
            global postalcode
            postalcode = ''.join(invoer)
            print(postalcode)
            if len(postalcode) < 1:
                None
            else:
                kb.destroy()

        w = Label(kb, text="Postcode:", font=("Arial", 20), background="white")
        w.place(x=275, y=25, anchor="c")
        test3 = Button(kb, text='Volgende', height=1, width=15, font=("Arial", 20), command=nextscreen)
        test3.place(x=270, y=250, anchor="c")
        kb.mainloop()

    def city_fun():
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

        for button in invoicebuttons:

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
            global city
            city = ''.join(invoer)
            print(city)
            if len(city) < 1:
                None
            else:
                kb.destroy()

        w = Label(kb, text="Woonplaats:", font=("Arial", 20), background="white")
        w.place(x=275, y=25, anchor="c")
        test3 = Button(kb, text='Volgende', height=1, width=15, font=("Arial", 20), command=nextscreen)
        test3.place(x=270, y=250, anchor="c")
        kb.mainloop()

    def country_fun():
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

        for button in invoicebuttons:

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
            global country
            country = ''.join(invoer)
            print(country)
            if len(country) < 1:
                None
            else:
                kb.destroy()

        w = Label(kb, text="Land:", font=("Arial", 20), background="white")
        w.place(x=275, y=25, anchor="c")
        test3 = Button(kb, text='Volgende', height=1, width=15, font=("Arial", 20), command=nextscreen)
        test3.place(x=270, y=250, anchor="c")
        kb.mainloop()

    def create_invoice():
        company_fun()
        name_fun()
        email_fun()
        phonenumber_fun()
        streetname_fun()
        number_fun()
        postalcode_fun()
        city_fun()
        country_fun()

    def create():
        choose.destroy()
        create_invoice()

    def annuleren():
        choose.destroy()

    btn = Button(choose, text='Invoeren', height=3, width=15, font=("Arial", 20), command=create)
    btn2 = Button(choose, text='Annuleren', height=3, width=15, font=("Arial", 20), command=annuleren)
    btn.place(x=140, y=200, anchor="c")
    btn2.place(x=410, y=200, anchor="c")
    mainloop()



    print("Company = " + str(company))
    print("Name = " + str(name))
    print("Email = " + str(email))
    print("Telefoonnummer = " + str(phonenumber))
    print("Straat = " + str(streetname))
    print("Huisnummer = " + str(number))
    print("Postcode = " + str(postalcode))
    print("Woonplaats = " + str(city))
    print("Land = " + str(country))

    make_invoice_screen()

    # TODO: Put all this info in the database


def make_invoice_screen(User):
    """"
    Scherm: Bedrag en knop om factuur te sturen
    String: Parkeertijd:
            Bedrag:
    Button: Versturen
            Annuleren
    """
    db = Database()
    car = db.get_car_by_number_plate(User.get_number_plate())
    db.set_unrealeased_car_to_released_by_car(car)
    parking_duration = db.get_released_car_duration_by_car(car)
    price = 10 * parking_duration  # TODO: Bedrag berekenen en importeren

    pay = Tk()
    pay.title('PayGUI')
    pay.geometry('550x300+100+100')
    pay.configure(background='white')
    w = Label(pay, text="Parkeertijd: " + parking_duration, font=("Arial", 20), background="white")
    w2 = Label(pay, text="Bedrag: €" + price, font=("Arial", 20), background="white")
    w.place(x=10, y=50, anchor="w")
    w2.place(x=10, y=100, anchor="w")

    def versturen():
        pay.destroy()
        # TODO: factuur sturen m.b.v variabele price + kenteken
        invoice_send_screen()

    def annuleren():
        pay.destroy()

    btn = Button(pay, text='Versturen', height=3, width=15, font=("Arial", 20), command=versturen)
    btn2 = Button(pay, text='Annuleren', height=3, width=15, font=("Arial", 20), command=annuleren)
    btn.place(x=140, y=200, anchor="c")
    btn2.place(x=410, y=200, anchor="c")
    mainloop()


def invoice_send_screen():
    """"
    Scherm: Factuur is verstuurd + uitrijtijd
    String:
    Button:
    """
    pay = Tk()
    pay.title('PayGUI')
    pay.geometry('550x300+100+100')
    pay.configure(background='white')
    pay.columnconfigure(1, minsize=150)
    pay.rowconfigure(1, minsize=50)
    pay.rowconfigure(3, minsize=30)
    w = Label(pay, text="Factuur is verstuurd", font=("Arial", 30), background="white")
    w.after(5000, lambda: pay.destroy())
    w.pack(side='top')


while True:
    start_screen()
    invoer_kenteken_screen()
