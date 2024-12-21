import configparser
import psycopg2


def execute_sql_file(connection, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_commands = file.read()
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql_commands)
            connection.commit()
            print(f"Script {file_path} is complete.")
        except Exception as e:
            connection.rollback()
            print(f"Script: {file_path} \nis failed by:\n {e}")


def init_table(conn, resource_dir):
    execute_sql_file(conn, resource_dir + "requests/tables.sql")
