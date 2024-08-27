import os
import time
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
 
 
#TEST ACCOUNT
# AIRTABLE_BASE_ID = 'appnjCm9aFRId8lxr'
# AIRTABLE_API_KEY = 'patiiPih4ERBsP9qI.2b9c1d9df084f42a04fa6c311a738ba8765a22a9591b14fc5a6114b960bcdd5a'
# AIRTABLE_TABLE_NAME = 'Review'
 
 
 
# Initialize Airtable
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
 
 
 
def check_duplicate(listing_id, review_date):
    """Check if the record with the given listing_id and review_date already exists in Airtable."""
    log(f"Checking for duplicate entry for Listing ID: {listing_id}, Review Date: {review_date}.")
    try:
        formula = f"AND({{Listing ID}} = '{listing_id}', {{Review Date}} = '{review_date}')"
        records = airtable.get_all(formula=formula)
        return len(records) > 0
    except Exception as e:
        log(f"Error checking for duplicate: {e}")
        return False
 
def save_to_airtable(data):
    try:
        airtable.insert(data)
        log("Data saved to Airtable successfully!")
    except Exception as e:
        log(f"Failed to save data to Airtable: {e}")
 
def load_all_listings(driver):
    while True:
        try:
            # Try to find the "Show More" button and click it
            show_more_button = driver.find_element(By.CSS_SELECTOR, 'div.lk34ed1 button')
            log(f"!!!!!!!!!!!!!!!!!!!!!!!!!{show_more_button}")
            driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
            show_more_button.click()
            time.sleep(3)  # Wait for listings to load
        except Exception as e:
            log(f"No more listings to load or error occurred:{e}")
            break
 
def main(url):
    try:
        chrome_options = webdriver.ChromeOptions()
        # Set up Chrome options
        chrome_options.add_argument("--headless")  # Headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument("--no-sandbox")  # Disable sandboxing (useful for headless mode)
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        #chrome_options.add_argument("--remote-debugging-port=9222")  # Remote debugging port (optional)
 
 
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5)
 
        # Click the button to open the popup window
        button = driver.find_element(By.CSS_SELECTOR, 'div.v1ubu2ue button')
        button.click()
       
        time.sleep(5)  # Wait for popup window to load
 
        # Load all listings by clicking "Show More" button until it's no longer available
        load_all_listings(driver)
 
        source_page = driver.page_source
        soup = BeautifulSoup(source_page, 'html.parser')
       
        # Find all divs with class "gm62wvj"
        divs = soup.find('div', class_='gm62wvj')
        all_listing = divs.find_all('a')
        log(f"Total listed title: {len(all_listing)}")
       
        for item in all_listing:
            review_link = item.get('href')
            listing_id = review_link.split('/')[2].split('?')[0]
            log(f"Review listed id: {listing_id}")
 
            driver.get(f"https://www.airbnb.ae/{review_link}")
            time.sleep(2)
            # try:
            #     dismiss_button = driver.find_element(By.CSS_SELECTOR, 'div.c1lbtiq8 button')
            #     dismiss_button.click()
            #     log("Dismissed the popup.")
            # except Exception as e:
            #     log("Dismiss button not found, proceeding:", e)
            #     # Proceed with the next steps or find another button if needed
            list_title = driver.find_element(By.CLASS_NAME, "_1xxgv6l").text
           
            div_element = driver.find_element(By.CSS_SELECTOR, 'div.rk4wssy')
           
       
            try:
               
                a_tag = div_element.find_element(By.TAG_NAME, 'a')
                if a_tag:
                    a_tag.click()
                    review_url = driver.current_url
                    log(f"Review url for review: {review_url}")
                    source_page = driver.page_source            
                    soup = BeautifulSoup(source_page, 'html.parser')
                    divs1 = soup.find_all('div', class_='r1are2x1')
                    log(f"Total review found:{len(divs1)}")
                   
                    for review in divs1:
                        reviewer_name = review.find('h2').text
                       
                        reviewer_comment = review.find('span', class_="lrl13de atm_kd_19r6f69_24z95b atm_kd_19r6f69_1xbvphn_1oszvuo dir dir-ltr").text
                        review_rating = review.find('div', class_="c5dn5hn atm_9s_1txwivl atm_cx_t94yts dir dir-ltr").text
                        review_date = review.find(class_="s78n3tv atm_c8_1w0928g atm_g3_1dd5bz5 atm_cs_10d11i2 atm_9s_1txwivl atm_h_1h6ojuz dir dir-ltr").text.split("·")[1].strip()
                        review_location = review.find(class_="s15w4qkt atm_c8_1w0928g atm_g3_1dd5bz5 atm_cs_6adqpa atm_7l_1wzk1hz dir dir-ltr").text
                        if check_duplicate(listing_id, review_date):
                            log(f"Duplicate found for Listing ID: {listing_id}, Review Date: {review_date}. Skipping...")
                            continue
                        # Prepare the data for Airtable
                        data = {
                            "Listing ID": listing_id,
                            "Listing Title": list_title,
                            "Reviewer Name": reviewer_name,
                            "Reviewer Location": review_location,
                            "Review Date": review_date,
                            "Review Comments": reviewer_comment,
                            "Review Rating": review_rating,
                            "Review URL": review_url
                        }
                       
                        save_to_airtable(data)
                       
 
                else:
                    continue
            except Exception as ee:
               
                continue      
    except Exception as e:
        log(f"An error occurred: {e}")
       
   
    finally:
        driver.quit()
 
if __name__ == "__main__":
    url = "https://www.airbnb.ae/users/show/74933177"
    main(url)