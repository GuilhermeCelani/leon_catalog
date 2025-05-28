from dotenv import load_dotenv
from logging import getLogger
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

logger = getLogger(__name__)

class Conn:
  DB_CONFIG = {
  'user'    :getenv('DB_USER'),
  'password':getenv('DB_PASS'),
  'host'    :getenv('DB_HOST'),
  'port'    :getenv('DB_PORT'),
  'database':getenv('DB_NAME')
}
  DB_TABLE = 'book_catalog'
  
  def __init__(self, user, password, host, port, database):
    self.user     = user
    self.password = password
    self.host     = host
    self.port     = port
    self.database = database
    self.engine   = None

  def connect(self):
    conn_string = (
      f'postgresql://{self.user}:{self.password}@'
      f'{self.host}:{self.port}/{self.database}'
    )

    try:
      self.engine = create_engine(conn_string)

      return self.engine
    
    except SQLAlchemyError as e:
      raise RuntimeError(f'Falha na conexão: {str(e)}') from e
    
  def disconnect(self):
    if self.engine:
      self.engine.dispose()
      logger.info('Conexão encerrada.')

  def test_connection(self):
    try:
      with self.engine.connect() as conn:
        logger.info('Conexão com PostgreSQL bem-sucedida.')

        return True
    
    except SQLAlchemyError as e:
      logger.info(f'Falha no teste de conexão: {str(e)}')

  def try_connection(self):
    try:
      if not self.connect():
        exit(0)
    
    except RuntimeError as e:
      logger.info(str(e))
      exit(1)