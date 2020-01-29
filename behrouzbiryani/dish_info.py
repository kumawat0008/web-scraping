class DishInfo:

    def __init__(self, driver, dish_config):
        
        self.driver = driver
        self.dish_config = dish_config

    def get_dish_info(self, url, restaurant_obj):

        try:
            print('++++++++getting dish info')
            self.driver.get(url)

            PRODUCT_CONTAINER = {
                'FIND_BY': self.dish_config['SELECTORS']['PRODUCT_CONTAINER']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['PRODUCT_CONTAINER']['VALUE']
            }

            DESCRIPTION = {
                'FIND_BY': self.dish_config['SELECTORS']['DESCRIPTION']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['DESCRIPTION']['VALUE']
            }
            CATEGORY = {
                'FIND_BY': self.dish_config['SELECTORS']['CATEGORY']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['CATEGORY']['VALUE']
            }
            PRICE = {
                'FIND_BY': self.dish_config['SELECTORS']['PRICE']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['PRICE']['VALUE']
            }
            NAME = {
                'FIND_BY': self.dish_config['SELECTORS']['NAME']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['NAME']['VALUE']
            }
            IMAGE = {
                'FIND_BY': self.dish_config['SELECTORS']['IMAGE']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['IMAGE']['VALUE'],
                'ATTRIBUTE': self.dish_config['SELECTORS']['IMAGE']['ATTRIBUTE']
            }

            if PRODUCT_CONTAINER['FIND_BY'] == 'class':
                product_container = self.driver.find_element_by_class_name(PRODUCT_CONTAINER['VALUE'])
            elif PRODUCT_CONTAINER['FIND_BY'] == 'id':
                product_container = self.driver.find_element_by_id(PRODUCT_CONTAINER['VALUE'])
            elif PRODUCT_CONTAINER['FIND_BY'] == 'tag':
                product_container = self.driver.find_element_by_tag_name(PRODUCT_CONTAINER['VALUE'])

            # print('++++++product_conta',product_container.find_element_by_class_name('singleProductSmallDescription').text)
        
            try:
                if DESCRIPTION['FIND_BY'] == 'class':
                    desc = product_container.find_element_by_class_name(DESCRIPTION['VALUE']).text
                elif DESCRIPTION['FIND_BY'] == 'id':
                    desc = product_container.find_element_by_id(DESCRIPTION['VALUE']).text
                elif DESCRIPTION['FIND_BY'] == 'tag':
                    desc = product_container.find_element_by_tag_name(DESCRIPTION['VALUE']).text
            except Exception as e:
                desc = None

            if NAME['FIND_BY'] == 'class':
                name = product_container.find_element_by_class_name(NAME['VALUE']).text
            elif NAME['FIND_BY'] == 'id':
                name = product_container.find_element_by_id(NAME['VALUE']).text
            elif NAME['FIND_BY'] == 'tag':
                name = product_container.find_element_by_tag_name(NAME['VALUE']).text

            if CATEGORY['FIND_BY'] == 'class':
                category = product_container.find_element_by_class_name(CATEGORY['VALUE']).text
            elif CATEGORY['FIND_BY'] == 'id':
                category = product_container.find_element_by_id(CATEGORY['VALUE']).text
            elif CATEGORY['FIND_BY'] == 'tag':
                category = product_container.find_element_by_tag_name(CATEGORY['VALUE']).text

            
            try:
                if PRICE['FIND_BY'] == 'class':
                    price = product_container.find_element_by_class_name(PRICE['VALUE']).text
                elif PRICE['FIND_BY'] == 'id':
                    price = product_container.find_element_by_id(PRICE['VALUE']).text
                elif PRICE['FIND_BY'] == 'tag':
                    price = product_container.find_element_by_tag_name(PRICE['VALUE']).text
            except Exception as e:
                price = None

            try:
                if IMAGE['FIND_BY'] == 'class':
                    image = product_container.find_element_by_class_name(IMAGE['VALUE']).get_attribute(IMAGE['ATTRIBUTE'])
                elif IMAGE['FIND_BY'] == 'id':
                    image = product_container.find_element_by_id(IMAGE['VALUE']).get_attribute(IMAGE['ATTRIBUTE'])
                elif IMAGE['FIND_BY'] == 'tag':
                    image = product_container.find_element_by_tag_name(IMAGE['VALUE']).get_attribute(IMAGE['ATTRIBUTE'])
            except:
                image = None

            dish_obj = {
                'name':name,
                'price':price,
                'image': image,
                'category':category,
                'description':desc
            }
            print('++++++appending dish obj in info')
            restaurant_obj['dishes'].append(dish_obj)

        except Exception as e:
            print('++++++Exception while getting dish info',e)