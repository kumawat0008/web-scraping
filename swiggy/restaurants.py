import requests
from bs4 import BeautifulSoup 

class Restaurant:

    def __init__(self, config):

        self.config = config
        # self.subzone = subzone
        # self.restaurants_data = restaurants_data
        self.restaurant_config = self.config['RESTAURANT']

    def get_restaurants(self, url,subzone, restaurants_data):

        try:
            if url is None:
                URL = "https://www.swiggy.com/bangalore/koramangala-restaurants"
            else:
                URL = url
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
            r = requests.get(URL,headers=headers) 


            soup = BeautifulSoup(r.content, 'html5lib')
            TAG = self.restaurant_config['SELECTORS']['WAIT']['TAG']
            FIND_BY = self.restaurant_config['SELECTORS']['WAIT']['FIND_BY']
            VALUE = self.restaurant_config['SELECTORS']['WAIT']['VALUE']
            data = soup.find_all(TAG,attrs={FIND_BY:VALUE})
            # data = soup.find_all('div',attrs={'class':'_3XX_A'})

            name = {
                'TAG' : self.restaurant_config['SELECTORS']['NAME']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['NAME']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['NAME']['VALUE'],
            }
            
            link = {
                'TAG' : self.restaurant_config['SELECTORS']['URL']['TAG'],
                'FIND_BY' : self.restaurant_config['SELECTORS']['URL']['FIND_BY'],
                'VALUE' : self.restaurant_config['SELECTORS']['URL']['VALUE'],
                'ATTRIBUTE' : self.restaurant_config['SELECTORS']['URL']['ATTRIBUTE']
            }


            for row in data:
                
                restaurant_link = row.find(link['TAG'],attrs={link['FIND_BY']:link['VALUE']})[link['ATTRIBUTE']]
                # restaurant_details_sql.get_details(config,"https://www.swiggy.com"+restaurant_link,subzone)
                restaurant_obj = {
                    'restaurant_link' : "https://www.swiggy.com"+restaurant_link,
                    'subzone' : subzone
                }
                print('+++++appending')
                restaurants_data.append(restaurant_obj)

            try:
                # links = soup.find_all('a', {'class': '_1FZ7A'})
                next_url = {
                        'TAG' : self.restaurant_config['SELECTORS']['NEXT_URL']['TAG'],
                        'FIND_BY' : self.restaurant_config['SELECTORS']['NEXT_URL']['FIND_BY'],
                        'VALUE' : self.restaurant_config['SELECTORS']['NEXT_URL']['VALUE'],
                        'ATTRIBUTE' : self.restaurant_config['SELECTORS']['NEXT_URL']['ATTRIBUTE']
                    }
                # print('++++++++next',next_url)
                links = soup.find_all(next_url['TAG'],attrs={next_url['FIND_BY']:next_url['VALUE']})
                # print('+++++++links',links)
                index = self.findHash(links)
                if index != -1:
                    self.get_restaurants("https://www.swiggy.com"+links[index+1]['href'],subzone,restaurants_data)
            except Exception as e:
                print('**********exception 1', e)
        except Exception as e:
            print('**********exception while getting all restro in subzone', e,'***subzone**',subzone)

    def findHash(self, list_of_links):

            for index in range(len(list_of_links)):
                if '#' == list_of_links[index]['href']:
                    if index == len(list_of_links)-1:
                        return -1
                    return index