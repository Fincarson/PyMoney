money = int(input("How much money do you have? "))
amount = int(input("Add an expense or income record with description and amount:\n").split()[1])
print(f"Now you have {money + amount} dollars.")