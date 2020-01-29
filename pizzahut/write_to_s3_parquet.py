import pandas as pd
import s3fs
from fastparquet import write
from config import parquet_file_path

class WriteS3Parquet:

    def __init__(self,city):
        
        self.city = city

    def write_to_parquet(self, restaurant_obj):
        df = pd.DataFrame(restaurant_obj)
        print('++++++',df)
        s3 = s3fs.S3FileSystem()
        myopen = s3.open

        try:
            write(
                parquet_file_path+self.city+'.parq.gzip',
                df,
                compression='GZIP',
                open_with=myopen
            )
            print('+++written to parquet')
        except Exception as e:
            print('+++exception while writing to parquet',e)
        