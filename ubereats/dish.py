import time, threading
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Dish:

    def __init__(self, dish_config):
        self.dish_config = dish_config

    def get_dishes(self,driver):
        print('+++++++inside dish')

        all_dishes = []

        FIND_BY = self.dish_config['SELECTORS']['DISHESH']['FIND_BY']
        VALUE = self.dish_config['SELECTORS']['DISHESH']['VALUE']
        if FIND_BY == 'css':
            dishes = driver.find_elements_by_css_selector(VALUE)
        elif FIND_BY == 'class':
            dishes = driver.find_elements_by_class_name(VALUE)

        for dish in dishes:
            try:
                FIND_BY = self.dish_config['SELECTORS']['NAME']['FIND_BY']
                VALUE = self.dish_config['SELECTORS']['NAME']['VALUE']
                if FIND_BY == 'css':
                    name = dish.find_element_by_css_selector(VALUE).get_attribute('textContent')
                elif FIND_BY == 'class':
                    name = dish.find_element_by_class_name(VALUE).get_attribute('textContent')
            except Exception as e:
                name = None
            try:
                FIND_BY = self.dish_config['SELECTORS']['PRICE']['FIND_BY']
                VALUE = self.dish_config['SELECTORS']['PRICE']['VALUE']
                if FIND_BY == 'css':
                    price = dish.find_element_by_css_selector(VALUE).get_attribute('textContent')
                elif FIND_BY == 'class':
                    price = dish.find_element_by_class_name(VALUE).get_attribute('textContent')
            except Exception as e:
                price = None

            try:
                image = dish.find_element_by_tag_name('img').get_attribute('src')
            except Exception as e:
                print('+++++++exec in image',e)
                image = None


            try:
                FIND_BY = self.dish_config['SELECTORS']['DESC']['FIND_BY']
                VALUE = self.dish_config['SELECTORS']['DESC']['VALUE']
                if FIND_BY == 'css':
                    desc = dish.find_element_by_css_selector(VALUE).get_attribute('textContent')
                elif FIND_BY == 'class':
                    desc = dish.find_element_by_class_name(VALUE).get_attribute('textContent')
            except Exception as e:
                desc = None 
            dish_obj = {
                                'name': name,
                                'price': price,
                                'description': desc,
                                'image' : image
                            }
            print('++++++dish added')
            all_dishes.append(dish_obj)

        return all_dishes



        