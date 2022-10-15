# Sentencias para crear las tablas
OP_TABLES = ("""
    CREATE TABLE users (
      id int,
      name varchar(34),
      surname varchar(34),
      phone varchar(50),
      email varchar(50),
      birth_date date,
      country varchar(50),
      city varchar(50),
      postal_code varchar(50),
      address varchar (50),
      PRIMARY KEY (id)
    )
""",
"""CREATE TABLE cards (
      id varchar(34),
      user_id int,
      iban varchar(34),
      pan varchar(255),
      pin varchar(4),
      cvv varchar(255),
      track1 varchar(255),
      track2 varchar(255),
      expiring_date varchar(255),
      PRIMARY KEY (id),
      CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id)
    )
""",
"""CREATE TABLE companies (
      company_id varchar(50),
      company_name varchar(50),
      phone varchar(50),
      email varchar(50),
      country varchar(50),
      website varchar(50),
      PRIMARY KEY (company_id)
    )
""",
"""CREATE TABLE products (
      id int,
      product_name varchar(50),
      price float,
      colour varchar(50),
      weight float,
      warehouse_id varchar(50),
      PRIMARY KEY (id)
    )
""",
"""CREATE TABLE transactions (
      id varchar(50),
      card_id varchar(50),
      business_id varchar(50),
      lat_long varchar(255),
      pin varchar(50),
      timestamp timestamp,
      amount float,
      declined boolean,
      product_ids varchar(255),
      PRIMARY KEY (id),
      CONSTRAINT fk_card FOREIGN KEY (card_id) REFERENCES cards (id),
      CONSTRAINT fk_business FOREIGN KEY (business_id) REFERENCES companies (company_id)
    )
""",
"""CREATE TABLE product_list (
      txn_id varchar(50) REFERENCES transactions (id),
      product_id int REFERENCES products (id),
      PRIMARY KEY (txn_id, product_id)
    )
""")

DW_TABLES = (
  """CREATE TABLE users (
      id int,
      name varchar(34),
      surname varchar(34),
      phone varchar(50),
      email varchar(50),
      birth_date date,
      country varchar(50),
      city varchar(50),
      postal_code varchar(50),
      address varchar (50),
      PRIMARY KEY (id)
    )
""",
"""CREATE TABLE cards (
      id varchar(34),
      iban varchar(34),
      pan varchar(255),
      pin varchar(4),
      cvv varchar(255),
      track1 varchar(255),
      track2 varchar(255),
      expiring_date varchar(255),
      PRIMARY KEY (id)
    )
""",
"""CREATE TABLE companies (
      company_id varchar(50),
      company_name varchar(50),
      phone varchar(50),
      email varchar(50),
      country varchar(50),
      website varchar(50),
      PRIMARY KEY (company_id)
    )
""",
"""CREATE TABLE products (
      id int,
      product_name varchar(50),
      price float,
      colour varchar(50),
      weight float,
      warehouse_id varchar(50),
      PRIMARY KEY (id)
    )
""",
"""CREATE TABLE transactions (
      id varchar(50),
      user_id int,
      card_id varchar(50),
      business_id varchar(50),
      lat_long varchar(255),
      pin varchar(50),
      timestamp timestamp,
      amount float,
      declined boolean,
      PRIMARY KEY (id),
      CONSTRAINT fk_card FOREIGN KEY (card_id) REFERENCES cards (id),
      CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id),
      CONSTRAINT fk_business FOREIGN KEY (business_id) REFERENCES companies (company_id)
    )
""",
"""CREATE TABLE product_list (
      txn_id varchar(50) REFERENCES transactions (id),
      product_id int REFERENCES products (id),
      PRIMARY KEY (txn_id, product_id)
    )
""")


# Sentencias para extraer la información de la 
# base de datos operacional
GET_USERS = "SELECT * FROM users"
GET_CARDS = "SELECT id, iban, pan, pin, cvv, track1, track2, expiring_date FROM cards"
GET_COMP = "SELECT * FROM companies"
GET_PRODS = "SELECT * FROM products"
GET_TXN = """SELECT t.id, 
                  c.user_id,
                  t.card_id,
                  t.business_id,
                  t.lat_long,
                  t.pin,
                  t.timestamp,
                  t.amount,
                  t.declined
              FROM transactions t JOIN cards c ON t.card_id=c.id
          """
GET_PROD_LIST = "SELECT * FROM product_list"


def build_insert(name, df):
  """Construye una sentencia INSERT a partir de las
  columnas de un dataframe.
  """
  start = f"INSERT INTO {name} ("
  middle = ") VALUES ("
  end = ")"
  for i in range(len(df.columns)):
      start += df.columns[i]
      middle += "%s"
      if i != len(df.columns) -1:
          start += ', '
          middle += ', '
  return start + middle + end 


