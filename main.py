from database import FoodDatabase, FoodData
from foodfacts_data import FoodFactsData
import datetime
fd = FoodDatabase()
factsdata = FoodFactsData()

def main_add_item():
    barcode = input('Please scan the item: ')
    amount = input('How much do you want to add (number of items): ')
    factsdata.add_entry(barcode, amount)
    print('Entry added.')

def main_remove_item():
    barcode = input('Please scan the item: ')
    fd.remove_item(barcode)
    print('Item removed.')

def main_check_item():
    barcode = input('Please scan the item: ')
    item = fd.retrieve_item(barcode)
    print(item)
    print('Item retrieved.')

def main_update_quantity():
    barcode = int(input('Please scan the item: '))
    amount_change = float(input('Enter the amount to add/remove (+/-): '))
    fd.update_amount(barcode, amount_change)
    print('Amount updated.')

def main_list_all():
    print(fd.get_all_items())
    print('Listing complete')

def main_menu():
    print('Food Organiser Command Line')
    print('Options:')
    print('1: Add an item')
    print('2: Remove whole item')
    print('3: Check an item')
    print('4: Update item quantity')
    print('5: List all items')
    selection = int(input('Please make your selection: '))
    if selection == 1:
        main_add_item()
    elif selection == 2:
        main_remove_item()
    elif selection == 3:
        main_check_item()
    elif selection == 4:
        main_update_quantity()
    elif selection == 5:
        main_list_all()
    else:
        print('Invalid selection.')

while True:
    main_menu()

