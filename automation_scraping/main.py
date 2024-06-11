import os
import requests
from airtable import Airtable
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

logs_path = "./"

def log(message):
    try:
        message = "{0:%Y-%m-%d %H:%M:%S} {1}".format(datetime.now(), message)
        print(message)
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)
        fileName = "{0}/{1}.{2:%m%d%y}.log"
        fileName = fileName.format(logs_path, "automation", datetime.now())
        with open(fileName, "a") as file:
            file.write(str(message) + "\n")
    except Exception as err:
        print(err)


class AirtableManager:
    def __init__(self):
        # Airtable keys
        self.airtable_api_key = os.getenv("API_KEY")
        self.airtable_base_id = os.getenv("BASE_ID")
        self.airtable_product = os.getenv("TABLE")
        

    def get_url_list(self):
        airtable = Airtable(self.airtable_base_id, self.airtable_product, api_key=self.airtable_api_key)
        result = airtable.get_all(formula="NOT({Status})")
        url_list = [{'id': record['id'], 'url': record['fields'].get('Source URL')} for record in result if 'Source URL' in record['fields']]
       
        return url_list


    def update_status(self, record_id, status):
        try:
            airtable = Airtable(self.airtable_base_id, self.airtable_product, api_key=self.airtable_api_key)
           
            if record_id and status:
                update_result = airtable.update(record_id, {'Status': status})
                log(f"Updated record {record_id} with status: {status}")
                return update_result
            else:
                log(f"Record id or status not found")
        except Exception as e:
            log(f"Error in update in airtable:{e}")

def main():
    manager = AirtableManager()
    url_list = manager.get_url_list()
    if url_list:
        for item in url_list:
            record_id = item['id']
            url = item['url']
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract the text of the element with the specific id
                stock_status = soup.find(id="ctl00_contentBody_lblStockStatus")
                if stock_status:
                    status_text = stock_status.get_text().strip()
                    if status_text:
                        log(f"Status of Stock:{status_text}")
                        manager.update_status(record_id, status_text)
                        log(f"Record update successfully for Url:{url}")
                    else:
                        stock_status1 = soup.find(id="ctl00_contentBody_pnlDiscontinued")
                        status_text1 = stock_status1.get_text().strip()
                        log(f"Status of Stock:{status_text1}")
                        manager.update_status(record_id, status_text1)
                        log(f"Record update successfully for Url:{url}")
                else:
                    log(f"Element with id 'ctl00_contentBody_lblStockStatus' not found.{url}")
            else:
                log(f"Failed to retrieve the page. Status code: {response.status_code}")
                log(f"Failed to retrieve the page url:{url}")
    else:
        log("No URLs found in the Airtable data.")

if __name__ == "__main__":
    main()