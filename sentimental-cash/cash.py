from cs50 import get_float

while True:
    d = get_float("Change owed: ") # d: dolares
    if d > 0:
        break # caso correcto

cents = round(d * 100) # convieto a centavos
quarters = cents // 25
dimes = (cents % 25) // 10
nickels = ((cents % 25) % 10) // 5
pennies = ((cents % 25) % 10) % 5

resultado_entero = int(quarters + dimes + nickels + pennies)

print(resultado_entero)