# 1
import sys
RECORD_FILE = 'record.txt'

def initialize():
    records = []
    money = 0
    try:
        with open(RECORD_FILE, 'r') as f:
            try: money = int(f.readline())
            except ValueError:
                sys.stderr.write("Invalid format in records.txt. Deleting contents.\n")
                return money, records

            for line in f.readlines():
                parts = line.split()
                if (len(parts) != 2):
                    sys.stderr.write("Invalid format in records.txt. Deleting the contents.\n")
                    return money, records

                description, value = parts
                try: value = int(value)
                except ValueError:
                    sys.stderr.write("Invalid amount in records.txt. Deleting the contents.\n")
                    return money, records
                records.append(f"{description} {value}")
            print("Welcome back!")
            return money, records

    except FileNotFoundError:
        try: money = int(input("How much money do you have? "))
        except ValueError:
            sys.stderr.write("Invalid value for money. Set to 0 by default.\n\n")
            money = 0
        return money, records


def add(records, money):
    add_input = list(input("Add some expense or income records with description and amount:\n""desc1 amt1, desc2 amt2, desc3 amt3, ...\n").split(", "))

    try:
        if not add_input: raise ValueError("The format of a record should be like this: breakfast -50.\n")
        elif any(len(a.split()) != 2 for a in add_input): raise ValueError("The format of a record should be like this: breakfast -50.\n")
        elif any(not a.rsplit(" ", 1)[1].lstrip("+-").isdigit() for a in add_input):
            print("Invalid value for money.")
            print("Fail to add a record.\n")
        else:
            for a in add_input: money += int(a.split()[1])
            records.extend(add_input)
            print()
    except:
        print("The format of a record should be like this: breakfast -50.")
        print("Fail to add a record.\n")
    return records, money

def view(initial_money, records):
    print("Description    Amount")
    print("==================== ======")
    for r in records:
        description, value = r.split()
        print("%-15s%s" % (description, value))
    print("==================== ======")
    print(f"Now you have {initial_money} dollars.\n")


def delete(records, money):
    if not records:
        print("No records to delete.")
        return records, money
    else:
        del_input = input("Which record do you want to delete? ")
        try:
            if not del_input: raise ValueError("The format of a record should be like this: breakfast -50.\n")
            elif any(len(a.split()) != 2 for a in [del_input]): raise ValueError("The format of a record should be like this: breakfast -50.\n")
            elif (del_input not in records): print(f"There's no record with {del_input}. Fail to delete a record.\n")
            else:
                idx = len(records) - 1 - records[::-1].index(del_input)
                if (idx == -1 or idx == len(records)): return records, money
                money -= int(records[idx].split()[1])
                records.pop(idx)
                print()
        except: print("The format of a record should be like this: breakfast -50.\n")
    return records, money


def save(initial_money, records):
    with open(RECORD_FILE, 'w') as f:
        f.write(f"{initial_money}\n")
        f.writelines(r + '\n' for r in records)


initial_money, records = initialize()
while True:
    command = input('\nWhat do you want to do (add / view / delete / exit)? ')
    if command == 'add':
        records, initial_money = add(records, initial_money)
    elif command == 'view':
        view(initial_money, records)
    elif command == 'delete':
        records, initial_money = delete(records, initial_money)
    elif command == 'exit':
        save(initial_money, records)
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')


# 2
import sys
RECORD_FILE = 'record.txt'

def load_records():
    records = []
    money = 0
    try:
        with open(RECORD_FILE, 'r') as f:
            try: money = int(f.readline())
            except ValueError:
                sys.stderr.write("Invalid format in records.txt. Deleting contents.\n")
                return money, records
            
            for line in f.readlines():
                parts = line.split()
                if(len(parts) != 2):
                    sys.stderr.write("Invalid format in records.txt. Deleting the contents.\n")
                    return money, records
                
                description, value = parts
                try: value = int(value)
                except ValueError:
                    sys.stderr.write("Invalid amount in records.txt. Deleting the contents.\n")
                    return money, records
                records.append(f"{description} {value}")
            print("Welcome back!")
            return money, records
    
    except FileNotFoundError:
        try: money = int(input("How much money do you have? "))
        except ValueError: sys.stderr.write("Invalid value for money. Set to 0 by default.\n\n")
        return money, records
    
