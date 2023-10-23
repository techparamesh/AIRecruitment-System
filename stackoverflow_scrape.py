from utils import records_insertion, collection_creation, count_records
import requests
import requests_cache
import time
import re
from IPython.display import clear_output


# Fucntion to fetch candidates data from the stackexchange API
def fetch_api_data(page: int):
    candidates_url = f'https://api.stackexchange.com/2.3/users?page={page}&pagesize=100&order=desc&sort=modified&site=stackoverflow&filter=!56ApJn82ELRG*IWQxo6.gXu9qS90qXxNmY8e9b'
    response = requests.get(candidates_url)
    return response


# Create Cache
requests_cache.install_cache(cache_name = 'stackoverflow_cache', backend = 'sqlite', expire_after = 6000)

# Create Collection on Mongodb
stackoverflow_scraped_data = collection_creation("Stackoverflow_Scraped")

# Empty list to save records
results = []

# Requesting data until page 25 (25 pages becasue of API limit without key)
for i in range(1, 5):
    print(f"Requesting page {i}/{25}")

    # Get Data
    response = fetch_api_data(i)
    result = response.json()

    # Save the candidates
    for candidate in result['items']:
        candidate['_id'] = candidate.pop('user_id')
        candidate['email'] = 'pythonproject2023test@gmail.com'
        results.append(candidate)

    # Print if results came from cache or not
    now = time.ctime(int(time.time()))
    using_cache = response.from_cache
    print(f'Time: {now} / Used Cache: {using_cache}')
    clear_output(wait=True)

    # If the result is not in cache, sleep to avoid too many rapid API requests to Stack Exchange
    if not using_cache and result.get('has_more'):
            time.sleep(11)
    else:
        break

# Insert records into MongoDB
before_insertion_count = count_records(stackoverflow_scraped_data)
records_insertion(results, stackoverflow_scraped_data)
after_insertion_count = count_records(stackoverflow_scraped_data)
print(f"There are a total of {after_insertion_count-before_insertion_count} new records in mongoDB")