import os, sys, json, time
#import xml.etree.cElementTree as ET
#import subprocess
#import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON = os.path.join(ROOT, 'python')
if PYTHON not in sys.path:
    sys.path.append(PYTHON)

from domino.core import log, DOMINO_ROOT
from components.print_job import PrintJob

if __name__ == "__main__":

    job = PrintJob()
    print(f'Сервер запущен. Для прерываия нажмите ctrl-C')
    try:
        job.dowork()
    except KeyboardInterrupt:
        print(f'Процесс прерван')
        pass
    
