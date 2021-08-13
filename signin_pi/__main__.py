"""The main routine of siginin-pi."""

import sys
from dotenv import load_dotenv


#from signin_pi.scan import scan

from signin_pi.database import database


def main(args=None):
    """The main routine."""

    #import signin_pi.scan
    tables = ['qrcode', 'qrlogs']

    load_dotenv()

    if args is None:
        args = sys.argv[1:]

    print("This is the main routine meep.")

    new = database.database()
    new.createTables()
    new.checkTables(tables)
    new.createQrcode('45667778')
    new.logQr('45667778')
    new.logQr('45667778')






    

if __name__ == "__main__":
    sys.exit(main())




