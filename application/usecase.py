from abc import *

class UseCase(metaclass=ABCMeta):
  def __init__(self) -> None:
      pass

  @abstractmethod
  def do_get(self, msg):
    pass

  @abstractmethod
  def do_put(self, msg):
    pass
