from config import dynamodb,TABLE_NAME
from botocore.exceptions import ClientError
import json

class DynamoDBBatchWrite:

    def __init__(self):
        pass

    def batch_write_to_ddb(self, dishes_data):

        dishes_data_set = set()
        new_dishes_data = []

        for dish_data in dishes_data:
            if dish_data['sort_key_info'] not in dishes_data_set:
                dishes_data_set.add(dish_data['sort_key_info'])
                new_dishes_data.append(dish_data)

        dishes_data = new_dishes_data
        
        ddb_batch = []

        for dish_data in dishes_data:
            ddb_batch.append({
                "PutRequest":{
                    "Item":dish_data
                }
            })

        num_of_items = len(ddb_batch)
        chunk_size = 25
        no_of_chunks = int(num_of_items/chunk_size)
        last_chunk = -1
        batch_threads = []
        for i in range(no_of_chunks):
            batch = {
                'RequestItems': {
                    TABLE_NAME: ddb_batch[i*chunk_size:(i+1)*chunk_size]
                }
            }
            # print('########', batch)
            # batch_threads.append(threading.Thread(
            #     target=batch_write_in_jwt_dishes, args=(batch,)))
            # batch_threads[-1].start()
            self.batch_write_in_jwt_dishes(batch)
            last_chunk = i
        last_chunk += 1
        if no_of_chunks*chunk_size < num_of_items:
            batch = {
                'RequestItems': {
                    TABLE_NAME: ddb_batch[last_chunk*chunk_size:num_of_items]
                }
            }
            # batch_threads.append(threading.Thread(
            #     target=batch_write_in_jwt_dishes, args=(batch,)))
            # batch_threads[-1].start()
            self.batch_write_in_jwt_dishes(batch)
        
        

    def batch_write_in_jwt_dishes(self, batch):
        try:
            response = dynamodb.batch_write_item(
                RequestItems=batch['RequestItems'])
        except Exception as e:
            print('++++++exception while writing ddb',e)
            # return {'statusCode': 400, 'data': json.dumps(e.response['Error']['Message'])}
        else:
            print('+++++success+++++ to ddb')