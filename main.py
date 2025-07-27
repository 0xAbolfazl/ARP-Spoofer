from Cli import main
from Gui import arp_spoofer_gui
from os import system

user_choice = int(input('1- Command line interface (CLI)\n2- Graphical user interface (GUI)\n-- Select your version : '))
if user_choice == 1:
    system('cls')
    main()
elif user_choice == 2:
    arp_spoofer_gui()
else:
    print('Wrong number !')