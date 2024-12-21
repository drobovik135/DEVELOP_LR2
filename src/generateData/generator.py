from .consts import *

def data_generate(conn):
    cur = conn.cursor()

    cur.execute(f"INSERT INTO {statuses} (Name) VALUES ('very bad') RETURNING ID")
    statusId = cur.fetchone()

    cur.execute(
        f"INSERT INTO {providers} (Name, Email, ContactPerson) VALUES ('my beautiful shop', 'myBeautifulMail@mail.com', 'Alexy') RETURNING ID")
    providerId = cur.fetchone()

    cur.execute(
        f"INSERT INTO {procurements} (IdProvider, Data, IdStatus) VALUES ('{providerId[0]}', '2023-02-05', '{statusId[0]}') RETURNING ID")
    procurementsId = cur.fetchone()

    cur.execute(f"SELECT ID FROM {souvenir} WHERE Id = '532'")
    souvenirId = cur.fetchone()
    cur.execute(
        f"INSERT INTO {ps} (IdSouvenir, IdProcurement, Amount, Price) VALUES ('{souvenirId[0]}', '{procurementsId[0]}', '50', '10') RETURNING ID")
    psId = cur.fetchone()

    cur.execute(
        f"INSERT INTO {stories} (IdProcurement, IdSouvenir, Amount) VALUES ('{procurementsId[0]}', '{souvenirId[0]}', '10') RETURNING ID")
    storiesId = cur.fetchone()

    conn.commit()