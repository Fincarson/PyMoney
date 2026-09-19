import sys
RECORD_FILE = 'records.txt'

class Record:
    def __init__(self, category, description, amount):
        self._category = category
        self._description = description
        self._amount = amount

    @property
    def category(self): return self._category

    @property
    def description(self): return self._description

    @property
    def amount(self): return self._amount

    def __str__(self): return f"{self._category} {self._description} {self._amount}"


class Records:
    # INIT
    def __init__(self):
        self._records = []
        self._initial_money = 0

        try:
            with open(RECORD_FILE, 'r') as f:
                try: self._initial_money = int(f.readline().strip())
                except ValueError:
                    sys.stderr.write(f"Invalid format in {RECORD_FILE}. Deleting contents.\n")
                    return

                for line in f.readlines():
                    parts = line.split()
                    if len(parts) != 3:
                        sys.stderr.write(f"Invalid format in {RECORD_FILE}. Deleting contents.\n")
                        self._records = []
                        return

                    cat, desc, val = parts
                    try: val = int(val)
                    except ValueError:
                        sys.stderr.write(f"Invalid value in {RECORD_FILE}. Deleting contents.\n")
                        self._records = []
                        return

                    self._records.append(Record(cat, desc, val))
                print("Welcome back!")

        except FileNotFoundError:
            try: self._initial_money = int(input("How much money do you have? "))
            except ValueError:
                sys.stderr.write("Invalid value for money. Set to 0 by default.\n\n")
                self._initial_money = 0

    # ADD
    def add(self, raw_input, categories):
        entries = [x.strip() for x in raw_input.split(",")]

        for entry in entries:
            parts = entry.split()
            if len(parts) != 3:
                print("The format should be: meal breakfast -50")
                print("Fail to add a record.\n")
                return

            cat, desc, val = parts

            if not val.lstrip("+-").isdigit():
                print("Invalid amount.")
                print("Fail to add a record.\n")
                return

            if not categories.is_category_valid(cat):
                print("The specified category is not in the category list.")
                print('You can check the category list by command "view categories".')
                print("Fail to add a record.\n")
                return

        for entry in entries:
            cat, desc, val = entry.split()
            val = int(val)
            self._initial_money += val
            self._records.append(Record(cat, desc, val))
        print()

    # VIEW
    def view(self):
        print("Here's your expense and income records:")
        print(f"{'Category':15s} {'Description':20s} {'Amount':>6s}")
        print(("="*15) + " " + ("="*20) + " " + ("="*6))
        for r in self._records:print(f"{r.category:15s} {r.description:20s} {r.amount:>6d}")
        print("=" * 43)
        print(f"Now you have {self._initial_money} dollars.\n")

    # DELETE
    def delete(self, record_str):
        parts = record_str.split()
        if len(parts) != 3:
            print("The format should be: meal breakfast -50.\n")
            return

        cat, desc, val = parts

        for i in range(len(self._records) - 1, -1, -1):
            r = self._records[i]
            if r.category == cat and r.description == desc and str(r.amount) == val:
                self._initial_money -= r.amount
                self._records.pop(i)
                print()
                return
        print(f"There's no record with {record_str}. Fail to delete.\n")

    # FIND
    def find(self, subcategories):
        print(f"Here's your expense and income records under category \"{subcategories[0]}\":")
        print(f"{'Category':15s} {'Description':20s} {'Amount':>6s}")
        print(("="*15) + " " + ("="*20) + " " + ("="*6))

        total = 0
        for r in self._records:
            if r.category in subcategories:
                print(f"{r.category:15s} {r.description:20s} {r.amount:>6d}")
                total += r.amount

        print("=" * 43)
        print(f"The total amount above is {total}.\n")

    # SAVE
    def save(self):
        with open(RECORD_FILE, 'w') as f:
            f.write(f"{self._initial_money}\n")
            for r in self._records:
                f.write(str(r) + "\n")



class Categories:
    # INIT
    def __init__(self):
        self._categories = [
            "expense",
            [
                "food",
                    [
                        "meal",
                        "snack",
                        "drink"
                    ],
                "transport",
                    [
                        "bus",
                        "railway"
                    ]
            ],
            "income",
            [
                "salary",
                "bonus"
            ]
        ]

    # VIEW
    def view(self, categories=None, level=0):
        if categories is None:
            categories = self._categories

        for item in categories:
            if isinstance(item, list):
                self.view(item, level + 1)
            else:
                print("  " * level + "- " + item)

    # IS VALID
    def is_category_valid(self, category, categories=None):
        if categories is None:
            categories = self._categories

        for item in categories:
            if isinstance(item, list):
                if self.is_category_valid(category, item):
                    return True
            else:
                if item == category:
                    return True

        return False

    # FIND
    def find_subcategories(self, category):
        def find_subcategories_gen(category, categories, found=False):
            if isinstance(categories, list):
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if (child == category and index + 1 < len(categories) and isinstance(categories[index + 1], list)):
                        yield from find_subcategories_gen(category,categories[index + 1], True)
            else:
                if categories == category or found: yield categories
        return list(find_subcategories_gen(category, self._categories))


# MAIN
categories = Categories()
records = Records()

while True:
    command = input("\nWhat do you want to do (add / view / delete / view categories / find / exit)? ")
    if command == 'add':
        record_str = input("Add records (cat desc amount), separated by commas:\ncat1 desc1 amt1, cat2 desc2 amt2, ...\n")
        records.add(record_str, categories)

    elif command == 'view':
        records.view()

    elif command == 'delete':
        delete_str = input("Which record do you want to delete? ")
        records.delete(delete_str)

    elif command == 'view categories':
        categories.view()

    elif command == 'find':
        cat = input("Which category do you want to find? ")
        subcats = categories.find_subcategories(cat)
        if not subcats: print(f'No such category "{cat}". Check with "view categories".\n')
        else: records.find(subcats)

    elif command == 'exit':
        records.save()
        break

    else: sys.stderr.write("Invalid command. Try again.\n")