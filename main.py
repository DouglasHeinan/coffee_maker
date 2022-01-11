from coffeeResources import MENU, resources


def main():
    # This function serves up virtual coffee until the machine runs out of resources.
    water = resources["water"]
    milk = resources['milk']
    coffee = resources['coffee']
    espresso = MENU['espresso']
    latte = MENU['latte']
    cappuccino = MENU['cappuccino']
    money = 0
    print("Welcome to Java-matic 3000.")
    while True:
        if water < 50 or coffee < 18:
            print("Out of order. Please contact maintenance department.")
            return
        drink = prompt()
        if drink == "":
            print("Come again!")
            return
        selection = key_word_convert(drink, espresso, latte, cappuccino)
        if selection == 'report':
            report(water, milk, coffee, money)
        else:
            enough_ingredients = confirm_selection(drink)
            if enough_ingredients:
                money_paid = payment(selection, drink)
                if money_paid == 0:
                    print("Come again!")
                    return
                change(selection, money_paid)
                money += selection['cost']
                water, milk, coffee = make_drink(drink, selection, water, milk, coffee)


def prompt():
    # The prompt() function takes an order, verifies that it's actually on the menu,
    # and returns it as a string to main().
    drink = input("What would you like? Espresso, latte, or cappuccino (for maintenance mode, enter 'report'. "
                  "To cancel your order, hit 'enter.): ").lower()
    while drink != "espresso" and drink != "latte" and drink != "cappuccino" and drink != "report" and drink != "":
        print("Please order from the menu.")
        drink = input("What would you like? Espresso, latte, or cappuccino (for maintenance mode, enter 'report'): ").lower()
    return drink


def key_word_convert(selection, espresso, latte, cappuccino):
    # This function converts the selection from prompt() into the appropriate key word. If selection == 'report',
    # it is left unconverted.
    if selection == "espresso":
        selection = espresso
    if selection == "latte":
        selection = latte
    if selection == "cappuccino":
        selection = cappuccino
    return selection


def report(water, milk, coffee, money):
    # If the user selected 'report' as their selection, this function will tell them how many of
    # each resource they have left.
    print(f"Water: {water}ml")
    print(f"Milk: {milk}ml")
    print(f"Coffee: {coffee}ml")
    print(f"Money: ${'{:.2f}'.format(money)}")


def confirm_selection(drink):
    # This function confirms that there are enough resources to make the drink the user has selected.
    for key in MENU[drink]['ingredients']:
        if resources[key] >= MENU[drink]['ingredients'][key]:
            return True
        else:
            print(f"Not enough {key}. Contact maintenance department.")
            return False


def payment(selection, drink):
    # This function will calculate the amount of money the user inputs and confirm that it's enough to pay for the
    # drink they selected.
    total = 0
    cancel = 0
    while total < selection['cost'] and cancel != 'Y':
        print(f"Your {drink} costs ${'{:.2f}'.format(selection['cost'])}.")
        quarters = input("How many quarters? ")
        quarters = check_change(quarters)
        dimes = input("How many dimes? ")
        dimes = check_change(dimes)
        nickles = input("How many nickles? ")
        nickles = check_change(nickles)
        pennies = input("How many pennies? ")
        pennies = check_change(pennies)
        total = add_up_money(quarters, dimes, nickles, pennies)
        if total < selection['cost']:
            print(f"That's only ${total}!")
            cancel = input("Did you want to cancel your order? (Press 'Y' to cancel). ").upper()
            if cancel == "Y":
                total = 0
    return total


def check_change(money):
    # This function runs after each monetary input from the user in payment() to confirm that the input is a number.
    while not money.isdigit():
        money = input("Please enter actual money: ")
    return int(money)


def add_up_money(quarters, dimes, nickles, pennies):
    # After the user enters all their coin quantities in payment(), their total amount paid is calculated here.
    total = ((quarters * 25) + (dimes * 10) + (nickles * 5) + pennies) / 100
    return total


def change(selection, money_paid):
    # This calculates how much change is given back to the user, if any.
    change_back = money_paid - selection['cost']
    if change_back > 0:
        print(f"Here is your ${'{:.2f}'.format(change_back)} change")
    else:
        print("Thank you for exact change!")


def make_drink(drink, selection, water, milk, coffee):
    # If the user is paid up and there are sufficient resources to make their ordered drink, this function will reduce
    # the resources stored in the machine by the necessary amount for the drink being made and inform the user that
    # their drink is their's now.
    water -= selection['ingredients']['water']
    milk -= selection['ingredients']['milk']
    coffee -= selection['ingredients']['coffee']
    print(f"Here is your {drink}. Enjoy!")
    return water, milk, coffee


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
