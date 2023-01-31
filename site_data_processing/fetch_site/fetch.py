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
