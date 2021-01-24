class FoodFactsData:
    import openfoodfacts as of
    from database import FoodDatabase, FoodData
    from datetime import datetime
    fd = FoodDatabase()

    def download_product_image(self, barcode: int, url: str):
        '''Download product images to the image cache

        Parameters:
        barcode (int): Barcode to add
        url (str): URL of image
        '''
        from os import path, mkdir
        # Check that the img_cache folder exists, if not - create it
        if not path.exists('img_cache'):
            mkdir('img_cache')
        # Check that an image does not already exist with the barcode name
        image_path = 'img_cache/' + str(barcode) + '.jpg'
        # If the image already exists, then don't download it again.
        if path.exists(image_path):
            print('Image already exists')
        else:
            import requests
            img = requests.get(url, allow_redirects=True)
            open(image_path, 'wb').write(img.content)

    def add_entry(self, barcode: int, amount: float):
        '''Download product images to the image cache

        Parameters:
        barcode (int): Barcode to add
        amount (float): Amount to add
        '''
        current_time = self.datetime.now()
        new_entry = self.FoodData(barcode, current_time, '', '', amount, '')
        # Firstly, check whether an entry already exists under that barcode
        if self.fd.check_if_exists(barcode):
            print('Entry already exists')
            self.fd.update_amount(barcode, float) # Add to the current entry
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
                    # Download the image if the URL exists
                    self.download_product_image(barcode, new_entry.img_url)
                except KeyError:
                    pass
                

            # Add the newly created entry into the database
            self.fd.add_item(new_entry)

   
        

        