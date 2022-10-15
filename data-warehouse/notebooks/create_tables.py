import psycopg2
import sql_queries

OP_DB = "operational"
DW_DB = "datawarehouse"

# función privada
def __create_dbs():
    """
        Create the datawarehouse and codeopfintech databases.
        If any of them already exists, Drop and create the database.
    Returns:
        success(boolean): wether the operation succeed or not.
    """
    try:
        # connect to default database
        conn = psycopg2.connect(user="user",
                                password="passw",
                                host="postgres"
                                )
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        # create databases with UTF8 encoding
        cur.execute(f"DROP DATABASE IF EXISTS {DW_DB}")
        cur.execute(f"DROP DATABASE IF EXISTS {OP_DB}")
        cur.execute(
            f"CREATE DATABASE {DW_DB} WITH ENCODING 'utf8' TEMPLATE template0"
        )
        cur.execute(
            f"CREATE DATABASE {OP_DB} WITH ENCODING 'utf8' TEMPLATE template0"
        )

        # close connection
        conn.close()
        return True
    except (Exception, psycopg2.Error) as error:
        print("Failed to creating dbs: ", error)
        return False

def get_db(db_name):
    """
    Establish connection to a database and return its connection.
    Args:
        dn_name (str): The name of the database you want to connect
    Returns:
        cursor(psycopg2.cursor): The psycopg2 cursor
        connection(psycopg2.connection): The db connection
    """
    try:
        conn = psycopg2.connect(database=db_name,
                                user="user",
                                password="passw",
                                host="postgres"
                                )
        return conn.cursor(), conn
    except (Exception, psycopg2.Error) as error:
        print("Failed to getting db: ", error)
        return False, False
    
def __create_tables(conn, cur, tables):
    # Me aseguro de que no hay ninguna transacción pendiente
    conn.rollback()
    # Creo todas las tablas
    for table in tables:
        print("Creating table ", table.split()[2])
        cur.execute(table)
    conn.commit()
    
def create_databases():
    # __create_dbs() devuelve un booleano. Por lo tanto, puedo usar ese valor
    # para asegurarme de que las bases se han creado
    if __create_dbs():
        print("CREATING OPERATIONAL: ")
        cur, conn = get_db(OP_DB)
        try:
            __create_tables(conn, cur, sql_queries.OP_TABLES)
        except psycopg2.Error:
            print("Error creando database operacional")
            conn.rollback()
        finally:
            conn.close()
        print("CREATING DATAWAREHOUSE: ")
        cur, conn = get_db(DW_DB)
        try:
            __create_tables(conn, cur, sql_queries.DW_TABLES)
        except psycopg2.Error as error:
            print("Error creando datawarehouse", error)
            conn.rollback()
        finally:
            conn.close()
