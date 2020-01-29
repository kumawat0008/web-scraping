from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
import json
from decimal import Decimal
from dish import Dish
from dynamodb_write import DynamoDBWrite
from write_to_s3_parquet import WriteS3Parquet
import datetime
from dish_info import DishInfo


class BehrouzBiryani:

    def __init__(self, url=None):
        
        self.CONFIG_FILE = "jwt-config.json"
        with open(self.CONFIG_FILE,'r') as config_file:
            self.data_set = json.load(config_file)

        self.starter_config = self.data_set['BEHROUZ_BIRYANI']['CONFIG']['STARTER']
        self.config = self.data_set['BEHROUZ_BIRYANI']['CONFIG']
        self.dish_config = self.data_set['BEHROUZ_BIRYANI']['CONFIG']['DISH']
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox(options=self.options)
        self.url = self.starter_config["URL"]
        self.city = 'general'
        self.country = 'india'
        self.city_code = self.city+'__'+self.country
        self.all_dishes_url = []
        self.restaurant_obj = {}

        

    def get_details(self):

        try:
            self.driver.get(self.url)

            try:
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

                IMAGE_CONTAINER = {
                    'FIND_BY': self.starter_config['SELECTORS']['IMAGE_CONTAINER']['FIND_BY'],
                    'VALUE' : self.starter_config['SELECTORS']['IMAGE_CONTAINER']['VALUE']
                }
                
                CTG_NAV = {
                    'FIND_BY': self.dish_config['SELECTORS']['CATEGORY_NAV']['FIND_BY'],
                    'VALUE' : self.dish_config['SELECTORS']['CATEGORY_NAV']['VALUE']
                }
                CATEGORIES = {
                    'FIND_BY': self.dish_config['SELECTORS']['CATEGORIES']['FIND_BY'],
                    'VALUE' : self.dish_config['SELECTORS']['CATEGORIES']['VALUE']
                }

                # if IMAGE_CONTAINER['FIND_BY'] == 'class':
                #     image_container = driver.find_element_by_class_name(IMAGE_CONTAINER['VALUE'])
                # elif IMAGE_CONTAINER['FIND_BY'] == 'id':
                #     image_container = driver.find_element_by_id(IMAGE_CONTAINER['VALUE'])
                # elif IMAGE_CONTAINER['FIND_BY'] == 'tag':
                #     image_container = driver.find_element_by_tag_name(IMAGE_CONTAINER['VALUE'])

                # image = image_container.get_attribute('src')
                # print('++++++++',image)

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

                self.restaurant_obj = {
                    'city_code':self.city_code,
                    'name':"Behrouz Biryani",
                    'type':"Biryani, Mughlai",
                    'stars':4.1,
                    'ratings':"100+ Ratings",
                    'image':"https://product-assets.faasos.io/production/product/image_1562244587528_brz_june_mehfil.jpg",
                    'opens_at':None,
                    'country':self.country,
                    'city':self.city,
                    'subzone':'General',
                    'platform':'Behrouz Biryani',
                    'dishes':[],
                    'added_on': str(datetime.datetime.utcnow())
                }


                self.dish_obj = Dish(self.driver, self.dish_config)

                for ctg in categories:
                    id = ctg.get_attribute('id')
                    category = ctg.text
                    # print('*****',id,category)
                    self.dish_obj.get_dishes(ctg, self.all_dishes_url)

                
                self.get_all_dishes_info(self.all_dishes_url)
                print('********',self.restaurant_obj,len(self.restaurant_obj['dishes']))
                sort_key_info = self.restaurant_obj['platform']+'__'+self.restaurant_obj['subzone']+'__'+self.restaurant_obj['name'].strip().replace(' ','_')
                self.restaurant_obj['sort_key_info'] = sort_key_info
                self.restaurant_obj['stars'] = Decimal(str(self.restaurant_obj['stars']))

                # write to dynamodb
                self.dynamodb_write_obj = DynamoDBWrite()
                self.dynamodb_write_obj.dynamodb_write(self.restaurant_obj)
                

                # # write data to parquet in s3
                self.restaurant_obj['stars'] = float(self.restaurant_obj['stars'])
                self.write_to_s3_parquet_obj = WriteS3Parquet(self.city)
                self.write_to_s3_parquet_obj.write_to_parquet(self.restaurant_obj)
                
                
            except Exception as e:
                print('++++++++NOT DONE',e)

            
            self.driver.close()
    
        except Exception as e:
            print('+++++++Exception while contents of given url',e)

    
    def get_all_dishes_info(self, all_dishes_url):

        for url in all_dishes_url:
            dish_info_obj = DishInfo(self.driver, self.dish_config)
            main_window = self.driver.current_window_handle
            self.driver.execute_script("window.open('');")
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            dish_info_obj.get_dish_info(url, self.restaurant_obj)
            self.driver.close()
            self.driver.switch_to_window(main_window)
    

if __name__  == '__main__':

    behrouzBiryani = BehrouzBiryani("https://www.behrouzbiryani.com/bangalore/residency-road")
    
    behrouzBiryani.get_details()
