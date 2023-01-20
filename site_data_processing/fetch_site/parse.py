import re
import requests
from bs4 import BeautifulSoup


class PageParser:
    data = []

    def __init__(self, page_text: requests) -> None:
        self.page = page_text
        self.card = None

    @staticmethod
    def parse_model(car):
        return car.select_one('span[class="truncate"]').text

    @staticmethod
    def parse_price(car):
        price_text = car.select_one('[class="heading-3 my-1 font-bold"]').text
        price_text = re.sub('\\$', '', price_text)
        price_text = re.sub(',', '', price_text)
        return int(price_text)

    @staticmethod
    def parse_year(car):
        return int(car.select_one('span[class="vehicle-card-year text-xs"]').text)

    @staticmethod
    def parse_mileage(car):
        miles_text = car.select_one('div[class="flex w-full justify-between"]').text
        miles_text = re.sub(',', '', miles_text)
        miles_list = re.findall(r'\d+', miles_text)
        return int(''.join(miles_list))

    def parse(self):
        soup = BeautifulSoup(self.page.text, 'html.parser')
        for car in soup.select('[class="linkable card card-shadow vehicle-card"]'):
            model = self.parse_model(car)
            price = self.parse_price(car)
            year = self.parse_year(car)
            mileage = self.parse_mileage(car)
            car_data = {'model': model,
                        'price': price,
                        'year': year,
                        'mileage': mileage}
            PageParser.data.append(car_data)
            print(car_data)
        return


if __name__ == '__main__':
    for i in range(1, 6):
        r = requests.get(f'https://www.truecar.com/used-cars-for-sale/listings/?page={i}')
        if r.status_code == 200:
            print(r)
            parser = PageParser(r)
            parser.parse()
    info = PageParser.data
    print(info)
    print(len(info))
