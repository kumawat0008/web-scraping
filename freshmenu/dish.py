import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time

class Dish:


    def __init__(self, dish_config, restaurant_obj):
        self.dish_config = dish_config
        self.restaurant_obj = restaurant_obj
        



    def get_dishes_url(self,dishes,dishes_url):
                            
            for item in dishes:
                print("INSIDE")
                one_dish_url = item.find_element_by_tag_name("a").get_attribute("href")
                dishes_url.append(one_dish_url)

    def get_description(self,dishes_url):
        no_of_threads = 2
        last_chunk = -1
        dishes_url_batch_threads = []
        length_of_dishes_url = len(dishes_url)
        # length_of_dishes_url= 4
        chunk_size = int(length_of_dishes_url/no_of_threads)
        for i in range(no_of_threads):
            
            batch = dishes_url[i*chunk_size:(i+1)*chunk_size]
            # batch = restaurants_data[0:2]
            dishes_url_batch_threads.append(threading.Thread(
                        target=self.get_description_thread, args=(batch,)))
            dishes_url_batch_threads[-1].start()
            # self.get_description_thread(batch)
            last_chunk = i

        last_chunk += 1
        if no_of_threads*chunk_size < length_of_dishes_url:
            
            batch = dishes_url[last_chunk*chunk_size:length_of_dishes_url]
            # batch = restaurants_data[0:2]
            dishes_url_batch_threads.append(threading.Thread(
                        target=self.get_description_thread, args=(batch,)))
            dishes_url_batch_threads[-1].start()
            # self.get_description_thread(batch)

        for thread in dishes_url_batch_threads:
            thread.join()


    
    def get_description_thread(self, dishes_urls):

        for dish_url in dishes_urls:
            try:
                print('+++++++dish url',dish_url)
                options = Options()
                options.headless = True

                driver = webdriver.Firefox(options=options)
                driver.set_page_load_timeout(30)
                self.get_dish_data(driver,dish_url)
                driver.close()
            except Exception as e:
                print('++++++error while getting dish',e)
            try:
                driver.close()
            except:
                pass

    def get_dish_data(self,driver,dish_url):

        driver.get(dish_url)

        FIND_BY = self.dish_config['SELECTORS']['ITEMS']['FIND_BY']
        VALUE = self.dish_config['SELECTORS']['ITEMS']['VALUE']
        try:
            if FIND_BY == 'class':
                item= driver.find_element_by_class_name(VALUE)
            elif FIND_BY == 'css':
                item= driver.find_element_by_css_selector(VALUE)
            
            FIND_BY = self.dish_config['SELECTORS']['NAME']['FIND_BY']
            VALUE = self.dish_config['SELECTORS']['NAME']['VALUE']
            if FIND_BY == 'class':
                name = item.find_element_by_class_name(VALUE).text
            elif FIND_BY == 'tag':
                name = item.find_element_by_tag_name(VALUE).text
            
            FIND_BY = self.dish_config['SELECTORS']['PRICE_TAG']['FIND_BY']
            VALUE = self.dish_config['SELECTORS']['PRICE_TAG']['VALUE']
            try:
                if FIND_BY == 'class':
                    price_tag = item.find_element_by_class_name(VALUE)
                elif FIND_BY == 'css':
                    price_tag = item.find_element_by_css_selector(VALUE)
                
            except Exception as e:
                price_tag = None
            
            FIND_BY = self.dish_config['SELECTORS']['PRICE_OFFER']['FIND_BY']
            VALUE = self.dish_config['SELECTORS']['PRICE_OFFER']['VALUE']
            try:
                if FIND_BY == 'class':
                    orig_price = price_tag.find_elements_by_class_name(VALUE)[0].text
                elif FIND_BY == 'id':
                    orig_price = price_tag.find_elements_by_id(VALUE)[0].text
                
            except Exception as e:
                orig_price = None

            try:
                if FIND_BY == 'class':
                    curr_price = price_tag.find_elements_by_class_name(VALUE)[1].text
                elif FIND_BY == 'id':
                    curr_price = price_tag.find_elements_by_id(VALUE)[1].text
                
            except Exception as e:
                curr_price = None
            
            try:
                if FIND_BY == 'class':
                    offer = price_tag.find_elements_by_class_name(VALUE)[2].text
                elif FIND_BY == 'id':
                    offer = price_tag.find_elements_by_id(VALUE)[2].text
                
            except Exception as e:
                offer = None

            FIND_BY = self.dish_config['SELECTORS']['DESC']['FIND_BY']
            VALUE = self.dish_config['SELECTORS']['DESC']['VALUE']
            if FIND_BY == 'class':
                try:
                    desc = driver.find_element_by_class_name(VALUE).text
                except Exception as e:
                    desc = None
            elif FIND_BY == 'id':
                try:
                    desc = driver.find_element_by_id(VALUE).text
                except Exception as e:
                    desc = None
            
            FIND_BY = self.dish_config['SELECTORS']['INGREDIENTS']['FIND_BY']
            VALUE = self.dish_config['SELECTORS']['INGREDIENTS']['VALUE']
            if FIND_BY == 'class':
                try:
                    ingredients = driver.find_element_by_class_name(VALUE).text
                except Exception as e:
                    ingredients = None
            elif FIND_BY == 'id':
                try:
                    ingredients = driver.find_element_by_id(VALUE).text
                except Exception as e:
                    ingredients = None
                        
            FIND_BY = self.dish_config['SELECTORS']['NUTRITION']['FIND_BY']
            VALUE = self.dish_config['SELECTORS']['NUTRITION']['VALUE']
            if FIND_BY == 'class':
                try:
                    nutrition = driver.find_element_by_class_name(VALUE).text
                except Exception as e:
                    nutrition = None
            elif FIND_BY == 'id':
                try:
                    nutrition = driver.find_element_by_id(VALUE).text
                except Exception as e:
                    nutrition = None

            IMAGE_FIND_BY = self.dish_config['SELECTORS']['IMAGE']['FIND_BY']
            IMAGE_VALUE = self.dish_config['SELECTORS']['IMAGE']['VALUE']
            if IMAGE_FIND_BY == 'class':
                try:
                    image = driver.find_element_by_class_name(IMAGE_VALUE).get_attribute('src')
                    print('++++++++++SDFsfs',image)
                except Exception as e:
                    image = None
            elif IMAGE_FIND_BY == 'id':
                try:
                    image = driver.find_element_by_id(IMAGE_VALUE).get_attribute('src')
                    
                except Exception as e:
                    image = None
            dish1_obj = {
                                'name': name,
                                'orig_price': orig_price,
                                'price' : curr_price,
                                'offer': offer,
                                'description': ingredients+" "+desc,
                                'details': desc,
                                'nutrition' : nutrition,
                                'image':image
                            }
            print('++++++++dish obj',dish1_obj)
                            
            self.restaurant_obj['dishes'].append(dish1_obj)
                
        except Exception as e:
            print('++++++error while getting dish',e)

    