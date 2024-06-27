import supabase


supabase_url = 'https://wzbzlbdggcymevtwcjqw.supabase.co'
supabase_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind6YnpsYmRnZ2N5bWV2dHdjanF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTkyOTgxNzIsImV4cCI6MjAzNDg3NDE3Mn0.3HefuULy4d1f-QmEGb4kC-pcxQBKIM4TRSZaB8TDJdo'
supabase_client = supabase.Client(supabase_url, supabase_key)

def insert_data_by_sp():
    response = supabase_client.rpc('sp_insert_data', params).execute()
    print(response)
    return response
   
def select_data():
    response = supabase_client.table('students').select('*').execute()
    return response.data

def insert_data(file_data,table_name):
    response = supabase_client.table(table_name).insert(file_data).execute()
    return response
    
if __name__ == "__main__":
    params = {'v_name': 'zaidi','v_class': '10th Grade','v_rollno': 199,'v_dob': '2005-05-15'}
    #res=insert_data_by_sp(params)
    #res=select_data()
    #res=insert_data()
    
