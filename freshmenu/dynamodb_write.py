from config import table
from botocore.exceptions import ClientError
class DynamoDBWrite:
    def __init__(self):
        pass
    def dynamodb_write(self, restaurant_obj):
        print("DYNMOOOOOOOOOOOOOOOO++++++")
        try:
            response = table.put_item(
                Item=restaurant_obj
            )
        except ClientError as e:
            print('+++client erroe',e.response['Error']['Message'])
        except Exception as e:
            print('++other exception',e)
        else:
            print('++++ADDED TO DDB')