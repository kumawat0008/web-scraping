from decimal import Decimal
import time
import datetime
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Dish:

    def __init__(self, config, city, country, city_code):
        self.config = config
        self.restaurant_config = self.config['RESTAURANT']

        self.dish_config = self.config['DISH']
        self.city = city
        self.country = country
        self.city_code = city_code

    def get_details(self,driver,restaurant,dishes_data):
    
        try:
            URL = restaurant['url']
            print('+++++++URL',URL)
            # options = Options()
            # options.headless = True
            # driver = webdriver.Firefox(options=options)
            # driver.set_page_load_timeout(30)
            driver.get(URL)
            time.sleep(3)

            if self.dish_config['BEAUTIFUL_SOUP']:
                pass

            else:
                try:
                    FIND_BY = self.dish_config['SELECTORS']['WAIT']['FIND_BY']
                    VALUE = self.dish_config['SELECTORS']['WAIT']['VALUE']

                    if FIND_BY == 'class':
                        element = WebDriverWait(driver, 15).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, VALUE))
                        )
                    elif FIND_BY == 'id':
                        element = WebDriverWait(driver, 15).until(
                            EC.visibility_of_element_located((By.ID, VALUE))
                        )
                    elif FIND_BY == 'tag':
                        element = WebDriverWait(driver, 15).until(
                            EC.visibility_of_element_located((By.TAG_NAME, VALUE))
                        )
                    

                    CATEGORY_NAV = {
                        'FIND_BY': self.dish_config['SELECTORS']['CATEGORY_NAV']['FIND_BY'],
                        'VALUE' : self.dish_config['SELECTORS']['CATEGORY_NAV']['VALUE']
                    }
                    CATEGORIES = {
                        'FIND_BY': self.dish_config['SELECTORS']['CATEGORIES']['FIND_BY'],
                        'VALUE' : self.dish_config['SELECTORS']['CATEGORIES']['VALUE']
                    }
                    if CATEGORY_NAV['FIND_BY'] == 'class':
                        ctg_nav = driver.find_element_by_class_name(CATEGORY_NAV['VALUE'])
                    elif CATEGORY_NAV['FIND_BY'] == 'id':
                        ctg_nav = driver.find_element_by_id(CATEGORY_NAV['VALUE'])
                    elif CATEGORY_NAV['FIND_BY'] == 'tag':
                        ctg_nav = driver.find_element_by_tag_name(CATEGORY_NAV['VALUE'])
                    # print('+++++++cat nav',ctg_nav)
                    # ctg_nav = driver.find_element_by_class_name('o2_nav_bar')
                    if CATEGORIES['FIND_BY'] == 'class':
                        categories = ctg_nav.find_elements_by_class_name(CATEGORIES['VALUE'])
                    elif CATEGORIES['FIND_BY'] == 'id':
                        categories = ctg_nav.find_element_by_id(CATEGORIES['VALUE'])
                    elif CATEGORIES['FIND_BY'] == 'tag':
                        categories = ctg_nav.find_elements_by_tag_name(CATEGORIES['VALUE'])
                    # print('++++++categories',categories)
                    # categories = ctg_nav.find_elements_by_class_name('item')
                
                    categories = categories[1:]
                    restaurant_obj = {
                        'name':restaurant['name'],
                        'type':restaurant['type'],
                        'stars':restaurant['stars'],
                        'ratings':restaurant['ratings'],
                        'image':restaurant['image'],
                        'opens_at':restaurant['opens_at'],
                        'country':self.country,
                        'city':self.city,
                        'subzone':restaurant['subzone'],
                        'platform':'ZOMATO',
                        'added_on': str(datetime.datetime.utcnow()),
                        'city_code':self.city_code,
                        'dishes':[]
                    }
                    
                    for ctg in categories:
                        id = ctg.get_attribute('id')
                        category = ctg.get_attribute('textContent')
                        item_id = id.split('_')[-1]
                        # print('*****',item_id,category)
                        self.get_dishes(driver,item_id,category,restaurant_obj)

                    sort_key_info = restaurant_obj['platform']+'__'+restaurant_obj['subzone'].strip().replace(' ','_')+'__'+restaurant_obj['name'].strip().replace(' ','_')
                    restaurant_obj['sort_key_info'] = sort_key_info

                    dishes_data.append(restaurant_obj)
                    
                    
                                
                except Exception as e:
                    print('++++++++NOT DONE',restaurant['name'],e)
                # driver.close()
        except Exception as e:
            print('+++++++exception while getting dish url',e)
        
    def get_dishes(self,driver,item_id,category,restaurant_obj):

        MENU_CONTAINER = {
            'FIND_BY': self.dish_config['SELECTORS']['MENU_CONTAINER']['FIND_BY'],
            'VALUE' : self.dish_config['SELECTORS']['MENU_CONTAINER']['VALUE']
        }
        MENU_CONTAINER2 = {
            'FIND_BY': self.dish_config['SELECTORS']['MENU_CONTAINER2']['FIND_BY'],
            'VALUE' : self.dish_config['SELECTORS']['MENU_CONTAINER2']['VALUE']
        }

        

        try:

            if MENU_CONTAINER['FIND_BY'] == 'class':
                menu_container_id = MENU_CONTAINER['VALUE']+item_id
                menu_container = driver.find_element_by_class_name(menu_container_id)
            elif MENU_CONTAINER['FIND_BY'] == 'id':
                menu_container_id = MENU_CONTAINER['VALUE']+item_id
                menu_container = driver.find_element_by_id(menu_container_id)
            elif MENU_CONTAINER['FIND_BY'] == 'tag':
                menu_container_id = MENU_CONTAINER['VALUE']+item_id
                menu_container = driver.find_element_by_tag_name(menu_container_id)
        except:

            if MENU_CONTAINER2['FIND_BY'] == 'class':
                menu_container_id = MENU_CONTAINER2['VALUE']+item_id
                menu_container = driver.find_element_by_class_name(menu_container_id)
            elif MENU_CONTAINER2['FIND_BY'] == 'id':
                menu_container_id = MENU_CONTAINER2['VALUE']+item_id
                menu_container = driver.find_element_by_id(menu_container_id)
            elif MENU_CONTAINER2['FIND_BY'] == 'tag':
                menu_container_id = MENU_CONTAINER2['VALUE']+item_id
                menu_container = driver.find_element_by_tag_name(menu_container_id)
        # print('+++++++menu container',menu_container)
        CONTENT = {
            'FIND_BY': self.dish_config['SELECTORS']['CONTENT']['FIND_BY'],
            'VALUE' : self.dish_config['SELECTORS']['CONTENT']['VALUE']
        }
        NAME = {
            'FIND_BY': self.dish_config['SELECTORS']['NAME']['FIND_BY'],
            'VALUE' : self.dish_config['SELECTORS']['NAME']['VALUE']
        }
        PRICE = {
            'FIND_BY': self.dish_config['SELECTORS']['PRICE']['FIND_BY'],
            'VALUE' : self.dish_config['SELECTORS']['PRICE']['VALUE']
        }
        IMAGE = {
            'FIND_BY': self.dish_config['SELECTORS']['IMAGE']['FIND_BY'],
            'VALUE' : self.dish_config['SELECTORS']['IMAGE']['VALUE'],
            'ATTRIBUTE': self.dish_config['SELECTORS']['IMAGE']['ATTRIBUTE']
        }
        DESCRIPTION = {
            'FIND_BY': self.dish_config['SELECTORS']['DESCRIPTION']['FIND_BY'],
            'VALUE' : self.dish_config['SELECTORS']['DESCRIPTION']['VALUE']
        }

        
        if CONTENT['FIND_BY'] == 'class':
            contents = menu_container.find_elements_by_class_name(CONTENT['VALUE'])
        elif CONTENT['FIND_BY'] == 'id':
            contents = menu_container.find_element_by_id(CONTENT['VALUE'])
        elif NAME['FIND_BY'] == 'tag':
            contents = menu_container.find_elements_by_tag_name(CONTENT['VALUE'])

        

        # contents = menu_container.find_elements_by_class_name('content')
        

        
        # print('++++++++contents',contents)
        for content in contents:

            
            if NAME['FIND_BY'] == 'class':
                name = content.find_element_by_class_name(NAME['VALUE']).text
            elif NAME['FIND_BY'] == 'id':
                name = content.find_element_by_id(NAME['VALUE']).text
            elif NAME['FIND_BY'] == 'tag':
                name = content.find_element_by_tag_name(NAME['VALUE']).text

            

            
            if PRICE['FIND_BY'] == 'class':
                price = content.find_element_by_class_name(PRICE['VALUE']).text
            elif PRICE['FIND_BY'] == 'id':
                price = content.find_element_by_id(PRICE['VALUE']).text
            elif PRICE['FIND_BY'] == 'tag':
                price = content.find_element_by_tag_name(PRICE['VALUE']).text
            # price = content.find_element_by_class_name('description')
            try:
                if IMAGE['FIND_BY'] == 'class':
                    image = content.find_element_by_class_name(IMAGE['VALUE']).get_attribute(IMAGE['ATTRIBUTE'])
                elif IMAGE['FIND_BY'] == 'id':
                    image = content.find_element_by_id(IMAGE['VALUE']).get_attribute(IMAGE['ATTRIBUTE'])
                elif IMAGE['FIND_BY'] == 'tag':
                    image = content.find_element_by_tag_name(IMAGE['VALUE']).get_attribute(IMAGE['ATTRIBUTE'])
            except:
                image = None
            # image = content.find_element_by_tag_name('img').get_attribute('src')
            try:
                if DESCRIPTION['FIND_BY'] == 'class':
                    desc = content.find_element_by_class_name(DESCRIPTION['VALUE'])
                elif DESCRIPTION['FIND_BY'] == 'id':
                    desc  = content.find_element_by_id(DESCRIPTION['VALUE'])
                elif DESCRIPTION['FIND_BY'] == 'tag':
                    desc = content.find_element_by_tag_name(DESCRIPTION['VALUE'])
                # desc = content.find_element_by_class_name('meta')
                desc = desc.text
            except:
                desc = None
        
            dish_obj = {
                'name':name,
                'price': price,
                'image':image,
                'category':category,
                'description':desc
            }
            print('++++++++dish added')
            restaurant_obj['dishes'].append(dish_obj)


# if __name__ == '__main__':
#     get_details(None,"ghjkl")
