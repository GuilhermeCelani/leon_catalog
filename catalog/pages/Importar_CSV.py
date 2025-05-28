from logging import getLogger
from pandas import read_csv, read_sql
from streamlit import file_uploader, form, form_submit_button
from conn.connection import Conn

logger = getLogger(__name__)

with form('input data'):
  imported_file   = file_uploader('Anexe um arquivo CSV:', type='csv', accept_multiple_files=False)
  submitted_value = form_submit_button('Enviar dados')

def load_csv(csv_path):
  """Load CSV file"""
  try:
    dataframe = read_csv(csv_path, delimiter=',', encoding='utf-8')

    print('CSV carregado com sucesso.')

    return dataframe

  except Exception as e:
    print(f'Erro ao ler o CSV: {str(e)}')
    exit(1)


def import_data():
  """Import CSV file data to database"""
  df = load_csv(imported_file)
  db = Conn(**Conn.DB_CONFIG)

  Conn.try_connection(db)

  try:
    df.to_sql(name=Conn.DB_TABLE, con=db.engine, if_exists='append', index=False)
    print('Dados inseridos no banco.')

    query    = f'SELECT * FROM {Conn.DB_TABLE} LIMIT 5;'
    df_check = read_sql(query, db.engine)
  
  except Exception as e:
    print(f'Falha ao carregar os dados: {str(e)}')
  
  finally:
    db.disconnect()

if submitted_value:
  import_data()