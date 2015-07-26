HOST = "localhost"
USERNAME = "root"
PASSWORD = ""
DATABASE = "als"

try:
    from local_settings import *
except:
    print "No local_settings.py found"
    pass
