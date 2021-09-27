from abc import *

class Repository(metaclass=ABCMeta):
  def __init__(self) -> None:
      pass

  @abstractmethod
  def get_data(self, key):
    pass

  @abstractmethod
  def put_data(self, key, value):
    pass
