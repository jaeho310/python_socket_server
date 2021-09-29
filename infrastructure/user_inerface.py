import threading
import os
import time
from presentation.interface.controller.client_controller import ClientController
from application.custom_logger import CustomLogger
import subprocess
import re

logger = CustomLogger()
command = {}


def start_cli_user_interface():
  command_pattern()
  ui_thread = threading.Thread(target = ui_loop, args=())
  ui_thread.start()

def command_pattern():
  command[1] = {'desc': '1. 현재 접속인원 확인', 'func': get_current_user}
  command[2] = {'desc': '2. 공지사항 보내기', 'func': send_all_clients}
  command[3] = {'desc': '3. 로그 확인(전체)', 'func': get_log}
  command[4] = {'desc': '4. 로그 확인(info)', 'func': get_info_log}
  command[5] = {'desc': '5. 로그 확인(warning)', 'func': get_warn_log}
  command[6] = {'desc': '6. 디버깅 로그 확인', 'func': get_debug_log}
  command[7] = {'desc': '7. 콘솔창 지우기', 'func': clear_console}
  command[8] = {'desc': '8. 서버종료(memory db의 데이터는 저장되지 않습니다)', 'func': force_quit}

def ui_loop():
  time.sleep(0.5)
  while True:
    for _, key in enumerate(command):
      print(command[key]['desc'])
    try:
      user_input = int(input())
      print('#####################################')
      if user_input not in command:
        wrong_input()
      command[user_input]['func']()
    except Exception as e:
      print(e)
    input()

def save_log():
  f = open("./application.txt", 'a', encoding='utf-8')
  for msg in logger.log_data:
    f.write(msg + '\n')
  f.close()

  f = open("./application_info.txt", 'a', encoding='utf-8')
  for msg in logger.log_data_info:
    f.write(msg + '\n')
  f.close()

  f = open("./application_warn.txt", 'a', encoding='utf-8')
  for msg in logger.log_data_warn:
    f.write(msg + '\n')
  f.close()

  f = open("./application_debug.txt", 'a', encoding='utf-8')
  for msg in logger.log_data_debug:
    f.write(msg + '\n')
  f.close()

def force_quit():
  save_log()
  a = subprocess.check_output('netstat -ano | findstr 8395', shell=True)
  print(a.decode())
  list = re.compile("\s\d{2,10}").findall(a.decode())
  pid = list[0].replace(" ","")
  print(pid)
  os.system('taskkill /pid %s /f' %(pid))

def clear_console():
  os.system('clear')

def wrong_input():
  print('잘못 입력하셨습니다.')

def get_current_user():
  client_list = ClientController.__clients__
  if not client_list:
    print('현재 접속인원이 없습니다.')
    return
  for addr in client_list:
    print(addr)

def get_log():
  for msg in logger.log_data:
    print(msg)

def get_warn_log():
  for msg in logger.log_data_warn:
    print(msg)

def get_info_log():
  for msg in logger.log_data_info:
    print(msg)

def get_debug_log():
  for msg in logger.log_data_debug:
    print(msg)

def send_all_clients():
  client_list = ClientController.__clients__
  if not client_list:
    print('현재 접속인원이 없습니다.')
    return
  print("공지사항을 보낼 메시지를 입력하세요")
  msg = input()
  parsed_msg = "[공지사항] " + msg
  for client in client_list.values():
    client.sendall(parsed_msg.encode())