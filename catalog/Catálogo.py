"""Main page. Shows the catalog."""

from unicodedata import normalize
from conn.connection import Conn
from pandas import DataFrame, isna, read_sql
from streamlit import data_editor , set_page_config, text_input

#
# FUNCTIONS
#
def normalize_search(search_term: str) -> str:
  """Normalize search term characters."""
  if isna(search_term):
    return ''

  search_term = normalize('NFKD', str(search_term)).encode('ASCII', 'ignore').decode('ASCII')

  return search_term.replace(',', '').strip().lower()

def filter_dataframe(dataframe: DataFrame, search_term: str) -> DataFrame:
  """Filters the dataframe by search."""
  if not search_term:
    return dataframe

  df_processed                = dataframe.copy()
  df_processed['author']      = df_processed['author'].apply(normalize_search)
  df_processed['name']        = df_processed['name'].apply(normalize_search)
  df_processed['publishyear'] = df_processed['publishyear'].apply(normalize_search)
  df_processed['yearedition'] = df_processed['yearedition'].apply(normalize_search)
  search_parts                = normalize_search(search_term).split()
  mask                        = (
    df_processed['author'].apply(lambda x: all(part in x for part in search_parts)) |
    df_processed['name'].apply(lambda x: all(part in x for part in search_parts)) |
    df_processed['publishyear'].apply(lambda x: all(part in x for part in search_parts)) |
    df_processed['yearedition'].apply(lambda x: all(part in x for part in search_parts))
  )

  return dataframe[mask]

def load_data():
  """Load the data from database."""
  db = Conn(**Conn.DB_CONFIG)

  Conn.try_connection(db)

  return read_sql('SELECT * FROM book_catalog', db.connect())

#
# MAIN CODE
#
set_page_config(page_title='Catálogo de livros - Biblioteca FLB-AP', layout='wide',
                initial_sidebar_state='auto')

column_conf = {
  'id'         :'ID',
  'type'       :'Tipo',
  'author'     :'Autor',
  'name'       :'Título',
  'yearedition':'Ano da edição',
  'publisher'  :'Editora',
  'publishyear':'Ano de publicação',
  'quantity'   :'Quantidade',
  'theme'      :'Tema'
}
df          = load_data()
search_bar  = text_input('Pesquise o nome do autor ou da obra...', key='search_input')
filtered_df = filter_dataframe(df, search_bar)
edited_df   = data_editor(filtered_df, column_config=column_conf,
                          num_rows='dynamic', disabled=True, use_container_width=True)
