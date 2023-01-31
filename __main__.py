import sys
import requests.exceptions
from site_data_processing.fetch_site import fetch
from site_data_processing.fetch_site import parse
from site_data_processing.store_data import car_database
from site_data_processing.ml import car_price_estimator


list_of_urls = [f'https://www.truecar.com/used-cars-for-sale/listings/?page={page}' for page in range(1, 334)]
try:
    all_sites = fetch.download_all_sites(list_of_urls)
except KeyboardInterrupt:
    print('If you are using Iran\'s internet Please download up to 30 pages each time!')
    sys.exit()
except requests.exceptions.SSLError:
    print('Connection Error!')
    sys.exit()
print('Download is complete')


parsed = parse.concurrent_parse(all_sites)

print('Parsing is complete')


car_database.create()

car_database.insert(parsed)

print('Data is stored in database')


car_price_estimator.main()

print('Done')
