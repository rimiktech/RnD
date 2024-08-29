import os
import time
import dateparser
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from airtable import Airtable

# Airtable configuration
AIRTABLE_BASE_ID = 'apprRoN4AnjIokL4p'
AIRTABLE_API_KEY = 'patQRtHf3kXuLceyW.4a5362f890bdc06343390ced8d1c62772460a82ff0f65b0986273c7ad88e0643'
AIRTABLE_TABLE_NAME = 'Airbnb Reviews'
AIRTABLE_TABLE_LISTINGS="Listings"
airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, api_key=AIRTABLE_API_KEY)

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
def get_all_listing():
    airtable1 = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_LISTINGS, api_key=AIRTABLE_API_KEY)
    records = airtable1.get_all(fields=['Listing ID', 'Listing URLS'])
    listing_urls = [record['fields']['Listing URLS'] for record in records if 'Listing URLS' in record['fields']]
    listing_ids = [record['fields']['Listing ID'] for record in records if 'Listing ID' in record['fields']]
    print(f"------------:{len(listing_ids)}")
    return listing_urls,listing_ids

def update_listing(listing_id, total_review_found):
    try:
        log(f"-------------------{listing_id,total_review_found}")
        airtable1 = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_LISTINGS, api_key=AIRTABLE_API_KEY)
        records = airtable1.get_all(formula=f"{{Listing ID}} = '{listing_id}'")  
        if records:
            record_id = records[0]['id']  # Get the Airtable record ID
            update_data = {
                "No of Review": total_review_found
            }
            airtable1.update(record_id, update_data)
            log(f"Updated the 'No of Review' in the listing table for Listing ID: {listing_id}")
        else:
            log(f"No record found with Listing ID: {listing_id}")    
    except Exception as e:
        log(f"Failed to update the 'No of Review' for Listing ID: {listing_id}. Error: {e}")


def save_to_airtable(data_batch):
    try:
       
        airtable.batch_insert(data_batch, typecast=True)
        log("Data batch saved to Airtable successfully!")
    except Exception as e:
        log(f"Failed to save data to Airtable: {e}")


def load_all_listings(driver):
    while True:
        try:
            log(f"Loading listing....")
            show_more_button = driver.find_element(By.CSS_SELECTOR, 'div.lk34ed1 button')
            driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
            show_more_button.click()
            time.sleep(3)  # Wait for listings to load
        except Exception as e:
            log(f"No more listings to load or error occurred:{e}")
            break

def main():
    try:
     

        all_listing, listing_ids = get_all_listing()
        data_batch = []  # List to hold batch data
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument("--no-sandbox")  # Disable sandboxing
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        driver = webdriver.Chrome(options=chrome_options)

        for i, (url, listing_id) in enumerate(zip(all_listing, listing_ids)):
            # if i == 5:
            #     break
       
            url = f"https://www.airbnb.ae/{url}"
            driver.get(url)
            time.sleep(3)
            source_page = driver.page_source
            soup = BeautifulSoup(source_page, 'html.parser')

            try:
                list_title = driver.find_element(By.CLASS_NAME, "_1xxgv6l").text
                div_element = driver.find_element(By.CSS_SELECTOR, 'div.rk4wssy')
                a_tag = div_element.find_element(By.TAG_NAME, 'a')

                if a_tag:
                    a_tag.click()
                    time.sleep()
                    review_url = driver.current_url
                    log(f"Review url for review: {review_url}")
                    source_page = driver.page_source
                    soup = BeautifulSoup(source_page, 'html.parser')
                    divs1 = soup.find_all('div', class_='r1are2x1')
                    log(f"Total review found: {len(divs1)}")

                    for review in divs1:
                        reviewer_name = review.find('h2').text
                        reviewer_comment = review.find(
                            'span', class_="lrl13de atm_kd_19r6f69_24z95b atm_kd_19r6f69_1xbvphn_1oszvuo dir dir-ltr"
                        ).text
                        review_rating = review.find(
                            'div', class_="c5dn5hn atm_9s_1txwivl atm_cx_t94yts dir dir-ltr"
                        ).text
                        review_date = review.find(
                            class_="s78n3tv atm_c8_1w0928g atm_g3_1dd5bz5 atm_cs_10d11i2 atm_9s_1txwivl atm_h_1h6ojuz dir dir-ltr"
                        ).text.split("·")[1].strip()
                        review_date = review_date.rstrip(',')
                        parsed_date = dateparser.parse(review_date)
                        formatted_date = parsed_date.strftime("%B %Y") if parsed_date else "Invalid Date"
                        review_location = review.find(
                            class_="s15w4qkt atm_c8_1w0928g atm_g3_1dd5bz5 atm_cs_6adqpa atm_7l_1wzk1hz dir dir-ltr"
                        ).text
                        #total_review_found = review.find("div", class_="_s9zd43").text

                        data = {
                            "Listing ID": listing_id,
                            "Listing Title": list_title,
                            "Reviewer Name": reviewer_name,
                            "Reviewer Location": review_location,
                            "Review Date": formatted_date,
                            "Review Comments": reviewer_comment,
                            "Review Rating": review_rating,
                            "Review URL": review_url,
                        }

                        data_batch.append(data)
                       
                        # Insert batch every 10 records
                        
                    save_to_airtable(data_batch)
                    data_batch.clear()     
                    update_listing(listing_id, len(divs1))
                else:
                    log(f"No review found fo ---------------r: {url}")
                    continue
            except Exception as ee:
                print(ee)
                #update_listing(listing_id, "No Review Found")
                log(f"No review found for: {url}")
                continue

    except Exception as e:
        log(f"An error occurred: {e}")

if __name__ == "__main__":
    #url = "https://www.airbnb.ae/users/show/74933177"
    main()