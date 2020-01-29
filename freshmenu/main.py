from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json,os, datetime, threading
from write_to_s3_parquet import WriteS3Parquet
from selenium.webdriver.firefox.options import Options
from dish import Dish
from dynamodb_write import DynamoDBWrite
from decimal import Decimal

class FreshMenu:

    def __init__(self):
        self.CONFIG_FILE = "jwt-config-freshmenu.json"
        with open(self.CONFIG_FILE,'r') as config_file:
            self.data_set = json.load(config_file)
        
        self.options = Options()
        self.options.headless = True
        self.starter_config = self.data_set['FRESHMENU']['CONFIG']['STARTER']
        self.dish_config = self.data_set['FRESHMENU']['CONFIG']['DISH']
        self.config = self.data_set['FRESHMENU']['CONFIG']
        self.url = self.starter_config['URL']
        self.dishes_data = []
        self.dishes_url = list()
        self.restaurant_obj = {}
        self.city = os.getenv('CITY', "bangalore")
        self.country = os.getenv('COUNTRY', "india")
        self.city_code = self.city + '__' + self.country
        self.driver = webdriver.Firefox(options=self.options)

    def get_details(self):
        try:
            self.driver.get(self.url)
            # for i in range(3):
            #     try:
            #         self.driver.find_element_by_id("exitIntentEmail").send_keys("abc@gmail.com")
            #         time.sleep(3)
            #         self.driver.find_element_by_class_name("submit").click()
            #     except:
            #         print("ERROR++++++++")
            # for i in range(0):
            #     try:
            #         self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #     except:
            #         print("ERROR SCROLL++++++++")
            #     time.sleep(3)
            #     print("________", i)
            
            # for i in range(3):
            #     try:
            #         self.driver.find_element_by_id("exitIntentEmail").send_keys("abc@gmail.com")
            #         time.sleep(3)
            #         self.driver.find_element_by_class_name("submit").click()
            #         time.sleep(3)
            #     except:
            #         print("ERROR++++++++")

            try:
                time.sleep(3)
                FIND_BY = self.dish_config['SELECTORS']['DISHES']['FIND_BY']
                VALUE = self.dish_config['SELECTORS']['DISHES']['VALUE']
                if FIND_BY == 'class':
                    dishes= self.driver.find_elements_by_class_name(VALUE)
                elif FIND_BY == 'id':
                    dishes= self.driver.find_elements_by_id(VALUE)
                
            except Exception as identifier:
                print("Error************",identifier)
            
            restaurant_obj = {
                            'city_code': self.city_code,
                            'name': "Fresh Menu",
                            'type': 'Mexican,Thai,Continental,Mediterranean,Indian,Chinese,Italian,American',
                            'stars': 4.1,
                            'ratings': '100+ ratings',
                            'image': 'https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwjVhJHBsuTmAhUwwzgGHQaEDAMQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.youtube.com%2Fchannel%2FUCtg2fATkg7hXYa5VzxzZzPg&psig=AOvVaw3cdHfc2BzRGirA_FABBvnJ&ust=1578036499721707',
                            'opens_at': None,
                            'country': self.country,
                            'subzone' : 'General',
                            'city':self.city,
                            'platform':'FRESHMENU',
                            'dishes':[],
                            'added_on': str(datetime.datetime.utcnow())
                            }

            
            
            self.restaurant_obj = restaurant_obj
            
            dish_obj = Dish(self.dish_config, self.restaurant_obj)
            print("++++HEREEE")
            dish_obj.get_dishes_url(dishes,self.dishes_url)
            self.driver.close()
            print("++++BACKKKKK",len(self.dishes_url))
            dish_obj.get_description(self.dishes_url)
                      
            print("OBJJJJJJJJJJJJJ++++", len(self.restaurant_obj['dishes']))
            
            sort_key_info = restaurant_obj['platform']+'__'+restaurant_obj['subzone']+'__'+restaurant_obj['name'].strip().replace(' ','_')
            restaurant_obj['sort_key_info'] = sort_key_info
            restaurant_obj['stars'] = Decimal(str(self.restaurant_obj['stars']))
            # # write to dynamodb
            self.dynamodb_write_obj = DynamoDBWrite()
            self.dynamodb_write_obj.dynamodb_write(self.restaurant_obj)
            # write data to parquet in s3
            restaurant_obj['stars'] = float(self.restaurant_obj['stars'])
            self.write_to_s3_parquet_obj = WriteS3Parquet(self.city)
            self.write_to_s3_parquet_obj.write_to_parquet(self.restaurant_obj)
            
        except Exception as e:
            print("+++++NOT DONE",e)
        try:
            self.driver.close()
        except:
            pass

if __name__ == "__main__":
    freshmenu = FreshMenu()
    freshmenu.get_details()