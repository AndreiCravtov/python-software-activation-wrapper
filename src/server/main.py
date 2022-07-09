# Set up environment for importing other files by including folders
import sys
sys.path.append("./util/")
sys.path.append("./lib/")

from server import *
import traceback

def main():
    try:
        Server()
    except Exception as _:
        print(traceback.format_exc())
        input()

if __name__ == '__main__':
    main()