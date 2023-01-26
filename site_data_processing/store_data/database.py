import mysql.connector
from mysql.connector import errorcode


class DataBase:
    def __init__(self, name, tables):
        self.NAME = name
        self.TABLES = tables
        self.cnx = mysql.connector.connect(user='admin', password='')
        self.cursor = self.cnx.cursor()
        self.use_database()
        self.create_tables()
        self.cursor.close()
        self.cnx.close()

    def use_database(self):
        try:
            self.cursor.execute(f"USE {self.NAME}")
        except mysql.connector.Error as err:
            print(f"Database {self.NAME} does not exists.")
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database()
                print(f"Database {self.NAME} created successfully.")
                self.cnx.database = self.NAME
            else:
                print(err)
                exit(1)
        return

    def create_database(self):
        try:
            self.cursor.execute(
                f"CREATE DATABASE {self.NAME} DEFAULT CHARACTER SET 'utf8'")
        except mysql.connector.Error as err:
            print(f"Failed creating database: {err}")
            exit(1)
        return

    def create_tables(self):
        for table_name in self.TABLES:
            table_description = self.TABLES[table_name]
            print(table_description)
            try:
                print(f"Creating table {table_name}: ", end='')
                self.cursor.execute("".join(table_description))
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        return


if __name__ == '__main__':
    DB_NAME = 'employersed'
    TABLES = {}
    TABLES['employees'] = (
        "CREATE TABLE `employees` ("
        "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
        "  `birth_date` date NOT NULL,"
        "  `first_name` varchar(14) NOT NULL,"
        "  `last_name` varchar(16) NOT NULL,"
        "  `gender` enum('M','F') NOT NULL,"
        "  `hire_date` date NOT NULL,"
        "  PRIMARY KEY (`emp_no`)"
        ") ENGINE=InnoDB")

    TABLES['departments'] = (
        "CREATE TABLE `departments` ("
        "  `dept_no` char(4) NOT NULL,"
        "  `dept_name` varchar(40) NOT NULL,"
        "  PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)"
        ") ENGINE=InnoDB")

    TABLES['salaries'] = (
        "CREATE TABLE `salaries` ("
        "  `emp_no` int(11) NOT NULL,"
        "  `salary` int(11) NOT NULL,"
        "  `from_date` date NOT NULL,"
        "  `to_date` date NOT NULL,"
        "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
        "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
        "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
        ") ENGINE=InnoDB")

    TABLES['dept_emp'] = (
        "CREATE TABLE `dept_emp` ("
        "  `emp_no` int(11) NOT NULL,"
        "  `dept_no` char(4) NOT NULL,"
        "  `from_date` date NOT NULL,"
        "  `to_date` date NOT NULL,"
        "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
        "  KEY `dept_no` (`dept_no`),"
        "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
        "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
        "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
        "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
        ") ENGINE=InnoDB")
    DataBase(DB_NAME, TABLES)
