from PySide2.QtWidgets import QApplication
from pi_visit.ui import menu

import sys


def start():

    app = QApplication(sys.argv)
    win = menu.Menu()
    win.show()
    app.exec_()




