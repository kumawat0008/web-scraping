from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, os, datetime
from dish import Dish
from write_to_s3_parquet import WriteS3Parquet
from selenium.webdriver.firefox.options import Options
from dynamodb_write import DynamoDBWrite
from decimal import Decimal
import json

class ReadyBowl:


    def __init__(self):
        self.CONFIG_FILE = "jwt-config-readybowl.json"
        with open(self.CONFIG_FILE,'r') as config_file:
            self.data_set = json.load(config_file)
        
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--disable-notifications")
        self.starter_config = self.data_set['READYBOWL']['CONFIG']['STARTER']
        self.dish_config = self.data_set['READYBOWL']['CONFIG']['DISH']
        self.config = self.data_set['READYBOWL']['CONFIG']
        self.url = self.starter_config['URL']
        self.dishes_data = []

        self.restaurant_obj = set()
        self.city = os.getenv('CITY', "bangalore")
        self.country = os.getenv('COUNTRY', "india")
        self.city_code = self.city + '__' + self.country
        self.driver = webdriver.Firefox(options=self.options)
        
    def get_details(self):
        
        
        try:
            self.driver.set_page_load_timeout(30)
            self.driver.get(self.url)
            
            print("+++++++++HEREEEEE coming")
            try:
                FIND_BY = self.starter_config['SELECTORS']['PRE_ORDER']['FIND_BY']
                VALUE = self.starter_config['SELECTORS']['PRE_ORDER']['VALUE']
                # if FIND_BY == 'class':
                #     self.driver.find_element_by_class_name(VALUE).click()
                # elif FIND_BY == 'css':
                #     self.driver.find_element_by_css_selector(VALUE).click()
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="hmodal"]/div/div/div[2]/button'))).click()
                
                print("+++++++CLICKED")
            except Exception as e:
                print("))))))))ERROR",e)
            FIND_BY = self.dish_config['SELECTORS']['DISHESH']['FIND_BY']
            VALUE = self.dish_config['SELECTORS']['DISHESH']['VALUE']
            # element = WebDriverWait(driver, 10).until(
            #     EC.visibility_of_element_located((By.CLASS_NAME, VALUE))
            # )
            if FIND_BY == 'class':
                dishes = self.driver.find_elements_by_class_name(VALUE)
            elif FIND_BY == 'css':
                dishes = self.driver.find_elements_by_css_selector(VALUE)
            print("+++++++++HEREEEEE")
            restaurant_obj = {
                            'city_code': self.city_code,
                            'name': "Ready Bowl",
                            'type': 'North Indian, South Indian',
                            'stars': 4.1,
                            'ratings': '100+ ratings',
                            'image': 'https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjo7r61s-TmAhX1zDgGHfJjAkoQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.zomato.com%2Fbangalore%2Freadybowl-btm&psig=AOvVaw2OnHt5mwTrtZrmFtJTEItS&ust=1578036819956899',
                            'opens_at': None,
                            'country': self.country,
                            'subzone' : 'General',
                            'city':self.city,
                            'platform':'READYBOWL',
                            'dishes':[],
                            'added_on': str(datetime.datetime.utcnow())
                            }

            
            self.restaurant_obj = restaurant_obj
            dish_obj = Dish(self.dish_config, self.restaurant_obj,self.driver)
            dish_obj.get_dishes(dishes)
            self.driver.close()
            

            sort_key_info = restaurant_obj['platform']+'__'+restaurant_obj['subzone']+'__'+restaurant_obj['name'].strip().replace(' ','_')
            restaurant_obj['sort_key_info'] = sort_key_info
            restaurant_obj['stars'] = Decimal(str(self.restaurant_obj['stars']))
            # # write to dynamodb
            self.dynamodb_write_obj = DynamoDBWrite()
            self.dynamodb_write_obj.dynamodb_write(self.restaurant_obj)
            # # write data to parquet in s3
            restaurant_obj['stars'] = float(self.restaurant_obj['stars'])
            print("OBJJJJJJJJJJJJJ++++print",json.dumps(self.restaurant_obj))
            self.write_to_s3_parquet_obj = WriteS3Parquet(self.city)
            self.write_to_s3_parquet_obj.write_to_parquet(self.restaurant_obj)

        except:
            print('++++++++NOT DONE')
            self.driver.close()

if __name__ == '__main__':
    readybowl = ReadyBowl()
    readybowl.get_details()
