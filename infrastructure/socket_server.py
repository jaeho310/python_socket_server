import socket
from presentation.interface.controller.client_controller import ClientController
from presentation.interface.gateway.memory_repository import MemoryRepository
from presentation.interface.gateway.rdb_repository import RdbRepository
from application.interactor import Interactor
from application.custom_logger import CustomLogger
from infrastructure.db_sqlite3 import DbSqlite3

class SocketServer:
  __socket_server = None
  __client_controller = None
  logger = CustomLogger()

  def __init__(self):
    self.__socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__socket_server.bind(('', 8395))
    self.logger.info("서버를 시작합니다.")
    self.__socket_server.listen(10)

  def start(self):
    self.__client_controller.receive_client(self.__socket_server)

  # layered architecture를 적용하였으며 각 컴포넌트는 구현에 의존하지 않고 추상에 의존합니다.
  # 고수준의 모듈이 저수준의 모듈에 의존하지 않게되면(결합도가 낮은 설계)
  # 업무규약이나, 데이터 저장방식이 바뀌더라도 손쉽게 유지보수가 가능합니다
  def register_layer(self, repository_type):
    repositoryImpl = self.repository_factory(repository_type)
    interactor = Interactor(repositoryImpl)
    self.__client_controller = ClientController(interactor)

  # repository를 python argument에서 설정합니다.
  def repository_factory(self, repository_type):
    repositoryImpl = None
    if repository_type == 'memory':
      repositoryImpl = MemoryRepository()
    elif repository_type == 'rdb':
      db_sqlite3 = DbSqlite3()
      rdb = db_sqlite3.getDb()
      repositoryImpl = RdbRepository(rdb)
    return repositoryImpl
