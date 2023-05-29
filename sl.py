import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS patient_info")
conn.commit()
conn.close()



# import random
# print(random.randint(999999, 999999999))



# import subprocess
# subprocess.call(["python", "manage.py", "runserver"])


# import ctypes
# user32 = ctypes.windll.user32
# screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# print(screensize)