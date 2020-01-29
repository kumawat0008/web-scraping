from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time


class Dish:


    def __init__(self, dish_config, restaurant_obj,driver):
        self.dish_config = dish_config
        self.restaurant_obj = restaurant_obj
        self.driver = driver


    def get_dishes(self,dishes):          
            for dish in dishes:
                print("++++++++++INSIDEEEE GET_DISHES",len(dishes))
                try: 
                    if len(dish.text) !=0:

                        FIND_BY = self.dish_config['SELECTORS']['NAME']['FIND_BY']
                        VALUE = self.dish_config['SELECTORS']['NAME']['VALUE']
                        if FIND_BY == 'tag':
                            name = dish.find_element_by_tag_name(VALUE).text
                        elif FIND_BY == 'css':
                            name = dish.find_element_by_css_selector(VALUE).text
                        
                        FIND_BY = self.dish_config['SELECTORS']['DISH_TYPE']['FIND_BY']
                        VALUE = self.dish_config['SELECTORS']['DISH_TYPE']['VALUE']
                        if FIND_BY == 'tag':
                            dish_type = dish.find_element_by_tag_name(VALUE).text
                        elif FIND_BY == 'css':
                            dish_type = dish.find_element_by_css_selector(VALUE).text
                        
                        # dish_price = dish.find_element_by_class_selector('i.fa-inr').text
                        FIND_BY = self.dish_config['SELECTORS']['DISH_QUANTITY']['FIND_BY']
                        VALUE = self.dish_config['SELECTORS']['DISH_QUANTITY']['VALUE']
                        if FIND_BY == 'class':
                            dish_quantity = dish.find_elements_by_class_name(VALUE)
                        elif FIND_BY == 'css':
                            dish_quantity = dish.find_elements_by_css_selector(VALUE)
                        
                        try:
                            FIND_BY = self.dish_config['SELECTORS']['IMAGE']['FIND_BY']
                            VALUE = self.dish_config['SELECTORS']['IMAGE']['VALUE']
                            if FIND_BY == 'tag':
                                image = dish.find_element_by_tag_name(VALUE).get_attribute('src')
                            elif FIND_BY == 'css':
                                image = dish.find_element_by_css_selector(VALUE).get_attribute('src')
                            
                        except:
                            image = None

                        try:
                            FIND_BY = self.dish_config['SELECTORS']['URL']['FIND_BY']
                            VALUE = self.dish_config['SELECTORS']['URL']['VALUE']
                            if FIND_BY == 'tag':
                                dish_url = dish.find_element_by_tag_name(VALUE).get_attribute('href')
                            elif FIND_BY == 'css':
                                dish_url = dish.find_element_by_css_selector(VALUE).get_attribute('href')
                            
                        except:
                            dish_url = None
                        
                        

                        dish1_obj = {
                                'Name': name,
                                'type': dish_type,
                                'url' : dish_url,
                                'more_prices': [],
                                'image' : image
                            }
                        for quantity in dish_quantity:
                            split_items = quantity.text.split(" - ")
                            orig_quantity = split_items[0]
                            price = split_items[1]
                            more_prices = {
                                'quantity': orig_quantity,
                                'price': price,
                            }
                            dish1_obj['more_prices'].append(more_prices)
                        dish1_obj['quantity'] = orig_quantity
                        dish1_obj['price'] = price
                        self.restaurant_obj['dishes'].append(dish1_obj)
                        print("+++++LENGTHHH",len(dish_quantity))
                except Exception as e:
                    print('++++++',e)

            print("+++*****",len(self.restaurant_obj['dishes']))
            for dish_obj in self.restaurant_obj['dishes']:      
                print("++++++++++=AFTERE LENGTHHH")
                main_window = self.driver.current_window_handle
                
                self.driver.execute_script("window.open('');")
                # time.sleep(1)
                self.driver.switch_to.window(self.driver.window_handles[1])
                
                try:
                    self.get_description(dish_obj)
                except Exception as e:
                    print("+++ERRORRRR", e)
                print("++++++++++=))")
                self.driver.close()
                self.driver.switch_to_window(main_window)

    def get_description(self, dish_obj):
        
        print("++++++++++INSIDEGETDESCR")
        # options.headless = True
        print("+++++++++++URLLL",dish_obj['url'])
        try:
            self.driver.get(dish_obj['url'])
        except Exception as e:
            print("++++ERRRORRRR",e)
            
        print("))))))gettteed")
        time.sleep(2)
        
        try:
            FIND_BY = self.dish_config['SELECTORS']['ITEM']['FIND_BY']
            VALUE = self.dish_config['SELECTORS']['ITEM']['VALUE']
            # element = WebDriverWait(driver, 10).until(
            # EC.visibility_of_element_located((By.CLASS_NAME, VALUE))
            # )
            if FIND_BY == 'class':
                item = self.driver.find_element_by_class_name(VALUE)
            elif FIND_BY == 'id':
                item = self.driver.find_element_by_id(VALUE)
            
        except:
            item = None

        
        try:
            FIND_BY = self.dish_config['SELECTORS']['DESC']['FIND_BY']
            VALUE = self.dish_config['SELECTORS']['DESC']['VALUE']
            if FIND_BY == 'tag':
                desc = self.driver.find_element_by_tag_name(VALUE).text
            elif FIND_BY == 'css':
                desc = self.driver.find_element_by_css_selector(VALUE).text
            
        except:
            desc = None

        if desc == "":
            desc = None
            
        print("_))))OBJECT FOUNDDDD")
        dish_obj['description']=desc
        try:
            dish_obj['description']=desc
        except Exception as e:
            dish_obj['description']=None
            print("++++++ERRORRRR",e)
        print("+++APPENDEDDDD")