import time


class Dish:
    
    def __init__(self, driver, dish_config):

        self.driver = driver
        self.dish_config = dish_config

    def get_dishes(self, ctg,restaurant_obj):

        try:
            print('+++++getting deishes',ctg.text)
            anchor_tag = ctg.find_element_by_tag_name('a')
            id = anchor_tag.get_attribute('id').split('-')[-1]
            category = ctg.text.strip().split('\n')[0]

            CONTAINER = {
                    'FIND_BY': self.dish_config['SELECTORS']['CONTAINER']['FIND_BY'],
                    'VALUE' : self.dish_config['SELECTORS']['CONTAINER']['VALUE']
                }

            DATA = {
                    'FIND_BY': self.dish_config['SELECTORS']['DATA']['FIND_BY'],
                    'VALUE' : self.dish_config['SELECTORS']['DATA']['VALUE']
                }

            container_id = CONTAINER['VALUE']+id
            ctg.click()
            time.sleep(1)
            if CONTAINER['FIND_BY'] == 'class':
                container = self.driver.find_element_by_class_name(container_id)
            elif CONTAINER['FIND_BY'] == 'id':
                container = self.driver.find_element_by_id(container_id)
            elif CONTAINER['FIND_BY'] == 'tag':
                container = self.driver.find_element_by_tag_name(container_id)
            

            if DATA['FIND_BY'] == 'class':
                data = container.find_elements_by_class_name(DATA['VALUE'])
            elif DATA['FIND_BY'] == 'id':
                data = container.find_element_by_id(DATA['VALUE'])
            elif DATA['FIND_BY'] == 'tag':
                data = container.find_elements_by_tag_name(DATA['VALUE'])

            NAME = {
                'FIND_BY': self.dish_config['SELECTORS']['NAME']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['NAME']['VALUE']
            }
            PRICE = {
                'FIND_BY': self.dish_config['SELECTORS']['PRICE']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['PRICE']['VALUE']
            }
            BOX8_USER_PRICE = {
                'FIND_BY': self.dish_config['SELECTORS']['BOX8_USER_PRICE']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['BOX8_USER_PRICE']['VALUE']
            }
            DESCRIPTION = {
                'FIND_BY': self.dish_config['SELECTORS']['DESCRIPTION']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['DESCRIPTION']['VALUE']
            }
            IMAGE = {
                'FIND_BY': self.dish_config['SELECTORS']['IMAGE']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['IMAGE']['VALUE'],
                'ATTRIBUTE': self.dish_config['SELECTORS']['IMAGE']['ATTRIBUTE']
            }

            
            for product in data:

                try:
                    if IMAGE['FIND_BY'] == 'class':
                        image = product.find_element_by_class_name(IMAGE['VALUE']).get_attribute(IMAGE['ATTRIBUTE'])
                    elif IMAGE['FIND_BY'] == 'id':
                        image = product.find_element_by_id(IMAGE['VALUE']).get_attribute(IMAGE['ATTRIBUTE'])
                    elif IMAGE['FIND_BY'] == 'tag':
                        image = product.find_element_by_tag_name(IMAGE['VALUE']).get_attribute(IMAGE['ATTRIBUTE'])
                except:
                    image = None

                if NAME['FIND_BY'] == 'class':
                    name = product.find_element_by_class_name(NAME['VALUE']).text
                elif NAME['FIND_BY'] == 'id':
                    name = product.find_element_by_id(NAME['VALUE']).text
                elif NAME['FIND_BY'] == 'tag':
                    name = product.find_element_by_tag_name(NAME['VALUE']).text

                # name = product.find_element_by_class_name('product-label').text

                if PRICE['FIND_BY'] == 'class':
                    price = product.find_element_by_class_name(PRICE['VALUE']).text.strip().split('\n')[0]
                elif PRICE['FIND_BY'] == 'id':
                    price = product.find_element_by_id(PRICE['VALUE']).text.strip().split('\n')[0]
                elif PRICE['FIND_BY'] == 'tag':
                    price = product.find_element_by_tag_name(PRICE['VALUE']).text.strip().split('\n')[0]

                try:
                    if DESCRIPTION['FIND_BY'] == 'class':
                        desc = product.find_element_by_class_name(DESCRIPTION['VALUE']).text
                    elif DESCRIPTION['FIND_BY'] == 'id':
                        desc = product.find_element_by_id(DESCRIPTION['VALUE']).text
                    elif DESCRIPTION['FIND_BY'] == 'tag':
                        desc = product.find_element_by_tag_name(DESCRIPTION['VALUE']).text
                    # desc = product.find_element_by_class_name('product-description').text
                except:
                    desc = None
                # price = product.find_element_by_class_name('prices-wrapper').text.strip().split('\n')[0]
                try:
                    if BOX8_USER_PRICE['FIND_BY'] == 'class':
                        box8_user_price = product.find_element_by_class_name(BOX8_USER_PRICE['VALUE']).text
                    elif BOX8_USER_PRICE['FIND_BY'] == 'id':
                        box8_user_price = product.find_element_by_id(BOX8_USER_PRICE['VALUE']).text
                    elif BOX8_USER_PRICE['FIND_BY'] == 'tag':
                        box8_user_price = product.find_element_by_tag_name(BOX8_USER_PRICE['VALUE']).text
                    # box8_user_price = product.find_element_by_class_name('product-pass-band-price').text
                except:
                    box8_user_price = price

                dish_obj = {
                    'name':name,
                    'price':price,
                    'box8_user_price':box8_user_price,
                    'image': image,
                    'category':category,
                    'description':desc
                }
                restaurant_obj['dishes'].append(dish_obj)

        except Exception as e:
            print('++++Exception while getting dishes')