from database import FoodDatabase, FoodData
from foodfacts_data import FoodFactsData
import datetime
fd = FoodDatabase()
factsdata = FoodFactsData()

item_to_add = FoodData(20303, datetime.datetime(2020, 1, 22), 'Test Item', '300g', 1, 'http://test.com')

fd.add_item(item_to_add)
print(fd.check_if_exists(20303))
print(fd.check_if_exists(101))
print(fd.retrieve_item(20303))
fd.update_amount(20303, -0.54)
print(fd.retrieve_item(20303))
fd.remove_item(20303)
print(fd.check_if_exists(20303))
print(fd.check_if_exists(101))

while True:
    barcode = int(input('Enter the barcode: '))
    print(barcode)
    factsdata.add_entry(barcode, 1)
    print(fd.check_if_exists(barcode))
    print(fd.retrieve_item(barcode))  