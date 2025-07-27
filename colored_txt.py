from colorama import init
from termcolor import colored
from os import system
system("cls")
init()
    

def gtxt(text, end='\n'):
    try:
        print(colored(text=text, color="green"), end=end)
    except Exception:
        print("Error while printing colored text")

def rtxt(text, end="\n"):
    try:
        print(colored(text=text, color="red"), end=end)
    except Exception:
        print("Error while printing colored text")

def ctxt(text, end="\n"):
    try:
        print(colored(text=text, color="cyan"), end=end)
    except Exception:
        print("Error while printing colored text")

def ytxt(text, end="\n"):
    try:
        print(colored(text=text, color="light_yellow"), end=end)
    except Exception:
        print("Error while printing colored text")


def lbtxt(text, end="\n"):
    try:
        print(colored(text=text, color="light_blue"), end=end)
    except Exception:
        print("Error while printing colored text")

def btxt(text, end="\n"):
    try:
        print(colored(text=text, color="blue"), end=end)
    except Exception:
        print("Error while printing colored text")

def mtxt(text, end="\n"):
    try:
        print(colored(text=text, color="magenta"), end=end)
    except Exception:
        print("Error while printing colored text")

def lmtxt(text, end="\n"):
    try:
        print(colored(text=text, color="light_magenta"), end=end)
    except Exception:
        print("Error while printing colored text")

def back_color(text, color='red', end='\n'):
    print(colored(text, color, on_color='on_white',attrs=['reverse']), end=end)


def lctxt(text, end="\n"):
    try:
        print(colored(text=text, color="light_cyan"), end=end)
    except Exception:
        print("Error while printing colored text")
