from infrastructure.socket_server import SocketServer
from infrastructure.user_inerface import *
import sys
import setproctitle

if __name__ == "__main__":
  start_cli_user_interface()

  repository_type = 'memory'
  if len(sys.argv) >= 2:
    repository_argv = sys.argv[1]
    if repository_argv == 'mem':
      repository_type = 'memory'
    elif repository_argv == 'rdb':
      repository_type = 'rdb'


  main_server = SocketServer()
  main_server.register_layer(repository_type)
  main_server.start()

