
import psycopg2
import pandas as pd
import sql_queries
from create_tables import get_db, OP_DB
 
def __load_table(cur, conn, name, df):
    try:
        # Construyo el INSERT con los VALUES necesarios
        sentencia_insert = sql_queries.build_insert(name, df)
        # Este método ejecuta la sentencia para cada fila del dataframe df
        cur.executemany(sentencia_insert, df.values)
        conn.commit()
    except psycopg2.Error:
       print(f"Error cargando tabla {name}!!!")
       conn.rollback()

# Todos estos métodos leen los csv y json y los cargan en un dataframe. 
# Luego usan el método load_table para cargar los datos en el database.
def __load_users(cur, conn):
    print("Loading users")
    df = pd.concat((pd.read_json("./data/users_usa.json"), 
           pd.read_json("./data/users_ca.json"),
           pd.read_json("./data/users_uk.json")), axis=0)
    __load_table(cur, conn, "users", df)

def __load_cards(cur, conn):
    print("Loading cards")
    __load_table(cur, conn, "cards", pd.read_csv("./data/credit_cards.csv"))

def __load_companies(cur, conn):
    print("Loading companies")
    __load_table(cur, conn, "companies", pd.read_json("./data/companies.json"))

def __load_products(cur, conn):
    print("Loading products")
    df = pd.read_csv("./data/products.csv")
    df['price'] = df['price'].str[1:].astype(float)
    __load_table(cur, conn, "products", df)

def __load_transactions(cur, conn):
    print("Loading transactions")
    df = pd.concat((pd.read_json("./data/transactions_1.json"),pd.read_json("./data/transactions_2.json")), axis=0)
    df['amount'] = df['amount'].str[1:].astype(float)
    __load_table(cur, conn, "transactions", df.loc[:, :'declined'])
    __load_product_list(cur, conn, df)

def __load_product_list(cur, conn, txn):
    print("Loading product list")
    # Para cada elemento en la lista de txn['products_ids'], hacer una entrada en el nuevo DF
    prods = pd.DataFrame(columns=['txn_id', 'product_id'])
    filtered = txn.filter(['id', 'product_ids'], axis=1)
    for row in range(len(filtered.values)):
        product = filtered.values[row][1]
        if type(product) != int:
            for p in product.split(', '):
                prods.loc[len(prods)] = [filtered.values[row][0], p]
        else:
            prods.loc[len(prods)] = [filtered.values[row][0], product]
    __load_table(cur, conn, "product_list", prods)

def load_data():
    cur, conn = get_db(OP_DB)
    __load_users(cur, conn)
    __load_cards(cur, conn)
    __load_companies(cur, conn)
    __load_products(cur, conn)
    __load_transactions(cur, conn)
    conn.close()
   