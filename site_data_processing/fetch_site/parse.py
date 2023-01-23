import re
import concurrent.futures
from bs4 import BeautifulSoup


def parse_model(car):
    return car.select_one('span[class="truncate"]').text


def parse_price(car):
    price_text = car.select_one('[class="heading-3 my-1 font-bold"]').text
    price_text = re.sub('\\$', '', price_text)
    price_text = re.sub(',', '', price_text)
    return int(price_text)


def parse_year(car):
    return int(car.select_one('span[class="vehicle-card-year text-xs"]').text)


def parse_mileage(car):
    miles_text = car.select_one('div[class="flex w-full justify-between"]').text
    miles_text = re.sub(',', '', miles_text)
    miles_list = re.findall(r'\d+', miles_text)
    return int(''.join(miles_list))


def parse(page):
    car_list = []
    soup = BeautifulSoup(page.text, 'html.parser')
    for car in soup.select('[class="linkable card card-shadow vehicle-card"]'):
        model = parse_model(car)
        price = parse_price(car)
        year = parse_year(car)
        mileage = parse_mileage(car)
        car_data = {'model': model,
                    'price': price,
                    'year': year,
                    'mileage': mileage}
        car_list.append(car_data)
        print(car_data)
    return car_list


def concurrent_parse(pages):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(parse, pages))
    whole_data = [car for car_list in results for car in car_list]
    print(len(whole_data))
    return whole_data
