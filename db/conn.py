import psycopg2

def create_connection():
    # Configuración de la conexión PostgreSQL
    connection = psycopg2.connect(
        host="localhost",
        database="postgres", # chall_falabella
        user="de_chall"
        ,password="pass321"
        #,port="5432"
    )
    return connection

def insert_df_to_psql(dataframe, table_name):
    try:
        # crear conexción
        connection = create_connection()
        cursor = connection.cursor()

        # lista de datos por fila del DF
        rec = [tuple(row) for row in dataframe.values]

        # Crear el string que separará los valores a insertar
        cols_val = ', '.join(['%s' for _ in range(len(dataframe.columns))])

        # query de ingesta
        in_q = f"INSERT INTO {table_name} VALUES ({cols_val})"

        # executar inserts
        cursor.executemany(in_q, rec)

        connection.commit()
        cursor.close()
        connection.close()

        print(f"Se cargaron {len(rec)} registros en '{table_name}'")
    except Exception as e:
        print(f"Error: {str(e)}")
