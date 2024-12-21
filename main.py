import configparser
import psycopg2

from src.dataBaseInit.dataBaseInit import init_table
from src.parser.mainParser import parse_files
from src.generateData.generator import data_generate

resource_dir = "resources/"

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
    conn = connect_by_conf(resource_dir + "config/config.ini")

    try:
        init_table(conn, resource_dir)
    except Exception as e:
        print("error on create:")
        print(e)

    try:
        parse_files(conn, resource_dir)
    except Exception as e:
        print("error on parse:")
        print(e)

    try:
        data_generate(conn)
    except Exception as e:
        print("error on data generate:")
        print(e)

    conn.close()


if __name__ == "__main__":
    main()
