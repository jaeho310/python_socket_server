import threading
from time import sleep
from application.usecase import UseCase
from application.custom_logger import CustomLogger
import traceback

class ClientController:
  __clients__ = {}
  __usecase = None
  logger = CustomLogger()
  def __init__(self, interractor):
    self.__usecase = self.interactor_factory(interractor)

  def interactor_factory(self, interactor)->UseCase:
    return interactor

  def receive_client(self, socket_server):
    while True:
      socket_client, addr = socket_server.accept()
      self.logger.info(addr[0] + " 사용자가 서버에 접속했습니다.")

      client_thread = threading.Thread(target=self.data_received, args=(socket_client, addr))
      client_thread.start()

      heart_beat_thread = threading.Thread(target=self.heart_beat, args=(socket_client, addr))
      heart_beat_thread.start()

      self.__clients__[addr[0]] = socket_client

  def data_received(self, socket_client, addr):
    while True:
      try:
        raw_data = socket_client.recv(1024)
        data = raw_data.decode('utf-8')
        self.logger.debug(data)
        self.parsing_data(socket_client, data, addr)
      except Exception as e:
        print(e)
        traceback.format_exc()
        # 소켓연결이 끊긴 에러코드가 온 경우에만 read 작업 끝
        if e.args[0] == 10054:
          break

  def parsing_data(self,socket_client, data, addr):
    parsed_data = data.split('>')
    for transaction in parsed_data:
      if transaction == '':
        continue
      request, msg = transaction.split('<')

      if request == '' or msg == '':
        self.logger.warn(addr[0] + " 사용자의 데이터 유실")
        # 지속적인 데이터유실 발생의 원인이 클라이언트의 과도한 트래픽이라면
        # 서버 과부하를 막기위해 클라이언트와의 커넥션을 강제로 끊어버려야 한다.
        continue

      self.logger.info(addr[0] + " 사용자가 msg를 보냈습니다. 요청: [" + request +'], 내용: [' + msg +']')
      response = ''
      if request == 'get':
        response = self.__usecase.do_get(msg)
      elif request == 'put':
        response = self.__usecase.do_put(msg)
      socket_client.sendall(response.encode())


  # heart_beat_thread
  # 서버가 현재 접속자를 확인하는 용도입니다.
  # heart beat 스레드를 사용하면 누가 서버와의 연결을 끊었는지 확인할 수 있습니다.
  def heart_beat(self, socket_client, addr):
    while True:
      try:
        sleep(3)
        socket_client.sendall('heart_beat'.encode())
      except Exception as e:
        self.logger.info(addr[0] + " left server")
        if addr[0] in self.__clients__:
          del self.__clients__[addr[0]]
        print(e)
        traceback.format_exc()
        break





