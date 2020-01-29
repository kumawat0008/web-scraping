from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Pizzas:

    def __init__(self, driver, dish_config):
        
        self.driver = driver
        self.dish_config = dish_config

    def get_pizzas(self,category,url,restaurant_obj):

        try:
            self.driver.get(url)
            print('+++++++HERE',category)
            
            FIND_BY = self.dish_config['SELECTORS']['WAIT']['FIND_BY']
            VALUE = self.dish_config['SELECTORS']['WAIT']['VALUE']

            if FIND_BY == 'class':
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, VALUE))
                )
            elif FIND_BY == 'id':
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, VALUE))
                )
            elif FIND_BY == 'tag':
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.TAG_NAME, VALUE))
                )
            # element = WebDriverWait(driver, 10).until(
            #         EC.visibility_of_element_located((By.CLASS_NAME, "m-container"))
            #     )
            CONTAINER = {
                'FIND_BY': self.dish_config['SELECTORS']['CONTAINER']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['CONTAINER']['VALUE']
            }
            PRODUCTS = {
                    'FIND_BY': self.dish_config['SELECTORS']['PRODUCTS']['FIND_BY'],
                    'VALUE' : self.dish_config['SELECTORS']['PRODUCTS']['VALUE']
                }

            if CONTAINER['FIND_BY'] == 'class':
                container = self.driver.find_element_by_class_name(CONTAINER['VALUE'])
            elif CONTAINER['FIND_BY'] == 'id':
                container = self.driver.find_element_by_id(CONTAINER['VALUE'])
            elif CONTAINER['FIND_BY'] == 'tag':
                container = self.driver.find_element_by_tag_name(CONTAINER['VALUE'])

            # container = driver.find_element_by_class_name('m-container')
            # container2 = container.find_elements_by_tag_name('ion-grid')[-1]

            if PRODUCTS['FIND_BY'] == 'class':
                products = container.find_elements_by_class_name(PRODUCTS['VALUE'])
            elif PRODUCTS['FIND_BY'] == 'id':
                products = container.find_element_by_id(PRODUCTS['VALUE'])
            elif PRODUCTS['FIND_BY'] == 'tag':
                products = container.find_elements_by_tag_name(PRODUCTS['VALUE'])
            
            # products = container2.find_elements_by_tag_name('ion-col')

            NAME = {
                'FIND_BY': self.dish_config['SELECTORS']['NAME']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['NAME']['VALUE']
            }

            # PRICE = {
            #     'FIND_BY': self.dish_config['SELECTORS']['PRICE']['FIND_BY'],
            #     'VALUE' : self.dish_config['SELECTORS']['PRICE']['VALUE']
            # }
            IMAGE = {
                'FIND_BY': self.dish_config['SELECTORS']['IMAGE']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['IMAGE']['VALUE'],
                'ATTRIBUTE': self.dish_config['SELECTORS']['IMAGE']['ATTRIBUTE']
            }
            DESCRIPTION = {
                'FIND_BY': self.dish_config['SELECTORS']['DESCRIPTION']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['DESCRIPTION']['VALUE']
            }
            # SIZE = {
            #     'FIND_BY': self.dish_config['SELECTORS']['SIZE']['FIND_BY'],
            #     'VALUE' : self.dish_config['SELECTORS']['SIZE']['VALUE']
            # }
            
            for product in products:
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

                # if PRICE['FIND_BY'] == 'class':
                #     price = product.find_element_by_class_name(PRICE['VALUE']).text
                # elif PRICE['FIND_BY'] == 'id':
                #     price = product.find_element_by_id(PRICE['VALUE']).text
                # elif PRICE['FIND_BY'] == 'tag':
                #     price = product.find_element_by_tag_name(PRICE['VALUE']).text
                price = None

                try:
                    if DESCRIPTION['FIND_BY'] == 'class':
                        desc = product.find_element_by_class_name(DESCRIPTION['VALUE']).text
                    elif DESCRIPTION['FIND_BY'] == 'id':
                        desc = product.find_element_by_id(DESCRIPTION['VALUE']).text
                    elif DESCRIPTION['FIND_BY'] == 'tag':
                        desc = product.find_element_by_tag_name(DESCRIPTION['VALUE']).text
                except:
                    desc = None
                # try:
                #     if SIZE['FIND_BY'] == 'class':
                #         size = product.find_element_by_class_name(SIZE['VALUE']).text.split('|')[0]
                #     elif SIZE['FIND_BY'] == 'id':
                #         size = product.find_element_by_id(SIZE['VALUE']).text.split('|')[0]
                #     elif SIZE['FIND_BY'] == 'tag':
                #         size = product.find_element_by_tag_name(SIZE['VALUE']).text.split('|')[0]
                # except:
                #     size = None

                dish_obj = {
                    'name':name,
                    'price':price,
                    'image': image,
                    'category':category,
                    'description':desc
                }
                restaurant_obj['dishes'].append(dish_obj)
                # print('+++++++',image,name,price,size,desc)

        except Exception as e:
            print('+++++++Exception while getting dishes',e)
        
        

    
