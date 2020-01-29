from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pizzas
import json
from selenium.webdriver.firefox.options import Options
from pizzas import Pizzas
import datetime
from decimal import Decimal
from dynamodb_write import DynamoDBWrite
from write_to_s3_parquet import WriteS3Parquet

class PizzaHut:

    def __init__(self,url=None):

        self.CONFIG_FILE = "jwt-config.json"

        with open(self.CONFIG_FILE,'r') as config_file:
            self.data_set = json.load(config_file)

        self.starter_config = self.data_set['PIZZAHUT']['CONFIG']['STARTER']
        self.config = self.data_set['PIZZAHUT']['CONFIG']
        self.dish_config = self.data_set['PIZZAHUT']['CONFIG']['DISH']
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox(options=self.options)
        self.url = self.starter_config["URL"]
        self.city = 'general'
        self.country = 'india'
        self.city_code = self.city+'__'+self.country

    def get_details(self):
        
        try:
            print('++++++Pizzas page getting scraped')
            self.driver.get(self.url)
            try:

                FIND_BY = self.starter_config['SELECTORS']['WAIT']['FIND_BY']
                VALUE = self.starter_config['SELECTORS']['WAIT']['VALUE']

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
                #     EC.visibility_of_element_located((By.CLASS_NAME, "product-content"))
                # )
                
                

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
                # ctg_nav = driver.find_element_by_class_name('menu-container')
                
                # categories = ctg_nav.find_elements_by_class_name('single-menu-item')
                
                
                restaurant_obj = {
                    'city_code':self.city_code,
                    'name':"Pizza Hut",
                    'type':"North Indian, South Indian",
                    'stars':4.1,
                    'ratings':"100+ Ratings",
                    'image':"https://images.phi.content-cdn.io/azure/inc-yum-resources/98d18d82-ba59-4957-9c92-3f89207a34f6/Images/userimages/Nov22-Dskt-Hero-Banner.jpg?height=540&width=2600",
                    'opens_at':None,
                    'country':self.country,
                    'city':self.city,
                    'subzone':'General',
                    'platform':'Pizza Hut',
                    'dishes':[],
                    'added_on': str(datetime.datetime.utcnow())
                }
                pizzas_obj = Pizzas(self.driver, self.dish_config)
                for ctg in categories:
                    category = ctg.find_element_by_tag_name('h2').text
                    # if category!='Deals':
                    self.get_dishes(pizzas_obj,ctg,category,restaurant_obj)
                
                print('+++++++',restaurant_obj,len(restaurant_obj['dishes']))

                sort_key_info = restaurant_obj['platform']+'__'+restaurant_obj['subzone']+'__'+restaurant_obj['name'].strip().replace(' ','_')
                restaurant_obj['sort_key_info'] = sort_key_info
                restaurant_obj['stars'] = Decimal(str(restaurant_obj['stars']))

                # self.dynamodb_write_obj = DynamoDBWrite()
                # self.dynamodb_write_obj.dynamodb_write(restaurant_obj)
                

                # write data to parquet in s3
                restaurant_obj['stars'] = float(restaurant_obj['stars'])
                self.write_to_s3_parquet_obj = WriteS3Parquet(self.city)
                self.write_to_s3_parquet_obj.write_to_parquet(restaurant_obj)
                
            except Exception as e:
                print('++++++++NOT DONE',e)
            self.driver.close()
        except Exception as e:
            print('+++++++Exception while contents of given url',e)
        

    def get_dishes(self,pizzas_obj,ctg,category,restaurant_obj):
        # ctg.click()
        # time.sleep(1)
        ancher_tag = ctg.find_element_by_tag_name('a')
        url = ancher_tag.get_attribute(self.starter_config['SELECTORS']['ANCHOR_TAG']['VALUE'])
        
        print('++++ctg url',category,url)
        main_window = self.driver.current_window_handle
        self.driver.execute_script("window.open('');")
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[1])
        pizzas_obj.get_pizzas(category,url,restaurant_obj)
        self.driver.close()
        self.driver.switch_to_window(main_window)

if __name__  == '__main__':

    pizzHut = PizzaHut("https://online.pizzahut.co.in/products?category=deals&id=CU00216624&redirect=true")
    pizzHut.get_details()