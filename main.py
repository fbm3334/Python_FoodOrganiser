from database import FoodDatabase, FoodData
import datetime
fd = FoodDatabase()

item_to_add = FoodData(20303, datetime.datetime(2020, 1, 22), 'Test Item', '300g', 1, 'http://test.com')

fd.add_item(item_to_add)