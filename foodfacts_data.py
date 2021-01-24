class FoodFactsData:
    import openfoodfacts as of
    from database import FoodDatabase, FoodData
    from datetime import datetime
    fd = FoodDatabase()

    def add_entry(self, barcode: int, amount: float):
        current_time = self.datetime.now()
        new_entry = self.FoodData(barcode, current_time, '', '', amount, '')
        # Firstly, check whether an entry already exists under that barcode
        if self.fd.check_if_exists(barcode):
            print('Entry already exists')
        else:
            # Get data from OpenFoodFacts
            item = self.of.products.get_product(str(barcode))
            # Check whether the item exists in the OpenFoodFacts database
            if item['status'] == 0:
                new_entry.name = 'Not in OpenFoodFacts database'
                print('The item does not exist in the OpenFoodFacts database.')
            else:
                try:
                    new_entry.name = item['product']['product_name']
                except KeyError:
                    new_entry.name = "Unknown"
                    pass
                try:
                    new_entry.quantity = item['product']['quantity']
                except KeyError:
                    new_entry.quantity = "Unknown"
                    pass
                try:
                    new_entry.img_url = item['product']['image_front_url']
                except KeyError:
                    pass
            
            # Add the newly created entry into the database
            self.fd.add_item(new_entry)

        