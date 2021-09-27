import sqlite3

class DbSqlite3:
  __cur = None

  def __init__(self):
    conn = sqlite3.connect("local.db", isolation_level=None, check_same_thread=False)
    self.__cur = conn.cursor()
    self.__cur.execute("CREATE TABLE IF NOT EXISTS my_table (id text, my_data text)")

  def getDb(self):
    return self.__cur