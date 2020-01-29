import requests
from bs4 import BeautifulSoup 
from restaurants import Restaurant
import json
import threading
import dish
from dish import Dish
from dynamodb_batch_write import DynamoDBBatchWrite
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from write_to_s3_parquet import WriteS3Parquet
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class Zomato:

    def __init__(self):
        self.CONFIG_FILE = "jwt-config.json"
        with open(self.CONFIG_FILE,'r') as config_file:
            self.data_set = json.load(config_file)

        self.starter_config = self.data_set['ZOMATO']['CONFIG']['STARTER']

        self.config = self.data_set['ZOMATO']['CONFIG']
        self.dishes_data = []
        self.restaurants_data = []
        self.restaurants_obj = Restaurant(self.config)
        self.city = os.getenv('CITY', "jaipur")
        self.country = os.getenv('COUNTRY', "india")
        self.city_code = self.city+'__'+self.country
        self.dish_obj = Dish(self.config, self.city, self.country, self.city_code)
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)
        
        
    def get_data(self,url=None):

        url = self.starter_config["URLS"][self.city]
        self.driver.get(url)
        # WebDriverWait(self.selenium, 20).until(visibility_of_element_located((By.XPATH, xpath)))
        # WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section[3]/div/a[1]")))
        
        # subzone_container = self.driver.find_element_by_class_name('zimagery')
        subzone_container = self.driver.find_element_by_class_name("zimagery")
        print('+++++++++hey',subzone_container)


        # SUBZONES= {
        #     'FIND_BY' : self.starter_config['SELECTORS']['SUBZONES']['FIND_BY'],
        #     'VALUE' : self.starter_config['SELECTORS']['SUBZONES']['VALUE'] 
        # }
        # SUBZONES_CONTAINER = {
        #     'FIND_BY' : self.starter_config['SELECTORS']['SUBZONES_CONTAINER']['FIND_BY'],
        #     'VALUE' : self.starter_config['SELECTORS']['SUBZONES_CONTAINER']['VALUE'] 
        # }

        # if SUBZONES_CONTAINER['FIND_BY'] == 'class':
        #     subzones_container = self.driver.find_element_by_class_name(SUBZONES_CONTAINER['VALUE'])
        # elif SUBZONES_CONTAINER['FIND_BY'] == 'id':
        #     subzones_container = self.driver.find_element_by_id(SUBZONES_CONTAINER['VALUE'])
        # elif SUBZONES_CONTAINER['FIND_BY'] == 'tag':
        #     subzones_container = self.driver.find_element_by_tag_name(SUBZONES_CONTAINER['VALUE'])

        # if SUBZONES['FIND_BY'] == 'class':
        #     subzones = subzones_container.find_elements_by_class_name(SUBZONES['VALUE'])
        # elif SUBZONES['FIND_BY'] == 'id':
        #     subzones = subzones_container.find_element_by_id(SUBZONES['VALUE'])
        # elif SUBZONES['FIND_BY'] == 'tag':
        #     subzones = subzones_container.find_elements_by_tag_name(SUBZONES['VALUE'])

        # _list = []
        # for row in subzones:
        #     link = row.get_attribute('href')
        #     subzone = row.text
        #     # index = subzone.index('')
        #     # subzone = subzone[0:index]
        #     # subzone = " ".join(subzone)
        #     # print('++++++subzone',subzone)
        #     _list.append({
        #         'subzone': subzone,
        #         'link':"https://www.zomato.com/"+self.city+"/delivery-in-"+subzone.lower().replace(' ','-')+"?ref_page=subzone"
        #     })
        
        # print(" list of subzones ",_list)
            
        self.driver.close()
        

    
if __name__ == '__main__':
    start = time.time()
    zomato = Zomato()
    zomato.get_data(None)
    end = time.time()
    print('++++++++++TIME CONSUME',end-start)