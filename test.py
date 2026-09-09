produse = {
    "lapte": 7.5,
    "paine": 4,
    "oua": 12.3,
    "cafea": 25
}

produse_cos = {}

total_pret = 0.0

while True:
    user_input = input("Ce produs vrei sa cumperi? ").lower()

    if user_input == "stop":
        break

    if user_input not in produse:
        print("Produsul dorit nu se afla in stoc.")
        continue

    try:
        cantitate = float(input("Ce cantitate doresti sa cumperi? "))
    except ValueError:
        print("Cantitatea trebuie sa fie un numar.")
        continue

    if cantitate <= 0:
        print("Cantitatea trebuie sa fie mai mare decat 0.")
        continue

    pret_unitar = produse[user_input]
    total_produs = pret_unitar * cantitate

    print(f"Pret per bucata pentru {user_input}: {pret_unitar}")
    print(f"Pret pentru cantitatea introdusa: {total_produs}")

    total_pret += total_produs

    if user_input in produse_cos:
        produse_cos[user_input] += cantitate
    else:
        produse_cos[user_input] = cantitate

    print(f"Total cos: {total_pret}")

print("\nProduse in cos:")
for produs, cantitate_cos in produse_cos.items():
        print(f"{produs}: {cantitate_cos}")

print(f"\nTotal final: {total_pret}")