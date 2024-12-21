import csv
import pandas as pd
import psycopg2


def insert_value(conn, table, value, dict_name):
    cur = conn.cursor()
    cur.execute(f"SELECT ID FROM {table} WHERE Name = '{value}'")
    row = cur.fetchone()
    if row is None:
        cur.execute(f"INSERT INTO {table} (Name) VALUES ('{value}') RETURNING ID")
        row = cur.fetchone()
        dict_name[value] = row[0]
    else:
        dict_name[value] = row[0]
    return dict_name[value]


def table_read(conn, file):
    df = pd.read_excel(file)

    colors = {}
    materials = {}
    application_methods = {}
    categories = {}

    for index, row in df.iterrows():
        colors[row['color']] = insert_value(conn, 'Colors', row['color'], colors)
        materials[row['material']] = insert_value(conn, 'SouvenirMaterials', row['material'], materials)
        application_methods[row['applicMetod']] = insert_value(conn, 'ApplicationMethods',
                                                               row['applicMetod'], application_methods)

    cur = conn.cursor()
    for index, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO Souvenirs (
                    ShortName,
                    Name,
                    Description,
                    Rating,
                    IdCategory,
                    IdColor,
                    Size,
                    IdMaterial,
                    Weight,
                    QTopics,
                    PicsSize,
                    IdApplicMethod,
                    AllCategories,
                    DealerPrice,
                    Price
                ) VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                ) RETURNING ID
            """, (
                row['shortname'],
                row['name'],
                row['description'],
                row['rating'],
                int(row['categoryid']),
                colors[row['color']],
                row['prodsize'],
                materials[row['material']],
                float(row['weight']) if pd.notna(row['weight']) else None,
                float(row['qtypics']) if pd.notna(row['qtypics']) else None,
                row['picssize'],
                application_methods[row['applicMetod']],
                False,
                float(row['dealerPrice']) if pd.notna(row['dealerPrice']) else None,
                float(row['price']) if pd.notna(row['price']) else None
            ))
        except psycopg2.errors.NumericValueOutOfRange as e:
            print(f"Ошибка NumericValueOutOfRange: {e}")
            print(f"Столбцы: {row}")
            print(
                f"Значения: {[float(x) if pd.notna(x) else None for x in [row['weight'], row['qtypics'], row['dealerPrice'], row['price']]]}")
        except Exception as e:
            print(f"Ошибка в заполнении данных : {e}")

    conn.commit()


def parse_category(conn, file):
    cursor = conn.cursor()
    with open(file, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            row[1] = row[1] if row[1] else None
            insert_data(cursor, 'SouvenirCategories', ['ID', 'IdParent', 'Name'], row)
    conn.commit()


def insert_data(cursor, table_name, columns, data):
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
    cursor.execute(query, data)


def parse_files(conn, resource_dir):
    parse_category(conn, resource_dir + "data/categories.txt")
    table_read(conn, resource_dir + "data/data.xlsx")