from sqlalchemy import create_engine, MetaData, \
    Column, Integer, Numeric, String, Date, Table, ForeignKey
import configparser
from connect import engine

engine = engine
metadata = MetaData()
metadata.reflect(bind=engine)


# DDL for customers, products, stores, and transactions
customers_table = Table(
    "utilisateur",
    metadata,
    Column("id_user", Integer, primary_key=True, autoincrement=True),
    Column("login_user", String(35), nullable=False)
)

products_table = Table(
    "pool",
    metadata,
    Column("id_pool", Integer, primary_key=True, autoincrement=True),
    Column("id_server", String(35), nullable=False)
)

stores_table = Table(
    "machine",
    metadata,
    Column("id_machine", Integer, primary_key=True, autoincrement=True),
    Column("os", String(135), nullable=False),
    Column("nb_coeur", String(35), nullable=False),
    Column("taille_disque_dur", String(35), nullable=False),
    Column("id_switch", String(35), nullable=True),
    Column("ram", String(35), nullable=False),
    Column("id_pool", ForeignKey("pool.id_pool"), nullable=False)
)

transactions_table = Table(
    "groupe",
    metadata,
    Column("id_group", Integer, primary_key=True, autoincrement=True),
    Column("libele_group", String(75), nullable=False),
    Column("id_pool", ForeignKey("pool.id_pool"), nullable=False)
)

transactions_table = Table(
    "est_dans",
    metadata,
    Column("id_user", ForeignKey("utilisateur.id_user"), primary_key=True),
    Column("id_group", ForeignKey("groupe.id_group"), primary_key=True)
)
# Start transaction to commit DDL to postgres database
with engine.begin() as conn:
    metadata.create_all(conn)

    for table in metadata.tables.keys():
        print(f"{table} successfully created")
