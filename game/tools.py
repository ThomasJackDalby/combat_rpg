from tabulate import tabulate
from colorama import Fore, Style

def display_options(options, format_option, is_valid=None):
    i = 0
    table = []
    valid_choices = [] 
    for option in options:
        formatted_option = format_option(option)
        if is_valid is None:
            valid = True
        else:
            result = is_valid(option)
            valid = True if result is None else False
        if valid:
            row = [f"[{i}]"]+formatted_option
            i += 1
            valid_choices.append(option)
        else:
            row = [f"{result[1]}{cell}{Style.RESET_ALL}" for cell in ["[-]"]+formatted_option+[result[0]]]
            result = None
        table.append(row)

    print(tabulate(table))
    print("[P]revious [N]ext [E]xit")

    while True:
        choice = input("> ").lower()
        # if choice == "n":
        #     print("Next")
        # elif choice == "p":
        #     print("Previous")
        if choice == "e" or choice == "exit":
            return
        elif len(choice) > 0 and choice.isdigit():
            index = int(choice)
            if index >= 0 and index < i:
                option = valid_choices[index] 
                return option
            print(f"Please enter a value between 0 and {i-1}.")
        else:
            print("Duh..")