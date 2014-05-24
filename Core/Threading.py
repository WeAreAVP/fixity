import threading
import datetime, time

class ThreadClass(threading.Thread):

  def run(self):

    count = 0
    if count > 10:
        exit()
    count = count + 1
    now = datetime.datetime.now()
    print count
    (self.getName(), now)


t = ThreadClass()
t.start()
time.sleep(10)
print(t.is_alive)

print(t.isAlive())