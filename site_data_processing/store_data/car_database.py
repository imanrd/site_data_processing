import mysql.connector
from . import database

DB_NAME = 'CAR_DB'
TABLE_NAME = 'car'


def insert(data):
    cnx = mysql.connector.connect(user='admin', password='')
    cursor = cnx.cursor()
    cursor.execute(f"USE {DB_NAME}")
    stmt = f"INSERT IGNORE INTO  {TABLE_NAME} (vin, model, price, year, mileage) VALUES (%s, %s, %s, %s, %s) "
    try:
        cursor.executemany(stmt, data)
    except Exception as e:
        print(e)
    cnx.commit()
    return


def create():
    TABLES = {}

    TABLES[TABLE_NAME] = (
        f"CREATE TABLE {TABLE_NAME} ("
        "  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,"
        "  `vin` varchar(50) NOT NULL UNIQUE,"
        "  `model` varchar(50) NOT NULL,"
        "  `price` int(10) NOT NULL,"
        "  `year` int(10) NOT NULL,"
        "  `mileage` int(10) NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    database.DataBase(DB_NAME, TABLES)
