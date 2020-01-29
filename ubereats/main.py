from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, datetime, os
from selenium.webdriver.firefox.options import Options
from decimal import Decimal
from dish import Dish
from restaurant import Restaurant
import threading
from dynamodb_batch_write import DynamoDBBatchWrite
from write_to_s3_parquet import WriteS3Parquet
import json

class Ubereats:

    def __init__(self):
        self.CONFIG_FILE = "jwt-config.json"
        with open(self.CONFIG_FILE,'r') as config_file:
            self.data_set = json.load(config_file)
        
        self.options = Options()
        self.options.headless = True
        self.starter_config = self.data_set['UBEREATS']['CONFIG']['STARTER']
        self.dish_config = self.data_set['UBEREATS']['CONFIG']['DISH']
        self.restaurant_config = self.data_set['UBEREATS']['CONFIG']['RESTAURANT']
        self.config = self.data_set['UBEREATS']['CONFIG']
        self.dishes_data = []
        self.rest_url = set()
        self.restaurants_obj = []
        self.city = os.getenv('CITY', "bangalore")
        self.url = self.starter_config['URLS'][self.city]
        self.country = os.getenv('COUNTRY', "india")
        self.city_code = self.city + '__' + self.country
        self.driver = webdriver.Firefox(options=self.options)

    def get_details(self):
        try:
            
            self.driver.get(self.url)
            FIND_BY = self.starter_config['SELECTORS']['WAIT']['FIND_BY']
            VALUE = self.starter_config['SELECTORS']['WAIT']['VALUE']

            if FIND_BY == 'class':
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, VALUE))
                )
            elif FIND_BY == 'css':
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, VALUE))
                )
            elif FIND_BY == 'id':
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, VALUE))
                )
            elif FIND_BY == 'tag':
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.TAG_NAME, VALUE))
                )

            


            FIND_BY = self.starter_config['SELECTORS']['ALL_REST']['FIND_BY']
            VALUE = self.starter_config['SELECTORS']['ALL_REST']['VALUE']

            
            if FIND_BY == 'css':
                all_rest = self.driver.find_elements_by_css_selector(VALUE)
            elif FIND_BY == 'class':
                all_rest = self.driver.find_elements_by_class_name(VALUE)

            

            RESTAURANT_TYPE_FIND_BY = self.restaurant_config['SELECTORS']['TYPE']['FIND_BY']
            RESTAURANT_TYPE_VALUE = self.restaurant_config['SELECTORS']['TYPE']['VALUE']

            NAME={
                'FIND_BY': self.restaurant_config['SELECTORS']['NAME']['FIND_BY'],
                'VALUE': self.restaurant_config['SELECTORS']['NAME']['VALUE']
            }

            STARS_RATINGS={
                'FIND_BY': self.restaurant_config['SELECTORS']['STARS_RATINGS']['FIND_BY'],
                'VALUE': self.restaurant_config['SELECTORS']['STARS_RATINGS']['VALUE']
            }

        
            
            restaurants_obj = []
            print('+++++LENGTH',len(all_rest))
            for restaurant in all_rest:
                try:
                    anchor_tag = restaurant.find_element_by_tag_name("a")
                    reatuarnat_url = anchor_tag.get_attribute("href")
                    try:
                        if RESTAURANT_TYPE_FIND_BY == 'css':
                            type = restaurant.find_element_by_css_selector(RESTAURANT_TYPE_VALUE).get_attribute('textContent')
                        elif RESTAURANT_TYPE_FIND_BY == 'class':
                            type = restaurant.find_element_by_class_name(RESTAURANT_TYPE_VALUE).get_attribute('textContent')
                    except Exception as e:
                        type = None

                    try:
                        if STARS_RATINGS['FIND_BY'] == 'css':
                            stars_ratings = restaurant.find_element_by_css_selector(STARS_RATINGS['VALUE']).get_attribute('textContent')
                        elif STARS_RATINGS['FIND_BY'] == 'class':
                            stars_ratings = restaurant.find_element_by_class_name(STARS_RATINGS['VALUE']).get_attribute('textContent')
                        
                        tokens = stars_ratings.split('(')
                        print('+++++++tokens',tokens)
                        stars = tokens[0]
                        ratings = tokens[1].split(')')[0]
                    except Exception as e:
                        print('++++++stars exce',e)
                        stars = Decimal(str(4.1))
                        ratings = None
                    try:
                        image = restaurant.find_element_by_tag_name('img').get_attribute("src")
                    except Exception as e:
                        image = None

                    if NAME['FIND_BY'] == 'css':
                        name = restaurant.find_element_by_css_selector(NAME['VALUE']).get_attribute('textContent')
                    elif NAME['FIND_BY'] == 'class':
                        name = restaurant.find_element_by_class_name(NAME['VALUE']).get_attribute('textContent')
                    restaurant = {
                        'type': type,
                        'name':name,
                        'url':reatuarnat_url,
                        'stars': stars,
                        'ratings':ratings,
                        'image':image
                    }
                    restaurants_obj.append(restaurant)
                    # print('+++++rest added',restaurant)
                except Exception as e:
                    print("&&&&&&&&",e)
            try:
                self.driver.close()
            except Exception as e:
                print('++++++driver closing exception',e)

                

            self.rest_obj = Restaurant(self.dish_config,self.restaurant_config,self.dishes_data,self.city_code,self.country,self.city)
            self.dish_obj = Dish(self.dish_config)


            self.get_restaurant_data(restaurants_obj)
            

            # # # write to dynamodb
            self.dynamodb_write_obj = DynamoDBBatchWrite()
            self.dynamodb_write_obj.batch_write_to_ddb(self.dishes_data)
            # # # # write data to parquet in s3
            for restaurant_obj in self.dishes_data:
                restaurant_obj['stars'] = float(restaurant_obj['stars'])
            # # # print('++++++dishes data',json.dumps(self.dishes_data))
            self.write_to_s3_parquet_obj = WriteS3Parquet(self.city)
            self.write_to_s3_parquet_obj.write_to_parquet(self.dishes_data)

        except Exception as e:
            print('++++++++NOT DONE',e)


    def get_restaurant_data(self,restaurants_obj):

        no_of_threads = 2
        last_chunk = -1
        restaurants_obj_batch_threads = []
        length_of_restaurants_obj = len(restaurants_obj)
        # length_of_restaurants_obj= 4
        chunk_size = int(length_of_restaurants_obj/no_of_threads)
        for i in range(no_of_threads):
            
            batch = restaurants_obj[i*chunk_size:(i+1)*chunk_size]
            # batch = restaurants_data[0:2]
            restaurants_obj_batch_threads.append(threading.Thread(
                        target=self.get_restaurant_data_thread, args=(batch,)))
            restaurants_obj_batch_threads[-1].start()
            last_chunk = i

        last_chunk += 1
        if no_of_threads*chunk_size < length_of_restaurants_obj:
            
            batch = restaurants_obj[last_chunk*chunk_size:length_of_restaurants_obj]
            # batch = restaurants_data[0:2]
            restaurants_obj_batch_threads.append(threading.Thread(
                        target=self.get_restaurant_data_thread, args=(batch,)))
            restaurants_obj_batch_threads[-1].start()

        for thread in restaurants_obj_batch_threads:
            thread.join()


    def get_restaurant_data_thread(self,restaurants_obj):

        for restaurant_obj in restaurants_obj:
            try:
                options = Options()
                options.headless = True
                driver = webdriver.Firefox(options=options)
                self.rest_obj.get_restaurant(driver,restaurant_obj,self.dish_obj)
                driver.close()
            except Exception as e:
                print('++++++error while getting dish',e)
            try:
                driver.close()
            except:
                pass
        


if __name__ == '__main__':
    ubereats = Ubereats()
    ubereats.get_details()
