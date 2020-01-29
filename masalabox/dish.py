

class Dish:


    def __init__(self, dish_config, restaurant_obj):
        self.dish_config = dish_config
        self.restaurant_obj = restaurant_obj


    def get_dishes(self,dishes):
                            
                for dish in dishes:
                    if len(dish.text) != 0:
                        FIND_BY = self.dish_config['SELECTORS']['THEAD']['FIND_BY']
                        VALUE = self.dish_config['SELECTORS']['THEAD']['VALUE']
                        if FIND_BY == 'tag':
                            thead = dish.find_element_by_tag_name(VALUE)
                        elif FIND_BY == 'id':
                            thead = dish.find_element_by_tag_name(VALUE)
                        
                        
                        print('++++++++++THEAD FOUND')
                        
                        try:
                            FIND_BY = self.dish_config['SELECTORS']['NAME']['FIND_BY']
                            VALUE = self.dish_config['SELECTORS']['NAME']['VALUE']
                            if FIND_BY == 'tag':
                                name = dish.find_element_by_tag_name(VALUE).text
                            elif FIND_BY == 'id':
                                name = dish.find_element_by_id(VALUE).text
                            
                        except Exception as e:
                            name = None

                        FIND_BY = self.dish_config['SELECTORS']['CAT']['FIND_BY']
                        VALUE = self.dish_config['SELECTORS']['CAT']['VALUE']
                        if FIND_BY == 'tag':
                            cat1 = dish.find_elements_by_tag_name(VALUE)[1].text
                        elif FIND_BY == 'id':
                            cat1 = dish.find_elements_by_id(VALUE)[1].text
                        
                        try :
                            if FIND_BY == 'tag':
                                cat2 = dish.find_elements_by_tag_name(VALUE)[3].text
                            elif FIND_BY == 'id':
                                cat2 = dish.find_elements_by_id(VALUE)[3].text
                        except Exception as e:
                            cat2 = None

                        # if len(name)!= 0:
                        #     print('++++++++++', name, cat1, cat2)
                        
                        FIND_BY = self.dish_config['SELECTORS']['TBODY']['FIND_BY']
                        VALUE = self.dish_config['SELECTORS']['TBODY']['VALUE']
                        if FIND_BY == 'tag':
                            tbody = dish.find_element_by_tag_name(VALUE)
                        elif FIND_BY == 'id':
                            tbody = dish.find_element_by_id(VALUE)
                        
                        
                        print('++++++++++TBODY FOUND')

                        FIND_BY = self.dish_config['SELECTORS']['TR']['FIND_BY']
                        VALUE =self.dish_config['SELECTORS']['TR']['VALUE']
                        if FIND_BY == 'tag':
                            trs = tbody.find_elements_by_tag_name(VALUE)
                        elif FIND_BY == 'id':
                            trs = tbody.find_elements_by_id(VALUE)
                        
                        
                        print('++++++++++TRS FOUND')
                    
                        for tr in trs:
                            if len(tr.text) !=0:
                                print('++++++++++TRS INSIDE')
                                try:
                                    FIND_BY = self.dish_config['SELECTORS']['TD']['FIND_BY']
                                    VALUE = self.dish_config['SELECTORS']['TD']['VALUE']
                                    if FIND_BY == 'tag':
                                        dish1 = tr.find_element_by_tag_name(VALUE).text
                                    elif FIND_BY == 'id':
                                        dish1 = tr.find_element_by_id(VALUE).text    
                                except Exception as e:
                                    dish1 = None
                                try:
                                    if FIND_BY == 'tag':
                                        item = tr.find_elements_by_tag_name(VALUE)[1].text
                                    elif FIND_BY == 'id':
                                        item = tr.find_elements_by_id(VALUE)[1].text
                                except Exception as e:
                                    item = None
                                
                                if cat2 is None:
                                    try:
                                        if FIND_BY == 'tag':
                                            item = tr.find_elements_by_tag_name(VALUE)[0].text
                                        elif FIND_BY == 'id':
                                            item = tr.find_elements_by_id(VALUE)[0].text
                                    except Exception as e:
                                        item = None

                                # print("**********CAT@@@@@@@@@",item)

                                if item is not None:
                                    split_items = item.split("\n")
                                    Name = split_items[0]
                                    quan = split_items[1]
                                
                            

                                try:
                                    if FIND_BY == 'tag':
                                        dish2 = tr.find_elements_by_tag_name(VALUE)[2].text
                                    elif FIND_BY == 'id':
                                        dish2 = tr.find_elements_by_id(VALUE)[2].text
                                except Exception as e:
                                    dish2 = None

                                
                                if cat1 is not None:
                                    dish1_obj = {
                                        'category': name,
                                        'name': Name,
                                        'type': cat1,
                                        'quantity': quan,
                                        'price': None,
                                        'description':dish1
                                    }
                                    
                                    self.restaurant_obj['dishes'].append(dish1_obj)

                                
                                if cat2 is not None:
                                    dish2_obj = {
                                        'category': name,
                                        'name': Name,
                                        'type': cat2,
                                        'quantity': quan,
                                        'price': None,
                                        'description':dish2
                                    }
                                    self.restaurant_obj['dishes'].append(dish2_obj)