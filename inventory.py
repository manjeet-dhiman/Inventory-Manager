# This program is for a Nike warehouse manager that allows them to
# capture, view, edit, search and report on shoe inventory for presentation purposes.

# used to create tables from shoe data
from tabulate import tabulate

# coloured terminal responses
RED = "\033[91m"
GREEN = "\033[32m"
PURPLE = '\033[95m'
# resets colour to default
RESET = "\033[0m"
# create line separators for decoration
SEP = "⎯"


# Classes
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        """Initialise the five attributes.

        Args:
            country (str) = country of origin
            code (str) = 8-digit code
            product (str) = name of shoe
            cost (float) = cost with decimal places
            quantity (int) = number of shoes in a whole number

        """
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def __str__(self):
        """Returns a string representation of the shoe object's attributes."""
        return f"""
Country:\t{self.country}
Code:\t\t{self.code}
Product:\t{self.product}
Cost:\t\t{self.cost}
Quantity:\t{self.quantity}
"""

    def get_cost(self):
        """Returns the cost of a shoe."""
        return self.cost

    def get_quantity(self):
        """Returns the quantity of a shoe."""
        return self.quantity


# The list will be used to store a list of objects of shoes.
shoes_list = []


# Functions outside the class
def read_shoes_data():
    """Reads data from a file and creates Shoe objects for each line of data.

    The data in the file should be in the following format:
    Country, Code, Product, Cost, Quantity
    The created shoe objects are appended to the shoes_list.

    Returns:
        shoe objects appended to the shoes_list.

    Raises:
        FileNotFoundError: If file is not found.
    """
    try:
        # open the file in read mode
        file = open('inventory.txt', 'r')
        # read the first line from the file but do not assign it to any variable, thereby skipping it
        file.readline()

        # loop through each line in the file
        for line in file:
            # strip white space and split the line by commas
            data = line.strip().split(",")

            # assign the indexes in data to each corresponding variable
            country = data[0]
            code = data[1]
            product = data[2]
            cost = data[3]
            quantity = data[4]

            # pass through Shoe class to create object
            shoes = Shoe(country, code, product, cost, quantity)

            # add to shoes_list
            shoes_list.append(shoes)

        # close the file
        file.close()

    # error when inventory.txt not found
    except FileNotFoundError:
        return print(f'''
{RED}inventory.txt does not exist!
Program will not work!
Make sure the text file is in same directory as python file.{RESET}''')


def capture_shoes():
    """Prompts the user to enter the country of origin, shoe code, product name, unit cost, and quantity.

    If an invalid cost or quantity is entered, the user is prompted to re-enter the input.
    The function then creates a new shoe object using the input and appends it to shoes_list.

    Returns:
        Confirmation that new object is added to list + text file
    """
    country = input("What country: ")
    code = input("Enter the shoe code: ")
    product = input("Enter the shoe product: ")
    # loop makes sure that user input is a float, gives error on incorrect entry
    while True:
        try:
            cost = float(input("Enter the shoe unit cost: "))
            break
        except ValueError:
            print(f"{RED}Enter a valid price.{RESET}")
            continue
    # looper makes sure that input is an integer, gives error on incorrect entry
    while True:
        try:
            quantity = int(input("Enter the shoe quantity: "))
            break
        except ValueError:
            print(f"{RED}Enter a whole number.{RESET}")
            continue

    # pass through shoe object
    new_shoe = Shoe(country, code, product, cost, quantity)

    # append object to list
    shoes_list.append(new_shoe)

    # append to text file too
    with open("inventory.txt", "a") as file:
        file.write(f"\n{new_shoe.country},{new_shoe.code},{new_shoe.product},{new_shoe.cost},{new_shoe.quantity}")

    print(f"{GREEN}Product added to inventory list.\n{RESET}")


def view_all():
    """Prints a table of all the shoes in the shoes_list."""
    # headers used for column titles
    headers = ['Country', 'Code', 'Product', 'Cost', 'Quantity']
    table = []

    # iterate through all the shoes in the shoes_list and add their details to the table list.
    for shoe in shoes_list:
        table.append([shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity])

    print(f"\n{PURPLE}{SEP * 29} [Inventory] {SEP * 29}{RESET}")
    # print the table in a fancy grid format using tabulate library
    print(tabulate(table, headers, tablefmt='fancy_grid'))


def re_stock():
    """Finds the shoe(s) with the lowest quantity in the 'shoes_list' and prompts the user to restock those shoes.

    Returns:
        The quantity will be updated in shoes_list and written to the 'inventory.txt' file.

    Raises:
        FileNotFoundError: If file is not found.
    """
    # start lowest_qty at infinity, first item quantity will replace it
    lowest_qty = float('inf')
    shoe_lowest_quantity = []

    # iterate through shoes_list to find the lowest quantity products, passing through shoe object, attach to list
    for shoe in shoes_list:
        # replace lowest_qty if a lower quantity and replace shoe_lowest_quantity list
        if shoe.quantity < lowest_qty:
            lowest_qty = shoe.quantity
            shoe_lowest_quantity = [shoe]
        # add to list if the quantities are equal
        elif shoe.quantity == lowest_qty:
            shoe_lowest_quantity.append(shoe)

    # for each low quantity shoe ask to restock and change in list and text file
    for shoe in shoe_lowest_quantity:
        print(f"{PURPLE}Shoe with the lowest quantity:{RESET} {shoe}")
        # ask user to restock or not, use error handling for negative integers
        while True:
            try:
                add_quantity = int(input(f"Enter the quantity for {shoe.product} to add (type 0 to not restock): "))
                if add_quantity < 0:
                    raise ValueError
                elif add_quantity == 0:
                    print(f"\n{GREEN}Product not restocked.{RESET}")
                    break
                else:
                    break
            except ValueError:
                print(f"{RED}Enter an positive integer for quantity.\n{RESET}")

        # add user input for add_quantity to the original quantity in inventory
        shoe.quantity += add_quantity

        print(f"{GREEN}Quantity for {shoe.product} ({shoe.country}):{RESET} {shoe.quantity}\n")

        # change the quantity to the text file, with error if file doesn't exist
        try:
            with open('inventory.txt', 'w') as file:
                for shoe in shoes_list:
                    file.write(f"\n{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}")

        except FileNotFoundError:
            print(f"{RED}inventory.txt not found. Make sure it is right directory.{RESET}")


