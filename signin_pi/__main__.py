"""The main routine of siginin-pi."""

import sys
from PySide2.QtWidgets import QApplication
from dotenv import load_dotenv


#from signin_pi.scan import scan

from signin_pi.database import database
from signin_pi.ui import ui


def main(args=None):
    """The main routine."""

    #import signin_pi.scan
    tables = ['qrcode', 'qrlogs']

    load_dotenv()

    if args is None:
        args = sys.argv[1:]

    print("This is the main routine meep.")

    #new = database.database()
    #new.createTables()
    #new.checkTables(tables)
    #ew.createQrcode('45667778')
    #new.logQr('45667778')
    #new.logQr('45667778')


    app = QApplication(sys.argv)
    win = ui.MainApp()
    win.show()
    sys.exit(app.exec_())



    

if __name__ == "__main__":
    sys.exit(main())




