#!/usr/bin/python3
"""
PyQt 5 tutorial
Simple application
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QWidget()
    window.resize(250, 150)
    window.move(300, 300)
    window.setWindowTitle('Simple Application')
    window.show()

    sys.exit(app.exec_())