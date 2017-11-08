

system_type = int(input('Welke systeem configuratie is nu actief? \n1: Poort\n2: Sluiting \n3: Betaling'))

# try catch to check if the system type is int and or while loop for data type prevention


if system_type == 1:
    # DEFINETLY NOT NICE, TKINTER OPENS WITHOUT BEING ASKED TO DUE TO IMPORT NEEDS TO BE FIXED
    from GUI import EntryGUI
    EntryGUI.start_screen()
elif system_type == 2:
    from GUI import ExitGUI
    ExitGUI.start_screen()
elif system_type == 3:
    from GUI import PayGUI
    PayGUI.start_screen()





