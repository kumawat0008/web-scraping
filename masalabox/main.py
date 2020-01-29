from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, os, datetime
from write_to_s3_parquet import WriteS3Parquet
from selenium.webdriver.firefox.options import Options
from dish import Dish
from dynamodb_write import DynamoDBWrite
from decimal import Decimal

class MasalaBox:

    def __init__(self):
        self.CONFIG_FILE = "jwt-config-masalabox.json"
        with open(self.CONFIG_FILE,'r') as config_file:
            self.data_set = json.load(config_file)
        
        self.options = Options()
        self.options.headless = True
        self.starter_config = self.data_set['MASALABOX']['CONFIG']['STARTER']
        self.dish_config = self.data_set['MASALABOX']['CONFIG']['DISH']
        self.config = self.data_set['MASALABOX']['CONFIG']
        self.url = self.starter_config['URL']
        self.dishes_data = []

        self.restaurant_obj = {}
        self.city = os.getenv('CITY', "bangalore")
        self.country = os.getenv('COUNTRY', "india")
        self.city_code = self.city + '__' + self.country
        self.driver = webdriver.Firefox(options=self.options)

    def get_details(self, url=None):
        try:
            # time.sleep(5)
            self.driver.get(self.url)

            FIND_BY = self.dish_config['SELECTORS']['DISHESH']['FIND_BY']
            VALUE = self.dish_config['SELECTORS']['DISHESH']['VALUE']
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, VALUE))
            )
            if FIND_BY == 'class':
                dishes = self.driver.find_elements_by_class_name(VALUE)
            elif FIND_BY == 'id':
                dishes = self.driver.find_elements_by_id(VALUE)
            restaurant_obj = {
                            'city_code': self.city_code,
                            'name': "Masala Box",
                            'type': 'North Indian, South Indian',
                            'stars': 4.1,
                            'ratings': '100+ ratings',
                            'image': 'https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwju_pWC2N_mAhVOzzgGHe4dBvIQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.masalabox.com%2F&psig=AOvVaw1h-_mKB5oipFia4-jSyvIU&ust=1577874845479690',
                            'opens_at': None,
                            'country': self.country,
                            'subzone' : 'General',
                            'city':self.city,
                            'platform':'MASALABOX',
                            'dishes':[],
                            'added_on': str(datetime.datetime.utcnow())
                            }

            
            self.restaurant_obj = restaurant_obj
            dish_obj = Dish(self.dish_config, self.restaurant_obj)
            dish_obj.get_dishes(dishes)
            print("OBJJJJJJJJJJJJJ++++", len(self.restaurant_obj['dishes']))

            sort_key_info = restaurant_obj['platform']+'__'+restaurant_obj['subzone']+'__'+restaurant_obj['name'].strip().replace(' ','_')
            restaurant_obj['sort_key_info'] = sort_key_info
            restaurant_obj['stars'] = Decimal(str(self.restaurant_obj['stars']))
            # write to dynamodb
            self.dynamodb_write_obj = DynamoDBWrite()
            self.dynamodb_write_obj.dynamodb_write(self.restaurant_obj)
            # write data to parquet in s3
            restaurant_obj['stars'] = float(self.restaurant_obj['stars'])
            self.write_to_s3_parquet_obj = WriteS3Parquet(self.city)
            self.write_to_s3_parquet_obj.write_to_parquet(self.restaurant_obj)

            
        except Exception as e:
            print('++++++++NOT DONE',e)
        self.driver.close()

if __name__ == '__main__':
    masalabox = MasalaBox()
    masalabox.get_details()
