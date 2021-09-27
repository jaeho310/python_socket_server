from application.repository import *
from application.custom_logger import CustomLogger

class MemoryRepository(Repository):
  # 실제로 사용하려면 thread로부터 안전한 dictionary를 사용해야 합니다.
  # 데이터 저장방법이 변경되더라도
  # 상위 layer는 추상에 의존하였으므로
  # get_data와 put_data를 구현하고 Repository를 상속받은 새로운 구현체를 만들면
  # 손쉽게 rdb, redis, nosql, file등으로 변경이 가능합니다
  __memory_db = {}
  logger = CustomLogger()
  def __init__(self) -> None:
    pass

  def get_data(self, key):
    if key in self.__memory_db:
      response = self.__memory_db[key]
      self.logger.info('데이터를 조회해갔습니다 ' +  key +": " + response)
      return response
    else:
      self.logger.info('존재하지 않은 key에 접근하려 합니다. key: ' +  key)
      return False

  def put_data(self, key, value):
    if key not in self.__memory_db:
      self.__memory_db[key] = value
      self.logger.info('데이터 저장 {' +  key +" : " + value + '}')
      return True
    else:
      self.logger.info('중복된 key: "' + key +'" 로 인해 value : "' + value + '" 는 저장되지 않습니다.')
      return False