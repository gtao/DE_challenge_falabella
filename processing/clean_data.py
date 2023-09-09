import pandas as pd
from datetime import date
import re
from db.conn import create_connection
from db.generate_data import generate_random_data
from db.conn import insert_df_to_psql

# Función para revisar y transformar la data
def check_and_clean(df):
    # Regla 1: name - validar Camelcase en nombre
    df['name'] = df['name'].apply(lambda x: ' '.join([word.capitalize() for word in x.split()]))

    # Regla 2: email - Validar patrón correcto de Email, sino llevarlo a Null
    email_pattern = r'^[\w\.-]+@[\w\.-]+(\.[\w]+)+$'
    df['email'] = df['email'].apply(lambda x: x if re.match(email_pattern, x) else None)

    # Regla 3: address - validar Camelcase en dirección
    df['address'] = df['address'].apply(lambda x: ' '.join([word.capitalize() for word in x.split()]))

    # Regla 4: purchase_amount - Cambiar los negativos a su valor absoluto
    df['purchase_amount'] = df['purchase_amount'].apply(lambda x: abs(x))

    # Regla 5: last_purchase - llevar al día actual si la fecha está en el futiro
    now = date.today()
    df['last_purchase'] = df['last_purchase'].apply(lambda x: now if x > now else x)

    return df

def main():
    # Tabla a consultar
    table_name = "raw_data"
    query = f"SELECT * FROM {table_name}"

    # Leer los datos a un Pandas DF desde la conexión PSQL
    connection = create_connection()
    df = pd.read_sql(query, connection)

    # Rellenar la data en tabla raw_data si es que se encuentra sin registros
    if df.empty:
        print('INFO: tabla raw_data sin información, se rellenará con datos random')
        generate_random_data()
    
    # Validación de los registros cargados
    df_cleaned = check_and_clean(df)

    # Revisión Output DF (primeros 10 de 100)
    print(df_cleaned.head(10))

    # Una vez validados los datos se procede a ingestar en tabla final
    insert_df_to_psql(df_cleaned, 'cleaned_data')
    

if __name__ == "__main__":
    main()