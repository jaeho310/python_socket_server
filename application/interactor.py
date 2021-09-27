from abc import *
from application.usecase import UseCase
from application.repository import Repository

class Interactor(UseCase):
  __repository = None

  def __init__(self, repositoryImpl) -> None:
    self.__repository = self.repository_factory(repositoryImpl)

  def repository_factory(self, repositoryImpl)->Repository:
    return repositoryImpl


  def do_get(self, msg):
    response = self.__repository.get_data(msg)
    if response:
      return response
    else:
      return '해당 key에는 data가 없습니다'

  def do_put(self, msg):
    key, value = msg.split(',')
    response = self.__repository.put_data(key, value)
    if response:
      return '데이터 저장 성공'
    else:
      return '중복된 key 입니다'
