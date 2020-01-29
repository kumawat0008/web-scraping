import requests
from bs4 import BeautifulSoup
import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
import time
import datetime


class Dish:

    def __init__(self, config, city, country, city_code):
        self.config = config
        self.restaurant_config = self.config['RESTAURANT']

        self.dish_config = self.config['DISH']
        self.city = city
        self.country = country
        self.city_code = city_code

    def get_details(self, restaurant,dishes_data):


        try:
            print('+++++++data',restaurant['subzone'],restaurant['restaurant_link'])

            url = restaurant['restaurant_link']
            subzone = restaurant['subzone']
            
            if url is None:
                URL = "https://www.swiggy.com/restaurants/swad-e-punjab-outer-ring-road-hsr-bangalore-18433"
            else:
                URL = url
            r = requests.get(URL) 

            soup = BeautifulSoup(r.content, 'html5lib')

            
            name = {
                'TAG' : self.restaurant_config['SELECTORS']['NAME']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['NAME']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['NAME']['VALUE'],
            }

            type_ = {
                'TAG' : self.restaurant_config['SELECTORS']['TYPE']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['TYPE']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['TYPE']['VALUE'],
            }

            opens_at = {
                'TAG' : self.restaurant_config['SELECTORS']['OPENS_AT']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['OPENS_AT']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['OPENS_AT']['VALUE'],
            }

            star = {
                'TAG' : self.restaurant_config['SELECTORS']['STARS']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['STARS']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['STARS']['VALUE'],
            }

            rating = {
                'TAG' : self.restaurant_config['SELECTORS']['RATINGS']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['RATINGS']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['RATINGS']['VALUE'],
            }

            CATEGORIES = {
                'TAG' : self.dish_config['SELECTORS']['CATEGORIES']['TAG'],
                'FIND_BY' : self.dish_config['SELECTORS']['CATEGORIES']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['CATEGORIES']['VALUE'],
            }

            CATEGORY_TAB = {
                'TAG' : self.dish_config['SELECTORS']['CATEGORY_TAB']['TAG'],
                'FIND_BY' : self.dish_config['SELECTORS']['CATEGORY_TAB']['FIND_BY'],
                'VALUE' : self.dish_config['SELECTORS']['CATEGORY_TAB']['VALUE'],
            }

            
            

            try:
                
                restaurant_name = soup.find(name['TAG'],attrs={name['FIND_BY']:name['VALUE']}).text
                
                restaurant_type = soup.find(type_['TAG'],attrs={type_['FIND_BY']:type_['VALUE']}).text
                
                try:
                    opens_at = soup.find(opens_at['TAG'],attrs={opens_at['FIND_BY']:opens_at['VALUE']}).text
                except Exception as e:
                    # print('+++++++EXCEPTION 3',e)
                    opens_at = None

                
                
                stars = soup.find(star['TAG'],attrs={star['FIND_BY']:star['VALUE']}).text
                try:
                    stars = Decimal(stars)
                except Exception as e:
                    # print('+++++++EXCEPTION 4',e)
                    stars = Decimal(0)
                
                ratings = soup.find(rating['TAG'],attrs={rating['FIND_BY']:rating['VALUE']}).text
                image = None
                if opens_at is None:
                    restaurant_type = restaurant_type
                else:
                    restaurant_type = restaurant_type.replace(opens_at,'')
            

                category_tab = soup.find(CATEGORY_TAB['TAG'],attrs={CATEGORY_TAB['FIND_BY']:CATEGORY_TAB['VALUE']})
                
                categories = category_tab.find_all(CATEGORIES['TAG'],attrs={CATEGORIES['FIND_BY']:CATEGORIES['VALUE']})
                restaurant_obj = {
                    'city_code':self.city_code,
                    'name':restaurant_name,
                    'type':restaurant_type,
                    'stars':stars,
                    'ratings':ratings,
                    'image':image,
                    'opens_at':opens_at,
                    'country':self.country,
                    'city':self.city,
                    'subzone':subzone,
                    'platform':'SWIGGY',
                    'dishes':[],
                    'added_on': str(datetime.datetime.utcnow())
                }
                categories = categories[1:]
                
                
                for ctg in categories:
                    if ctg.text != "Veg" and ctg.text != "Non Veg":
                        self.get_dishes(soup, ctg, restaurant_obj)

                sort_key_info = restaurant_obj['platform']+'__'+subzone.strip().replace(' ','_')+'__'+restaurant_obj['name'].strip().replace(' ','_')
                restaurant_obj['sort_key_info'] = sort_key_info
                print('+++++RES OBJ',len(restaurant_obj['dishes']))
                dishes_data.append(restaurant_obj)
                


            except Exception as e:
                print('++++++++EXCEPTION WHILE GETTING DISHES 5',e)
        except Exception as e:
            print('++++++++EXCEPTION WHILE GETTING RESTRON DISHES 0',e,'****',restaurant['restaurant_link'])


    def get_dishes(self, soup,ctg,restaurant_obj):


        container = {
            'TAG' : self.dish_config['SELECTORS']['CONTAINER']['TAG'],
            'FIND_BY' : self.dish_config['SELECTORS']['CONTAINER']['FIND_BY']
            
        }
        data = {
            'TAG' : self.dish_config['SELECTORS']['DATA']['TAG'],
            'FIND_BY' : self.dish_config['SELECTORS']['DATA']['FIND_BY'],
            'VALUE' : self.dish_config['SELECTORS']['DATA']['VALUE'],
        }





        id = ctg['href'].split('#')[-1]
        
        container = soup.find(container['TAG'],attrs={container['FIND_BY']:id})
        data = container.find_all(data['TAG'],attrs={data['FIND_BY']:data['VALUE']})

        

        NAME = {
            'TAG' : self.dish_config['SELECTORS']['NAME']['TAG'],
            'FIND_BY' : self.dish_config['SELECTORS']['NAME']['FIND_BY'],
            'VALUE' : self.dish_config['SELECTORS']['NAME']['VALUE'],
        }

        PRICE = {
            'TAG' : self.dish_config['SELECTORS']['PRICE']['TAG'],
            'FIND_BY' : self.dish_config['SELECTORS']['PRICE']['FIND_BY'],
            'VALUE' : self.dish_config['SELECTORS']['PRICE']['VALUE'],
        }

        description = {
            'TAG' : self.dish_config['SELECTORS']['DESCRIPTION']['TAG'],
            'FIND_BY' : self.dish_config['SELECTORS']['DESCRIPTION']['FIND_BY'],
            'VALUE' : self.dish_config['SELECTORS']['DESCRIPTION']['VALUE'],
        }

        

        

        for row in data:
            dish = row.find(NAME['TAG'],attrs={NAME['FIND_BY']:NAME['VALUE']}).text
            try:
                ingredients = row.find(description['TAG'],attrs={description['FIND_BY']:description['VALUE']}).text
            except Exception as e:
                # print('+++++++EXCEPTION 2',e)
                ingredients = None
            price = row.find(PRICE['TAG'],attrs={PRICE['FIND_BY']:PRICE['VALUE']}).text
            category = ctg.text
            image = None
            
        
            dish_obj = {
                'name':dish,
                'price':price,
                'image': image,
                'category':category,
                'description':ingredients
            }
            restaurant_obj['dishes'].append(dish_obj)
  

# if __name__ == '__main__':
#     get_details(None,"ghjkl")
