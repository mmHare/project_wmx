from src.minigames import bulls_n_cows, fifteen_puzzle


def add_option(opt_list, name, func):
    last_index = max([int(item["option_id"]) for item in opt_list])
    opt_list.append(dict(option_id=str(last_index+1),
                    option_name=name, function=func))
    return


def execute_option(opt_list, option_id_name):
    for item in opt_list:
        if option_id_name.lower() in [item["option_id"], item["option_name"].lower()]:
            print()
            item["function"]()
            return
    else:
        print("Brak wybranej opcji.")


def menu_minigames():
    # stworzenie listy opcji
    option_list = [dict(option_id="0", option_name="Quit", function=None)]
    add_option(option_list, "15 Puzzle", fifteen_puzzle)
    add_option(option_list, "Bulls and Cows", bulls_n_cows)

    while True:
        print("\n"*2)
        print("---Minigames---")

        # wypisanie opcji
        for option in option_list[1:]:
            print("{}. {}".format(option["option_id"], option["option_name"]))
        print("0. Wyjście (q)")

        user_input = input()
        if user_input.lower() in ["0", "q", "quit"]:
            break
        else:
            execute_option(option_list, user_input)
