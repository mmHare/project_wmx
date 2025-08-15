"""PROJECT WMX"""
"""The Ultimate Learing"""


from src.globals import *
from src.menu_screens import *
from src.class_db import connection_manager
from src.menu_minigames import menu_minigames
from src.class_config import config_manager


# starting data load
config_manager.load_config()
connection_manager.reconnect()


def main():
    while True:
        """Main program loop"""
        main_menu()
        break


main()

# # Tu można wklejać funkcje
# def prime_numbers():
#     print("Wypiszę wszystkie liczby pierwsze w podanym zakresie.")
#     start = int(input("Podaj początek zakresu: "))
#     end = int(input("Podaj koniec zakresu: "))
#     liczby_pierwsze = []

#     if start > end:
#         start, end = end, start

#     if start < 2:
#         start = 2

#     if end < 2:
#         end = 2

#     for j in range(start, end+1):
#         for i in range(2, int(j ** 0.5) + 1):
#             if j % i == 0:
#                 break
#         else:
#             liczby_pierwsze.append(j)
#     print(f"Oto lista liczb pierwszych w podanym zakresie:")
#     print(liczby_pierwsze)


# def print_square():
#     bok = int(input("Podaj szerokość kwadratu: "))
#     print("*"*2*bok)
#     for i in range(bok-2):
#         print("*" + " "*(2*bok - 2) + "*")
#     print("*"*2*bok)


# def random_name_generator():
#     plec = input(
#         "Czy chcesz wygenerować imię męskie(M) czy żeńskie(F)?: ").upper()

#     fem_names = ['Felicia', 'Ayarissa', 'Freya', 'Claire', 'Alice <3']
#     mal_names = ['Rob', 'Bob', 'Cody', 'John', 'Bilbo']

#     if plec == 'F':
#         name = random.choice(fem_names)
#     elif plec == 'M':
#         name = random.choice(mal_names)

#     print(name)


# # Lista, do której wrzucamy funkcje do menu
# list_of_functions = [prime_numbers, print_square,
#                      random_name_generator, menu_minigames]
# # Podawane funkcje nie przyjmują argumentów - przyjmują wartości wewnątrz przez input użytkownika

# while True:
#     display_menu(list_of_functions)

#     option = int(input(": "))

#     if option > len(list_of_functions) or option < 0:
#         print("Brak funkcji")
#         continue
#     elif option == 0:
#         break

#     func_to_run = list_of_functions[option - 1]

#     func_to_run()
