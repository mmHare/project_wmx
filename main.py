def display_menu():
    print()
    print("="*10, "MENU", "="*10)

    print("1 - Wypisz 'n' pierwszych liczb pierwszych")
    print("2 - Narysuj kwadrat o długości 'n'")
    print("3 - Wylosuj męskie lub żeńskie imię")
    print()


def prime_num(n: int) -> list:
    licznik = 0
    liczba = 2
    liczby_pierwsze = []
    while licznik < n:
        for i in range(2, int(liczba ** 0.5) + 1):
            if liczba % i == 0:
                break
        else:
            liczby_pierwsze.append(liczba)
            licznik += 1
        liczba += 1
    return liczby_pierwsze

def square(n: int):
    print("*"*2*n)
    for i in range(n-2):
        print("*" + " "*(2*n - 2) + "*")
    print("*"*2*n)

# def random_name_generator(plec: str) -> str:
    

display_menu()

option = input(": ")


if option == "1":
    prime_count = int(input("Ile liczb pierwszych wypisać? "))
    print(f"Oto lista {prime_count} pierwszych liczb pierwszych.")
    print(prime_num(prime_count))

elif option == "2":
    bok = int(input("Podaj szerokość kwadratu: "))
    print()
    square(bok)