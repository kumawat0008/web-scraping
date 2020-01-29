import requests
from bs4 import BeautifulSoup 
from decimal import Decimal

import json

restaurants = []

class Restaurant:

    def __init__(self, config):

        self.config = config
        # self.subzone = subzone
        # self.restaurants_data = restaurants_data
        self.restaurant_config = self.config['RESTAURANT']


    def get_restaurants(self,url,subzone,restaurants_data):
        
        if url is None:
            URL = "https://www.zomato.com/bangalore/koramangala-5th-block-restaurants?ref_page=subzone"
        else:
            URL = url
            print( " URL == == ",URL)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        r = requests.get(URL,headers=headers) 


        soup = BeautifulSoup(r.content, 'html5lib')
        
        if self.restaurant_config['BEAUTIFUL_SOUP']:
            print(" inside ---")
            TAG = self.restaurant_config['SELECTORS']['WAIT']['TAG']
            FIND_BY = self.restaurant_config['SELECTORS']['WAIT']['FIND_BY']
            VALUE = self.restaurant_config['SELECTORS']['WAIT']['VALUE']
            data = soup.findAll(TAG,attrs={FIND_BY:VALUE})

                      
            
            name = {
                'TAG' : self.restaurant_config['SELECTORS']['NAME']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['NAME']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['NAME']['VALUE'],
            }
            image = {
                'TAG' : self.restaurant_config['SELECTORS']['IMAGE']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['IMAGE']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['IMAGE']['VALUE'],
                'ATTRIBUTE' : self.restaurant_config['SELECTORS']['IMAGE']['ATTRIBUTE'] 
            }
            url = {
                'TAG' : self.restaurant_config['SELECTORS']['URL']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['URL']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['URL']['VALUE'],
                'ATTRIBUTE' : self.restaurant_config['SELECTORS']['URL']['ATTRIBUTE']
            }
            type_r = {
                'TAG' : self.restaurant_config['SELECTORS']['TYPE']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['TYPE']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['TYPE']['VALUE'],
            }
            opens = {
                'TAG' : self.restaurant_config['SELECTORS']['OPENS_AT']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['OPENS_AT']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['OPENS_AT']['VALUE'],
            }
            star_rating = {
                'TAG' : self.restaurant_config['SELECTORS']['STARS']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['STARS']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['STARS']['VALUE'],
            }
            # dish_config = config['DISH']

            for row in data:

                try:
                    # print(" name ")
                    restaurant_name = row.find(name['TAG'],attrs={name['FIND_BY']:name['VALUE']}).text.strip()
                    try:
                        restaurant_image = row.find(image['TAG'],attrs={image['FIND_BY']:image['VALUE']})[image['ATTRIBUTE']]
                    except Exception as e:
                        # print('++EXCEPTION',e)
                        restaurant_image = None
                    
    
                    restaurant_url = row.find(url['TAG'],attrs={url['FIND_BY']:url['VALUE']})['href']
                    
                    restaurant_type = row.find(type_r['TAG'],attrs={type_r['FIND_BY']:type_r['VALUE']}).text
                    # print(" opens_at ")
                    opens_at = row.find(opens['TAG'],attrs={opens['FIND_BY']:opens['VALUE']}).text.strip()
                    # print(" starts_rating ")

                    stars_ratings = row.find(star_rating['TAG'],attrs={star_rating['FIND_BY']:star_rating['VALUE']}).text.strip().split('\n')
                    # print(" end ")

                    stars = stars_ratings[0]
                    try:
                        stars = Decimal(stars)
                    except:
                        stars = Decimal(0)
                    ratings = stars_ratings[-1]

                    restaurant = {
                        'url':restaurant_url,
                        'subzone':subzone,
                        'name':restaurant_name,
                        'image':restaurant_image,
                        'type':restaurant_type,
                        'opens_at':opens_at,
                        'stars':stars,
                        'ratings':ratings.strip()
                    }
                    # print('++++++++ ADDING RESTAURANT',restaurant)
                    # restaurant_details_sql.get_details(dish_config,restaurant)
                    
                    restaurants_data.append(restaurant)
                        
                except Exception as e:
                    print('+++++EXCEPTION',e)
                    
            # print('+++++++++HEY',urls)

            try:
                next_url = {
                    'TAG' : self.restaurant_config['SELECTORS']['NEXT_URL']['TAG'],
                    'FIND_BY' : self.restaurant_config['SELECTORS']['NEXT_URL']['FIND_BY'],
                    'VALUE' : self.restaurant_config['SELECTORS']['NEXT_URL']['VALUE'],
                    'ATTRIBUTE' : self.restaurant_config['SELECTORS']['NEXT_URL']['ATTRIBUTE']
                }
                print(" + + + + + ",next_url)
                next_link = soup.find(next_url['TAG'],attrs={next_url['FIND_BY']:next_url['VALUE']})[next_url['ATTRIBUTE']]
                print('++++++++HERE ',next_link)

                self.get_restaurants("https://www.zomato.com"+next_link,subzone,restaurants_data)
            except Exception as e:
                print('**********exception -- -- ',e)

    




