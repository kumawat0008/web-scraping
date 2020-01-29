import time, threading,datetime
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from decimal import Decimal

class Restaurant:

    def __init__(self,dish_config,restaurant_config,dishes_data,city_code,country,city):
        self.dish_config = dish_config
        self.dishes_data = dishes_data
        self.restaurant_config = restaurant_config
        self.city = city
        self.city_code = city_code
        self.country = country

    def get_restaurant(self, driver,rest_obj,dish_obj):

        print('+++++++inside restaurant')

        driver.get(rest_obj['url'])
        # time.sleep(3)

        FIND_BY = self.restaurant_config['SELECTORS']['WAIT']['FIND_BY']
        VALUE = self.restaurant_config['SELECTORS']['WAIT']['VALUE']

        if FIND_BY == 'class':
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, VALUE))
            )
        elif FIND_BY == 'id':
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, VALUE))
            )
        elif FIND_BY == 'tag':
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.TAG_NAME, VALUE))
            )

        elif FIND_BY == 'css':
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, VALUE))
            )

       
        opens_at = None

        SUBZONE = {
            'FIND_BY': self.restaurant_config['SELECTORS']['SUBZONE']['FIND_BY'],
            'VALUE':self.restaurant_config['SELECTORS']['SUBZONE']['VALUE']
        }

        try:
            if SUBZONE['FIND_BY'] == 'css':
                subzone = driver.find_element_by_css_selector(SUBZONE['VALUE']).get_attribute('textContent').split('Bengaluru')[0].split(',')[-2]
            elif SUBZONE['FIND_BY'] == 'class':
                subzone = driver.find_element_by_class_name(SUBZONE['VALUE']).get_attribute('textContent').split('Bengaluru')[0].split(',')[-2]
        except Exception as e:
            print('+++exc in subzone',e)
            subzone = 'General'


        
        restaurant_obj = {
                'city_code': self.city_code,
                'name': rest_obj['name'],
                'type': rest_obj['type'],
                'url': rest_obj['url'],
                'stars': rest_obj['stars'],
                'ratings': rest_obj['ratings'],
                'image': None,
                'opens_at': opens_at,
                'country': self.country,
                'subzone' : 'General',
                'city':self.city,
                'platform':'UBEREATS',
                'dishes':[],
                'added_on': str(datetime.datetime.utcnow())
                }
        sort_key_info = restaurant_obj['platform']+'__'+restaurant_obj['subzone']+'__'+restaurant_obj['name'].strip().replace(' ','_')
        restaurant_obj['sort_key_info'] = sort_key_info
        restaurant_dishes = dish_obj.get_dishes(driver)
        restaurant_obj['dishes'] = restaurant_dishes
        # print('+++++++rest obj',restaurant_obj)
        self.dishes_data.append(restaurant_obj)
            