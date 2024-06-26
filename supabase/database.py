import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def insert_data(table_name, data):
    response = (supabase.table(table_name).insert(data).execute())
    return response

def get_data(table_name):
    response = supabase.table(table_name).select("*").execute()
    return response

def call_function(fn_name): 
    response = supabase.rpc(fn_name).execute()
    return response
    

def main():
    # res = insert_data("Countries", {"id": 3, "country": "Denmark"})
    # data = get_data("Countries")
    fn_res = call_function("test")
    print(fn_res)

if __name__ == '__main__':
    main()
    