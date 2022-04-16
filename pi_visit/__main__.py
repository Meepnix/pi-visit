"""The main routine of siginin-pi."""

import sys
from PySide2.QtWidgets import QApplication
from dotenv import load_dotenv
import argparse


#from signin_pi.scan import scan

from pi_visit.database import database
from pi_visit.ui import ui


def main(args=None):
    """The main routine."""

    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument('-setup', action='store_true')
    args = parser.parse_args()

    if args.setup == True:

        print("Setup begins!")
        setup()

    load_dotenv()

    print("Main routine begins.")

    ui.start()
   

def setup():

    print("Setup")

    tables = ['qrcode', 'qrlogs']

    new = database.database()
    if new.check_tables(tables) == False:
        new.create_tables()

    print("Setup complete!")





    

if __name__ == "__main__":
    sys.exit(main())




