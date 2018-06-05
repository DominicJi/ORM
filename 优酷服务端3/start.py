import os
import sys
BASE_DIR=os.path.dirname(__file__)
sys.path.append(BASE_DIR)
from tcpserver import server_run
if __name__ == '__main__':
    server_run.run()



