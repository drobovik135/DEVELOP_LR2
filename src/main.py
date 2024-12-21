import configparser
import psycopg2

from .dataBaseInit.dataBaseInit import init_table

def connect_by_conf(file):
    config = configparser.ConfigParser()
    config.read(file)

    return psycopg2.connect(
        dbname=config['database']['dbname'],
        user=config['database']['user'],
        password=config['database']['password'],
        host=config['database']['host'],
        port=config['database']['port']
    )


def main():
    conn = connect_by_conf("config.ini")
    init_table(conn)


if __name__ == "__main__":
    main()
