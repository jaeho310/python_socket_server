from datetime import datetime

class CustomLogger:
  log_data = []
  log_data_info = []
  log_data_warn = []
  log_data_debug = []
  now = datetime.now()

  def __new__(cls):
    if not hasattr(cls,'instance'):
      cls.instance = super(CustomLogger, cls).__new__(cls)
    else:
      pass
    return cls.instance

  def warn(self, msg):
    formatted_msg = "[WARN] [%s년 %s월 %s일 %s시 %s분 %s초] " %(self.now.year, self.now.month, self.now.day, self.now.hour, self.now.minute, self.now.second) + msg
    print(formatted_msg)
    self.log_data.append(formatted_msg)
    self.log_data_warn.append(formatted_msg)

  def info(self, msg):
    formatted_msg = "[INFO] [%s년 %s월 %s일 %s시 %s분 %s초] " %(self.now.year, self.now.month, self.now.day, self.now.hour, self.now.minute, self.now.second) + msg
    print(formatted_msg)
    self.log_data.append(formatted_msg)
    self.log_data_info.append(formatted_msg)

  def debug(self, msg):
    formatted_msg = "[INFO] [%s년 %s월 %s일 %s시 %s분 %s초] " %(self.now.year, self.now.month, self.now.day, self.now.hour, self.now.minute, self.now.second) + msg
    self.log_data_debug.append(formatted_msg)