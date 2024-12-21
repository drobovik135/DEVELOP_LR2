import configparser
import psycopg2


def execute_sql_file(connection, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_commands = file.read()
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql_commands)
            connection.commit()
            print(f"Start of {file_path} so nice.")
        except Exception as e:
            connection.rollback()
            print(f"Failed start: {file_path} \nby error:\n {e}")


def init_table(conn):
    execute_sql_file(conn, "sql/table_create.sql")
    execute_sql_file(conn, "sql/select.sql")
