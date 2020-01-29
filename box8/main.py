from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
import json
import datetime
from dish import Dish
from decimal import Decimal
from dynamodb_write import DynamoDBWrite
from write_to_s3_parquet import WriteS3Parquet


class Box8:

    def __init__(self,url=None):

        self.CONFIG_FILE = "jwt-config.json"
        with open(self.CONFIG_FILE,'r') as config_file:
            self.data_set = json.load(config_file)
        self.starter_config = self.data_set['BOX8']['CONFIG']['STARTER']
        self.config = self.data_set['BOX8']['CONFIG']
        self.dish_config = self.data_set['BOX8']['CONFIG']['DISH']
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox(options=self.options)
        self.url = self.starter_config["URL"]
        self.city = 'general'
        self.country = 'india'
        self.city_code = self.city+'__'+self.country

    def get_details(self,url):

        try:
            print('+++++getting restro page')
            self.driver.get(self.url)
            try:
                # element = WebDriverWait(driver, 10).until(
                #     EC.visibility_of_element_located((By.CLASS_NAME, "menu-content-wrapper"))
                # )
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

                CTG_NAV = {
                    'FIND_BY': self.dish_config['SELECTORS']['CATEGORY_NAV']['FIND_BY'],
                    'VALUE' : self.dish_config['SELECTORS']['CATEGORY_NAV']['VALUE']
                }
                CATEGORIES = {
                    'FIND_BY': self.dish_config['SELECTORS']['CATEGORIES']['FIND_BY'],
                    'VALUE' : self.dish_config['SELECTORS']['CATEGORIES']['VALUE']
                }

                if CTG_NAV['FIND_BY'] == 'class':
                    ctg_nav = self.driver.find_element_by_class_name(CTG_NAV['VALUE'])
                elif CTG_NAV['FIND_BY'] == 'id':
                    ctg_nav = self.driver.find_element_by_id(CTG_NAV['VALUE'])
                elif CTG_NAV['FIND_BY'] == 'tag':
                    ctg_nav = self.driver.find_element_by_tag_name(CTG_NAV['VALUE'])

                if CATEGORIES['FIND_BY'] == 'class':
                    categories = ctg_nav.find_elements_by_class_name(CATEGORIES['VALUE'])
                elif CATEGORIES['FIND_BY'] == 'id':
                    categories = ctg_nav.find_element_by_id(CATEGORIES['VALUE'])
                elif CATEGORIES['FIND_BY'] == 'tag':
                    categories = ctg_nav.find_elements_by_tag_name(CATEGORIES['VALUE'])

                # ctg_nav = driver.find_element_by_class_name('menu-sidebar-items')
                # categories = ctg_nav.find_elements_by_tag_name('li')
                restaurant_obj = {
                    'city_code':self.city_code,
                    'name':"Box8",
                    'type':"North Indian, South Indian",
                    'stars':4.1,
                    'ratings':"100+ Ratings",
                    'image':"https://assets.box8.co.in/images/Box8.jpg",
                    'country':self.country,
                    'city':self.city,
                    'city':'Bangalore',
                    'subzone':'General',
                    'platform':'Box8',
                    'dishes':[],
                    'added_on': str(datetime.datetime.utcnow())
                }

                self.dish_obj = Dish(self.driver, self.dish_config)

                for ctg in categories:
                    self.dish_obj.get_dishes(ctg,restaurant_obj)

                print('+++++++',len(restaurant_obj['dishes']))
                sort_key_info = restaurant_obj['platform']+'__'+restaurant_obj['subzone']+'__'+restaurant_obj['name'].strip().replace(' ','_')
                restaurant_obj['sort_key_info'] = sort_key_info
                restaurant_obj['stars'] = Decimal(str(restaurant_obj['stars']))

                self.dynamodb_write_obj = DynamoDBWrite()
                self.dynamodb_write_obj.dynamodb_write(restaurant_obj)
                

                # write data to parquet in s3
                restaurant_obj['stars'] = float(restaurant_obj['stars'])
                self.write_to_s3_parquet_obj = WriteS3Parquet(self.city)
                self.write_to_s3_parquet_obj.write_to_parquet(restaurant_obj)
                

            except Exception as e:
                print('++++++++NOT DONE',e)
            self.driver.close()
            
        except Exception as e:
                print('+++++++Exception while contents of given url',e)


if __name__  == '__main__':
    box8 = Box8()
    box8.get_details("https://box8.in/menu")