import time


class Dish:

    def __init__(self, driver, dish_config):

        self.driver = driver
        self.dish_config = dish_config

    def get_dishes(self, ctg, all_dishes_url):

        try:
            category = ctg.text
            print('+++++getting deishes',category)

            ctg.click()
            time.sleep(2)
            CONTAINER = {
                    'FIND_BY': self.dish_config['SELECTORS']['CONTAINER']['FIND_BY'],
                    'VALUE' : self.dish_config['SELECTORS']['CONTAINER']['VALUE']
                }
            DATA = {
                    'FIND_BY': self.dish_config['SELECTORS']['DATA']['FIND_BY'],
                    'VALUE' : self.dish_config['SELECTORS']['DATA']['VALUE']
                }

            if CONTAINER['FIND_BY'] == 'class':
                container = self.driver.find_element_by_class_name(CONTAINER['VALUE'])
            elif CONTAINER['FIND_BY'] == 'id':
                container = self.driver.find_element_by_id(CONTAINER['VALUE'])
            elif CONTAINER['FIND_BY'] == 'tag':
                container = self.driver.find_element_by_tag_name(CONTAINER['VALUE'])

            if DATA['FIND_BY'] == 'class':
                data = container.find_elements_by_class_name(DATA['VALUE'])
            elif DATA['FIND_BY'] == 'id':
                data = container.find_element_by_id(DATA['VALUE'])
            elif DATA['FIND_BY'] == 'tag':
                data = container.find_elements_by_tag_name(DATA['VALUE'])


            PRODUCT_LINK = {
                'FIND_BY': self.dish_config['SELECTORS']['PRODUCT_LINK']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['PRODUCT_LINK']['VALUE']
            }
            
            

            for product in data:

                if PRODUCT_LINK['FIND_BY'] == 'class':
                    url = product.find_element_by_class_name(PRODUCT_LINK['VALUE']).get_attribute('href')
                elif PRODUCT_LINK['FIND_BY'] == 'id':
                    url = product.find_element_by_id(PRODUCT_LINK['VALUE']).get_attribute('href')
                elif PRODUCT_LINK['FIND_BY'] == 'tag':
                    url = product.find_element_by_tag_name(PRODUCT_LINK['VALUE']).get_attribute('href')

                print('+++++++++url',url)
                all_dishes_url.append(url)
        except Exception as e:
            print('++++Exception while getting dishes',e)
