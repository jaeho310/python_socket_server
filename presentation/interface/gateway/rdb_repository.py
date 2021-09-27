from application.repository import *
from application.custom_logger import CustomLogger

class RdbRepository(Repository):
  __rdb = None
  logger = CustomLogger()

  def __init__(self, rdb) -> None:
    self.__rdb = rdb


  def get_data(self, key):
    response = self.__rdb.execute("SELECT my_data FROM my_table WHERE id = %s" %(key)).fetchone()
    if response:
      self.logger.info('데이터를 조회해갔습니다 ' +  key +": " + str(response[0]))
      return str(response[0])
    else:
      self.logger.info('존재하지 않은 key에 접근하려 합니다. key: ' +  key)
      return False

  def put_data(self, key, value):
    is_duplicated = self.__rdb.execute("SELECT 1 FROM my_table WHERE id = %s" %(key)).fetchone()
    if is_duplicated:
      self.logger.info('중복된 key: "' + key +'" 로 인해 value : "' + value + '" 는 저장되지 않습니다.')
      return False
    else:
      self.__rdb.execute("INSERT INTO my_table VALUES('%s', '%s')" %(key, value))
      return True