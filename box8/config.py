import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
TABLE_NAME = "JWT_DISHES"
table = dynamodb.Table(TABLE_NAME)
parquet_file_path = 'jwt-parquet/parquet_files/india/'