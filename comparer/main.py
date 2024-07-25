import os
import numpy as np
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
pd.set_option('future.no_silent_downcasting', True)
load_dotenv()

LOGS_PATH = "./logs"
TABLE_NAME = "trading_journal_source_t1"
CSV_FILE_PATH = "./data/ctr_must_start_from_ptr_target_hit_preview_all_minuteTimeframes.csv"

class Database:
    
    def __init__(self):
        self.h = os.getenv("HOST")
        self.u = os.getenv("USER")
        self.p = os.getenv("PASSWORD")
        self.db = os.getenv("DATABASE_NAME")
        self.port = int(os.getenv("PORT"))
        self.connection = create_engine(self.get_db_connection(), pool_recycle=3600)
        
    def get_db_connection(self):
        return "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(self.u, self.p, self.h, self.port, self.db)          

    #get table as pandas
    def get(self, query):
        dbConnection = self.connection.connect()
        try:
            frame = pd.read_sql(query, dbConnection)  
            return frame
        except Exception as ex:   
            print(ex)
            return None
        finally:
            dbConnection.close()

def log(message):
    try:
        message = "{0:%Y-%m-%d %H:%M:%S} {1}".format(datetime.now(), message)
        print(message)
        if not os.path.exists(LOGS_PATH): os.makedirs(LOGS_PATH)
        fileName = "{0}/{1}.{2:%m%d%y}.log"
        fileName = fileName.format(LOGS_PATH, os.path.basename(__file__), datetime.now())
        with open(fileName, "a") as file:
            file.write(str(message) + "\n")
    except Exception as err:
        print(err)

def get_csv_data():
    log("Reading {0} csv file...".format(os.path.basename(CSV_FILE_PATH)))
    csv_data = pd.read_csv(CSV_FILE_PATH)
    min_id = csv_data['RECORD_ID'].min() 
    max_id = csv_data['RECORD_ID'].max() 
    log("There are total {0} records in the file.".format(len(csv_data)))
    return csv_data, min_id, max_id

def get_data_from_database(min_id, max_id):
    log("Getting all the records from the {0} table between {1} and {2} IDs.".format(TABLE_NAME, min_id, max_id))
    query = "SELECT * FROM {0} where RECORD_ID BETWEEN {1} and {2};".format(TABLE_NAME, min_id, max_id)
    database_df = Database().get(query)
    database_df = database_df.fillna(value=np.nan)
    log("Got {0} records.".format(len(database_df)))
    return database_df

def compare(row):
    if pd.isna(row['PATTERN']) and pd.isna(row['pattern']):
        return True
    return row['PATTERN'] == row['pattern']

def pattern_difference(database_df, csv_data):
    log("Merging both dataframes...")
    merged_df = pd.merge(database_df, csv_data, on='RECORD_ID', how='inner', suffixes=('_DATABASE', '_CSV'))
    log("Got {0} common records in both dataframes after merging.".format(len(merged_df)))
    log("Comparing both patterns...")
    merged_df['PATTERN_MATCHED'] = merged_df.apply(compare, axis=1)
    log("{0} records have matching patterns, and {1} records have non-matching patterns".format(merged_df['PATTERN_MATCHED'].sum(), (~merged_df['PATTERN_MATCHED']).sum()))
    return merged_df

def main():
    log("Srcipt starting...")
    csv_df, min_id, max_id = get_csv_data()
    database_df = get_data_from_database(min_id, max_id)
    diff_df = pattern_difference(database_df, csv_df)

    log("Generating result's csv...")
    diff_df.to_csv('compared_records.csv', index=False)
    log("Completed.")

if __name__ == '__main__':
    main()
    