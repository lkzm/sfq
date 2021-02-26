import os
f = open("/home/vnubis_lkz/django/sfq/files/next.py", "w") 
f.write("print('something')")
f.close()
os.system("python3 /home/vnubis_lkz/django/sfq/files/next.py")
