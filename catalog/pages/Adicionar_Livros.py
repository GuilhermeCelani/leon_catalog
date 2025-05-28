from logging import getLogger
from pandas import DataFrame
import streamlit as st
from conn.connection import Conn

logger = getLogger(__name__)

def send():
  """Send data to database."""
  edited_df = st.session_state.get('df_edited', DataFrame())

  if not edited_df.empty:
    db = Conn(**Conn.DB_CONFIG)

    Conn.try_connection(db)

    try:
      if 'id' in edited_df.columns:
        edited_df = edited_df.drop(columns=['id'])

      edited_df = edited_df.dropna(how='all')
      edited_df = edited_df.dropna(subset=['author', 'name'], how='all')

      edited_df.to_sql(name=Conn.DB_TABLE, con=db.engine, if_exists='append', index=False)
      logger.info('Dados inseridos no banco.')

      st.session_state.success = 'Dados salvos com sucesso!'

    except Exception as e:
      logger.info(f'Falha ao carregar os dados: {str(e)}')

      st.session_state.error = f'Erro ao salvar: {str(e)}'

    finally:
      db.disconnect()

df          = DataFrame(
  columns=['type', 'author', 'name','yearedition',
           'publisher', 'publishyear','quantity', 'theme']
)
column_conf = {
  'type'       :st.column_config.SelectboxColumn('Tipo', options=['Livro', 'Revista'],
                                                          default='Livro'),
  'author'     :st.column_config.Column('Autor', required=True),
  'name'       :st.column_config.Column('Título', required=True),
  'yearedition':'Ano da edição',
  'publisher'  :'Editora',
  'publishyear':'Ano de publicação',
  'quantity'   :'Quantidade',
  'theme'      :'Tema'
}

if 'df' not in st.session_state:
  st.session_state.df = DataFrame(columns=['type', 'author', 'name','yearedition',
                                        'publisher', 'publishyear','quantity', 'theme'])

with st.form('input data'):
  st.session_state.df_edited = st.data_editor(st.session_state.df, column_config=column_conf,
                                              key='data_editor', num_rows='dynamic',
                                              use_container_width=True)
  submitted_value            = st.form_submit_button('Enviar dados ao catálogo')

if submitted_value:
  send()

if 'success' in st.session_state:
  st.success(st.session_state.success)

  del st.session_state.success

if 'error' in st.session_state:
  st.error(st.session_state.error)

  del st.session_state.error
