var1 = 38
var2 = 42
var3 = var1+var2

print(var1+var3)

#fundamental data structures

arr = [11,22,33,44,"gustike"]

print(arr[0])

var4 = {
    "animal":"mata",
    "culoare":"negru"
}

print(f"Culoarea matei este {var4["culoare"]}")


offer_letter = False

if offer_letter == True:
    print("all g")
else:
    print("e false totike")

from decimal import Decimal

numar1 = Decimal("1.3")
numar2 = Decimal("0.4")

total = numar1 + numar2

if total == Decimal("1.7"):
    print("este bun")
else:
    print("nu e 1,7 totike")

i = 0

# while True:
#     user_input = input("you>")
#     if int(user_input) == 15:
#         break
#     print(user_input)