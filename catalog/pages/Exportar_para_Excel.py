from conn.connection import Conn
from pandas import read_sql

def load_data():
  """Load data from database."""
  db = Conn(**Conn.DB_CONFIG)

  Conn.try_connection(db)

  return read_sql('SELECT * FROM book_catalog', db.connect())

def export_data():
  """Export data to Excel"""
  df         = load_data()  
  excel_file = df.to_excel()
