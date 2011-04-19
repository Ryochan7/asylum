import os
import sys
import site

sys.stdout = sys.stderr
# Add virtualenv site-packages directory to sys.path
VIRTUALENV_DIR = """/home/ryochan7/.virtualenvs/asylum/lib/python2.7/"""
    """site-packages"""
site.addsitedir(VIRTUALENV_DIR)

PROJECT_PATH  = os.path.dirname (__file__)
ROOT_FILE_PATH = os.path.abspath (os.path.join (PROJECT_PATH, '..'))

if ROOT_FILE_PATH not in sys.path:
    sys.path.insert (0, ROOT_FILE_PATH)

if PROJECT_PATH not in sys.path:
    sys.path.insert (1, PROJECT_PATH)

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
 
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler ()
print sys.path