def search_shoe():
    """Prompts user to enter a product code and searches through a list of shoes to find a match.

    Returns:
        If a match is found, the information for that shoe is displayed.
        If no match is found, an error message is displayed.
    """
    code = input("Enter the product code: ")

    match_found = False

    # iterate through list and if code matches show information and change match_found to True
    for shoe in shoes_list:
        if shoe.code == code:
            match_found = True
            print(shoe)

    # if match_found stays false after loop, give error message
    if match_found is False:
        print(f"{RED}Product code not found!{RESET}")


def value_per_item():
    """Prints the total value of each shoe in the shoes_list.

    Calculates the total value by multiplying the cost and quantity for each shoe.
    """
    print(f"\n{PURPLE}{SEP * 10} [Total Value For Each Shoe] {SEP * 10}{RESET}")

    headers = ['Country', 'Product', 'Code', 'Total Value']
    table = []

    # iterate through list and use methods from shoe class to calculate value of each product
    for shoe in shoes_list:
        value = (shoe.get_cost()) * (shoe.get_quantity())
        # append total value of each product to table list
        table.append([shoe.country, shoe.product, shoe.code, value])

    # create table using information from headers and table
    print(tabulate(table, headers, tablefmt="fancy_grid"))


def highest_qty():
    """Finds the shoe(s) with the highest quantity in the 'shoes_list' displays to user. Add option to discount."""
    highest_quantity = 0
    shoe_highest_quantity = []

    # iterate through shoes_list finding the highest quantity items, appending to list after passing through object
    for shoe in shoes_list:
        # replace highest_quantity if a higher quantity and replace shoe_highest_quantity list
        if int(shoe.quantity) > highest_quantity:
            highest_quantity = shoe.quantity
            shoe_highest_quantity = [shoe]
        # add to list if the quantities are equal
        elif int(shoe.quantity) == highest_quantity:
            shoe_highest_quantity.append(shoe)

    print(f"\n{PURPLE}Product(s) with the highest quantity for sale:{RESET}")

    # for each shoe that have the same highest quantity
    for shoe in shoe_highest_quantity:
        print(f"{shoe}")
        # ask user to discount or not
        while True:
            change_price = (input(f"Do you want to discount {shoe.product} ({shoe.country}) (Yes/No)? ")).lower()
            if change_price == 'yes':
                # ask user to enter amount to discount, adding error handling if non float entered
                try:
                    discount_price = float(input("Enter amount to discount off shoe: "))
                except ValueError:
                    print("Entry not a valid amount. Please enter a number.")
                    continue

                # reduce the cost by amount user entered
                shoe.cost = shoe.cost - discount_price

                # show confirmation message
                print(f"\n{GREEN}The new price of {shoe.product} ({shoe.country}) is {shoe.cost}.{RESET}")
                break
            
            # if no exit to main menu
            elif change_price == 'no':
                print(f"\n{GREEN}Product not discounted.{RESET}")
                break

            # incorrect entry ask again
            else:
                print(f"{RED}Enter Yes or No.\n{RESET}")
                continue

    # change the cost to the text file, with error if file doesn't exist
    try:
        with open('inventory.txt', 'w') as file:
            for shoe in shoes_list:
                file.write(f"\n{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}")

    except FileNotFoundError:
        print(f"{RED}inventory.txt not found. Make sure it is right directory.{RESET}")

def main():
    # populate shoe_list with inventory.txt
    read_shoes_data()

    # Main menu
    while True:
        menu = input(f"""
{PURPLE}{SEP * 20}[ Inventory Program ]{SEP * 20}{RESET}
Choose the menu option by typing the corresponding letter:
'S'earch  - Search products by code.
'V'iew    - View a list of the inventory.
'A'dd     - Add a product to the inventory.
'L'owest  - Determine the product with the lowest quantity and restock it.
'H'ighest - Determine the product with the highest quantity and discount it.
'T'otal   - Calculate the total value of each stock item.
'E'xit    - Exit program.
{PURPLE}: {RESET}""").lower()

        # search
        if menu == 's':
            search_shoe()
            continue

        # view all inventory
        elif menu == 'v':
            view_all()
            continue

        # add product
        elif menu == 'a':
            capture_shoes()
            continue

        # lowest quantity + restock
        elif menu == 'l':
            re_stock()
            continue

        # highest quantity
        elif menu == 'h':
            highest_qty()
            continue

        # total value of each product
        elif menu == 't':
            value_per_item()
            continue

        # end program
        elif menu == 'e':
            print(f"{GREEN}Goodbye!!!{RESET}")
            exit()

        # incorrect menu entry
        else:
            print(f"{RED}Incorrect choice. Please type a letter corresponding to the option.{RESET}\n")

# run program
main()