money, records = load_records()
commands = "Hello, World!"
while(True):
    command = input("What do you want to do (add / view / delete / exit)? ")
    
    # Exit
    if(command == "exit"):
        with open(RECORD_FILE, 'w') as f:
            f.write(f"{money}\n")
            f.writelines(r + '\n' for r in records)
        break

    # Add
    elif(command == "add"):
        add_input = list(input("Add some expense or income records with description and amount:\ndesc1 amt1, desc2 amt2, desc3 amt3, ...\n").split(", "))
        try:
            if not add_input: raise ValueError("The format of a record should be like this: breakfast -50.\n")
            elif any(len(a.split()) != 2 for a in add_input): raise ValueError("The format of a record should be like this: breakfast -50.\n")
            elif any(not a.rsplit(" ", 1)[1].lstrip("+-").isdigit() for a in add_input):
                print("Invalid value for money.")
                print("Fail to add a record.\n")
            else:
                for a in add_input: money += int(a.split()[1])
                records.extend(add_input)
                print()
        except:
            print("The format of a record should be like this: breakfast -50.")
            print("Fail to add a record.\n")
    
    # View
    elif(command == "view"):
        print("Description    Amount")
        print("==================== ======")
        for r in records:
            description, value = r.split()
            print("%-15s%s" % (description, value))
        print("==================== ======")
        print(f"Now you have {money} dollars.\n")

    # Delete
    elif(command == "delete"):
        if not records: print("No records to delete.")
        else:
            del_input = input("Which record do you want to delete? ")
            try:
                if not del_input: raise ValueError("The format of a record should be like this: breakfast -50.\n")
                elif any(len(a.split()) != 2 for a in add_input): raise ValueError("The format of a record should be like this: breakfast -50.\n")
                elif (del_input not in records): print(f"There's no record with {del_input}. Fail to delete a record.\n")
                else:
                    idx = len(records) - 1 - records[::-1].index(del_input)
                    if(idx == -1 or idx == len(records)): continue
                    money -= int(records[idx].split()[1])
                    records.pop(idx)
                    print()
            except: print("The format of a record should be like this: breakfast -50.\n")

    # Invalid command
    else: print("Invalid command. Try again.\n")



money = int(input("How much money do you have? "))
records = []

while(True):
    command = input("What do you want to do (add / view / delete / exit)? ")
    # Exit
    if(command == "exit"): break

    # Add
    elif(command == "add"):
        add_input = list(input("Add some expense or income records with description and amount:\ndesc1 amt1, desc2 amt2, desc3 amt3, ...\n").split(", "))
        for a in add_input: money += int(a.split()[1])
        records.extend(add_input)
        print()

    # View
    elif(command == "view"):
        print("Description    Amount")
        print("==================== ======")
        for r in records:
            description, value = r.split()
            print("%-15s%s" % (description, value))
        print("==================== ======")
        print(f"Now you have {money} dollars.\n")

    # Delete
    elif(command == "delete"):
        del_input = input("Which record do you want to delete? ")
        idx = len(records) - 1 - records[::-1].index(del_input)
        if(idx == -1 or idx == len(records)): continue
        money -= int(records[idx].split()[1])
        records.pop(idx)
        print()



money = int(input("How much money do you have? "))
records = list(input("Add some expense or income records with description and amount:\ndesc1 amt1, desc2 amt2, desc3 amt3, ...\n").split(", "))

print("Here's your expenses and income records:")
for p in records: print(p)

for r in records: money += int(r.split()[1])
print(f"Now you have {money} dollars.")