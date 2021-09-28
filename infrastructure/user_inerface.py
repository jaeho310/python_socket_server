#-*-coding:utf-8-*-
import threading
import os
import time
from presentation.interface.controller.client_controller import ClientController
from application.custom_logger import CustomLogger
import subprocess
import re

#-*-coding:utf-8-*-

logger = CustomLogger()

def start_cli_user_interface():
  ui_thread = threading.Thread(target = ui_loop, args=())
  ui_thread.start()

def ui_loop():
  time.sleep(0.5)
  while True:
    print('################관리자################')
    print('1. 현재 접속인원 확인')
    print('2. 공지사항 보내기')
    print('3. 로그 확인(전체)')
    print('4. 로그 확인(info)')
    print('5. 로그 확인(warning)')
    print('6. 디버깅 로그 확인')
    print('7. 콘솔창 지우기')
    print('8. 서버종료(memory db의 데이터는 저장되지 않습니다)')
    try:
      user_input = int(input())
      print('#####################################')
      if user_input == 1:
        get_current_user()
      elif user_input == 2:
        send_all_clients()
      elif user_input == 3:
        get_log()
      elif user_input == 4:
        get_info_log()
      elif user_input == 5:
        get_warn_log()
      elif user_input == 6:
        get_debug_log()
      elif user_input == 7:
        clear_console()
      elif user_input == 8:
        force_quit()
      else:
        wrong_input()
    except Exception as e:
      print(e)
      wrong_input()
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