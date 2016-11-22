#!/usr/bin/python3
"""
PyQt 5 tutorial
Simple application
"""

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QDesktopWidget, \
    QMessageBox, QMenuBar, QPushButton, QLabel, QWidget

JBROWSE_ROOT = ""
DEFAULT_ASSEMBLER = ""


class JBrowseApplication(QMainWindow):
    def __init__(self):
        super(JBrowseApplication, self).__init__()
        self.setCentralWidget(PreferencesWidget(self))
        self.initUI()

    def initUI(self):
        """Initializes the main window."""

        def uicalls():
            self.add_menu_bar()
            self.center()
            self.setGeometry(300, 300, 350, 250)
            self.setWindowTitle('JBrowse Loader')
            self.setWindowIcon(QIcon('./jbrowse.png'))

        uicalls()
        self.show()

    def add_menu_bar(self):
        """Adds the menu bar with Loader Settings under Configure."""
        preferenceAction = QAction(QIcon('./jbrowse.png'), "Loader Settings", self)
        preferenceAction.setText("Loader Settings")
        preferenceAction.triggered.connect(self.preferences)

        menubar = QMenuBar()
        configure_menu = menubar.addMenu('Configure')
        configure_menu.addAction(preferenceAction)
        self.setMenuBar(menubar)

    def preferences(self):
        """TBD"""
        temp = SecondWidget(self)
        self.setCentralWidget(temp)

    def center(self):
        """Centers the window on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        """Confirms that the user wants to quit the application."""
        reply = QMessageBox.question(self, 'Confirm',
                                     "Are you sure to quit? All current processes will be terminated",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class PreferencesWidget(QWidget):
    def __init__(self, parent):
        super(PreferencesWidget, self).__init__(parent)
        jbrowse_label = QLabel("JBrowse Root: --", self)
        assembler_label = QLabel("Assembler: --", self)

        def add_buttons():
            btn = QPushButton('JBrowse', self)
            btn.clicked.connect(updateJBrowseLabel)
            btn.resize(btn.sizeHint())
            btn.move(50, 50)

            btn = QPushButton('Assembler', self)
            btn.clicked.connect(updateAssembler)
            btn.resize(btn.sizeHint())
            btn.move(50, 100)

        def updateJBrowseLabel():
            jbrowse_label.setText("JBrowse Root: " + JBROWSE_ROOT)

        def updateAssembler():
            assembler_label.setText("Assembler: " + DEFAULT_ASSEMBLER)

        def add_labels():
            jbrowse_label.move(145, 50)
            assembler_label.move(165, 100)

        add_buttons()
        add_labels()


class SecondWidget(QWidget):
    def __init__(self, parent):
        super(SecondWidget, self).__init__(parent)
        new_label = QLabel("NEW LABEL", self)
        new_label.move(145, 50)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JBrowseApplication()
    sys.exit(app.exec_())
