from utils import records_insertion, collection_creation, count_records
import requests
import requests_cache
import time
import re 
from concurrent.futures import ThreadPoolExecutor 
from IPython.display import clear_output

requests_cache.clear()

# Fucntion to fetch candidates data from the stackexchange API
def fetch_api_data(page: int):
    candidates_url = f'https://api.stackexchange.com/2.3/users?page={page}&pagesize=100&order=desc&sort=modified&site=stackoverflow&filter=!56ApJn82ELRG*IWQxo6.gXu9qS90qXxNmY8e9b'
    response = requests.get(candidates_url)
    return response

# Create Cache
requests_cache.install_cache(cache_name = 'stackoverflow_cache', backend = 'sqlite', expire_after = 6000)

# Create Collection on Mongodb
stackoverflow_scraped_data = collection_creation("Stackoverflow_Scraped")

# Function to process data after fetching it from 25 pages (25 pages becasue of API limit without key)
def process_api_data(page):
    print(f"Requesting page {page}/{25}")
    response = fetch_api_data(page)
    result = response.json()

    if 'items' in result:
        records = []

        for candidate in result['items']:
            candidate['_id'] = candidate.pop('user_id')
            candidate['email'] = 'pythonproject2023test@gmail.com'
            records.append(candidate)

        now = time.ctime(int(time.time()))
        using_cache = response.from_cache
        print(f'Time: {now} / Used Cache: {using_cache}')
        clear_output(wait=True)

        if not using_cache and result.get('has_more'):
            time.sleep(11)

        return records
    else:
        print(f"Error while fetching page {page}: {result.get('error_message')}")
        return []

# Fetch data using multithreading
results = []
max_pages = 25

with ThreadPoolExecutor(max_pages) as executor:
    pages = [executor.submit(process_api_data, i) for i in range(1, max_pages + 1)]
    
    for page in pages:
        results.extend(page.result())

# Insert records into MongoDB
before_insertion_count = count_records(stackoverflow_scraped_data)
records_insertion(results, stackoverflow_scraped_data)
after_insertion_count = count_records(stackoverflow_scraped_data)
print(f"There are {after_insertion_count - before_insertion_count} new records inserted in MongoDB collection")