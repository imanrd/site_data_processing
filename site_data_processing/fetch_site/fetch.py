import parse
import requests
import threading

import concurrent.futures


thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(site):
    session = get_session()
    print(site)
    with session.get(site) as response:
        return response


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as executor:
        return executor.map(download_site, sites)


if __name__ == '__main__':
    list_of_urls = [f'https://www.truecar.com/used-cars-for-sale/listings/?page={page}' for page in range(1, 10)]
    all_sites = download_all_sites(list_of_urls)
    print('Download is complete')

    parsing = parse.concurrent_parse(all_sites)
    print(parsing)
