from sqlalchemy import create_engine, MetaData, select
from faker import Faker
import sys
import random
import datetime
import configparser
from connect import engine

engine = engine
metadata = MetaData()
metadata.reflect(bind=engine)

# Instantiate faker object
faker = Faker()

utilisateur = metadata.tables["utilisateur"]
est_dans = metadata.tables["est_dans"]
groupe = metadata.tables["groupe"]
pool = metadata.tables["pool"]
machine = metadata.tables["machine"]

database = []

try:
    database.append((utilisateur, 15000))
    database.append((pool, 2000))
    database.append((groupe, 1500))
    database.append((est_dans, 1500))
    database.append((machine, 500))
except KeyError as err:
    print("error : Metadata.tables " + str(err) + " not found")

# os list
os_list = ["Windows 7", "Windows 10", "Debian 11", "MacOS X"]

class GenerateData:
    """
    generate a specific number of records to a target table
    """

    def __init__(self, table):
        """
        initialize command line arguments
        """
        self.table = table[0]
        self.num_records = table[1]

    def create_data(self):
        """
        using faker library, generate data and execute DML
        """

        if self.table.name == "utilisateur":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        login_user=faker.user_name()
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "pool":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        id_server=faker.user_name()
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "groupe":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        id_pool=random.choice(conn.execute(select([pool.c.id_pool])).fetchall())[0],
                        libele_group=faker.country()
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "est_dans":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        id_user=random.choice(conn.execute(select([utilisateur.c.id_user])).fetchall())[0],
                        id_group=random.choice(conn.execute(select([groupe.c.id_group])).fetchall())[0]
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "machine":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        os=random.choice(os_list),
                        id_pool=random.choice(conn.execute(select([pool.c.id_pool])).fetchall())[0],
                        nb_coeur=faker.random_int(1, 24),
                        taille_disque_dur=faker.random_int(128, 1024),
                        id_switch="vmbr" + str(faker.random_int(1, 9999)),
                        ram=faker.random_int(4, 64)
                    )
                    conn.execute(insert_stmt)


if __name__ == "__main__":
    for i in database:
        generate_data = GenerateData(i)
        generate_data.create_data()
