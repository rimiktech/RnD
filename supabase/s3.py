import boto3 
import supabase 
from io import BytesIO
import datetime
import pandas as pd
from pytz import timezone
import re  
import io




endpoint_url = 'https://wzbzlbdggcymevtwcjqw.supabase.co/storage/v1/s3'
access_key = '16c5de30ae9f236719e0d89719266e9e'
secret_key = 'ab09c3145cf4301ac1c1fc311a09e659aaf0cd12dd228846f750ba76cb95ee80'
supabase_url = 'https://wzbzlbdggcymevtwcjqw.supabase.co'
supabase_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind6YnpsYmRnZ2N5bWV2dHdjanF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTkyOTgxNzIsImV4cCI6MjAzNDg3NDE3Mn0.3HefuULy4d1f-QmEGb4kC-pcxQBKIM4TRSZaB8TDJdo'

file='TradingScanner_B1_VM43_20240426030742_Long_1200.scn'
bucket_name='testcsv'
local_file_path='C:\\Users\\Hp\\Downloads\\_042424_ED_STOCKS.scn'
Table_name='analysis_data'

s3 = boto3.client('s3', endpoint_url=endpoint_url,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
supabase_client = supabase.Client(supabase_url, supabase_key)

def read_file():
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file)
        csv_file_content = obj['Body'].read()
        csv_file_obj = BytesIO(csv_file_content)
        print(csv_file_obj)
        csv_content = csv_file_obj.getvalue().decode('utf-8')
        Eastern_US_time = datetime.datetime.now(timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")
        file_data = []
        # Using regular expressions to find content between <Scan Save v2.0> and </Scan Save>
        match = re.search(r'<Scan Save v2\.0>(.*?)</Scan Save>', csv_content, re.DOTALL)
        if match:
            content_between_tags = match.group(1)
            dfs = pd.read_csv(io.StringIO(content_between_tags), header=None)
            # Parsing file name to extract date and time
            file_parts = file.split('_')
            datetime_obj = datetime.datetime.strptime(file_parts[3], '%Y%m%d%H%M%S')
            for index, row in dfs.iterrows():
                # Mapping values from the DataFrame
                ANALYSIS_DATE_TIME = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')  # Parse after the third underscore
                CURRENT_DATE_TIME = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')  # Parse after the third underscore
                SECURITY_NAME = row[0]
                SYMBOL = row[0]
                ITEM_INTERVAL = "Minutes" if row[0].split('_')[-1].isnumeric() else "Daily"
                DIRECTION = file_parts[4]     # Parse after the fifth underscore
                PATTERN_TYPE = row[3]
                SCAN_WAVE_NUMBER = row[4]
                SCREEN_SHOT_PATH_INITIAL = row[9]
                SCREEN_SHOT_PATH_CURRENT = row[9]
                SOURCE = file_parts[1]  
                BARS_LOADED = file_parts[5].replace('.scn', '') 
                BARS_DISPLAYED = file_parts[5].replace('.scn', '') 
                # Hardcoded values
                ITEM_ID = "0000"
                HIDDEN_WAVES = "1"
                PATTERN_FILTER = "Ending Diagonal (ED)"
                DATETIME_RECORD_CREATED = Eastern_US_time
                STATUS = "Pending"
                CREATED_WITH_AUTO_TRADER = "0"
                CREATED_IN_SIMPLE_MODE = "0"
                file_data.append({
                    'ANALYSIS_DATE_TIME' : ANALYSIS_DATE_TIME,
                    'CURRENT_DATE_TIME' : CURRENT_DATE_TIME,
                    'SECURITY_NAME': SECURITY_NAME,
                    'SYMBOL': SYMBOL,
                    'ITEM_INTERVAL': ITEM_INTERVAL,
                    'DIRECTION': DIRECTION,
                    'PATTERN_TYPE': PATTERN_TYPE,
                    'SCAN_WAVE_NUMBER': SCAN_WAVE_NUMBER,
                    'SCREEN_SHOT_PATH_INITIAL': SCREEN_SHOT_PATH_INITIAL,
                    'SCREEN_SHOT_PATH_CURRENT': SCREEN_SHOT_PATH_CURRENT,
                    'SOURCE': SOURCE,
                    'BARS_LOADED': BARS_LOADED,
                    'BARS_DISPLAYED': BARS_DISPLAYED,
                    'ITEM_ID': ITEM_ID,
                    'HIDDEN_WAVES': HIDDEN_WAVES,
                    'PATTERN_FILTER': PATTERN_FILTER,
                    'DATETIME_RECORD_CREATED': DATETIME_RECORD_CREATED,
                    'STATUS': STATUS,
                    'CREATED_WITH_AUTO_TRADER': CREATED_WITH_AUTO_TRADER,
                    'CREATED_IN_SIMPLE_MODE': CREATED_IN_SIMPLE_MODE
                })     
        else:
            print("<Scan Save v2.0> and </Scan Save> Pattern not found in the content.")
    
        if file_data:
            response = supabase_client.table(Table_name).insert(file_data).execute()
            print(response)
            print('Data inserted successfully:',)
        else:
            print("No data to insert.")
    except Exception as e:
        print(f'Error: {e}')




if __name__ == "__main__":
    read_file()
