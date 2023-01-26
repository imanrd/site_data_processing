import mysql.connector
from site_data_processing import fetch_site
import database

DB_NAME = 'CAR_DB'
table = 'car'


def insert(data):
    cnx = mysql.connector.connect(user='admin', password='')
    cursor = cnx.cursor()
    cursor.execute(f"USE {DB_NAME}")
    stmt = f"INSERT INTO  {table} (id, model, price, year, mileage) VALUES (%s, %s, %s, %s, %s) " \
           f"ON DUPLICATE KEY UPDATE id=%s"
    try:
        cursor.executemany(stmt, data)
    except Exception as e:
        print(e)
    cnx.commit()
    return


def create():
    TABLES = {}

    TABLES['car'] = (
        "CREATE TABLE `car` ("
        "  `id` varchar(50) NOT NULL ,"
        "  `model` varchar(50) NOT NULL,"
        "  `price` int(10) NOT NULL,"
        "  `year` int(10) NOT NULL,"
        "  `mileage` int(10) NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    database.DataBase(DB_NAME, TABLES)


if __name__ == '__main__':
    list_of_urls = [f'https://www.truecar.com/used-cars-for-sale/listings/?page={page}' for page in range(1, 25)]
    all_sites = fetch_site.fetch.download_all_sites(list_of_urls)
    print('Download is complete')

    parsing = fetch_site.parse.concurrent_parse(all_sites)

    print(parsing)

    parsed = [tuple(dic.values()) for dic in parsing]

    print(parsed)

    print('Parsing is complete')

    create()

    insert(parsed)
