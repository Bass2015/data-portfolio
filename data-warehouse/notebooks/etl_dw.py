import os
import psycopg2
import pandas as pd
import sql_queries as qu
from create_tables import get_db, OP_DB, DW_DB
 
# El doble guión bajo marca la función como privada
def __load_table(name, df, cur, conn):
    try:
        # Construyo el INSERT con los VALUES necesarios
        sentencia_insert = qu.build_insert(name, df)
        # Este método ejecuta la sentencia para cada fila del dataframe df
        cur.executemany(sentencia_insert, df.values)
        conn.commit()
    except psycopg2.Error:
       print(f"Error cargando tabla {name}!!!")
       conn.rollback()

def __get_data_from_op():
    # Este método extrae la información de la base de datos operacional
    # usando las sentencias SELECT guardadas en sql_queries.py 
    # y transforma la información en dataframes.
    cur, conn = get_db(OP_DB)
    users = pd.read_sql(qu.GET_USERS, conn) 
    cards = pd.read_sql(qu.GET_CARDS, conn) 
    comps = pd.read_sql(qu.GET_COMP, conn)
    prods = pd.read_sql(qu.GET_PRODS, conn)
    txn = pd.read_sql(qu.GET_TXN, conn) 
    prod_list = pd.read_sql(qu.GET_PROD_LIST, conn)
    conn.commit()
    conn.close()
    return users, cards, comps, prods, txn, prod_list

def load_data():
    # Coge los dataframes y los carga en la base
    # de `datos datawarehouse`
    users, cards, companies, products, txns, prod_list = __get_data_from_op()
    cur, conn = get_db(DW_DB)
    __load_table("users", users, cur, conn)
    __load_table("cards", cards, cur, conn)
    __load_table("companies", companies, cur, conn)
    __load_table("products", products, cur, conn)
    __load_table("transactions", txns, cur, conn)
    __load_table("product_list", prod_list, cur, conn)

   