#!/usr/bin/python3
"""
Kadhirvel Manickam December 2016
PyQt 5
JBrowse Data Loader
"""

import sys

from Helper.GlobalHelper import *

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QDesktopWidget, \
    QMessageBox, QMenuBar, QPushButton, QLabel, QWidget, QFileDialog, QGridLayout

JBROWSE_ROOT = ""
DEFAULT_ASSEMBLER = ""


class JBrowseApplication(QMainWindow):
    def __init__(self):
        super(JBrowseApplication, self).__init__()
        self.init_ui()
        self.write_config_setting()
        self.setCentralWidget(Settings(self))

    def init_ui(self):
        """Initializes the main window."""
        def uicalls():
            self.add_menu_bar()
            self.center()
            self.setGeometry(300, 300, 350, 250)
            self.setWindowTitle('JBrowseLoader')
            self.setWindowIcon(QIcon('./jbrowse.png'))

        uicalls()
        self.show()

    def add_menu_bar(self):
        """Adds the menu bar with Loader Settings under Configure."""
        homeAction = QAction(QIcon('./jbrowse.png'), "Go Home", self)
        homeAction.setText("Go Home")
        homeAction.triggered.connect(self.home)

        settingsAction = QAction(QIcon('./jbrowse.png'), "Settings", self)
        settingsAction.setText("Loader Settings")
        settingsAction.triggered.connect(self.settings)

        menubar = QMenuBar()
        home_menu = menubar.addMenu('Settings')
        home_menu.addAction(settingsAction)
        configure_menu = menubar.addMenu('Home')
        configure_menu.addAction(homeAction)

        self.setMenuBar(menubar)

    def settings(self):
        """Displays the settings window, so the user can adjust where the JBrowse
        Loader takes JBrowse from and which assembler to use."""
        self.setCentralWidget(Settings(self))

    def home(self):
        """Home screen"""
        self.setCentralWidget(Home(self))

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

    @staticmethod
    def write_config_setting():
        global JBROWSE_ROOT
        global DEFAULT_ASSEMBLER
        Jbrowse_setting = read_configuration_file('JBrowse_Root')
        if Jbrowse_setting != 'None':
            JBROWSE_ROOT = Jbrowse_setting
        Assembler_setting = read_configuration_file('Assembler')
        if Assembler_setting != 'None':
            DEFAULT_ASSEMBLER = Assembler_setting


class Settings(QWidget):
    POSITIONS = [(0, 0), (1, 0), (0, 1), (1, 1)]

    def __init__(self, parent):
        super(Settings, self).__init__(parent)
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.jbrowse_label = QLabel("JBrowse Root: " + JBROWSE_ROOT, self)
        self.assembler_label = QLabel("Assembler: " + DEFAULT_ASSEMBLER, self)

        self.grid.addWidget(self.jbrowse_label, *(0, 1))
        self.grid.addWidget(self.assembler_label, *(1, 0))
        self.assembler_buttons_layout = QGridLayout()
        self.grid.addLayout(self.assembler_buttons_layout, 1, 1)

        self.all_assemblers = [QPushButton('SPAdes', self), QPushButton('A5', self),
                               QPushButton('ABySS', self), QPushButton('Velvet', self),
                               QPushButton('SOAPdenovo2', self), QPushButton('DISCOVAR', self),
                               QPushButton('MaSuRCA', self), QPushButton('Newbler', self)]

        self.add_buttons()
        self.update_buttons(DEFAULT_ASSEMBLER)

    def add_buttons(self):
        jbrowse_button = QPushButton('JBrowse', self)
        jbrowse_button.clicked.connect(self.update_jbrowse_labels)
        jbrowse_button.resize(jbrowse_button.sizeHint())
        self.grid.addWidget(jbrowse_button, *(0, 0))

        for index in range(0, len(self.all_assemblers)):
            button = self.all_assemblers[index]
            button.setCheckable(True)
            button.clicked[bool].connect(self.update_assembler)
            self.assembler_buttons_layout.addWidget(button, *(index, 0))

    def update_assembler(self, pressed):
        source = self.sender()
        if pressed:
            self.update_buttons(source.text())

    def update_buttons(self, source_text):
        global DEFAULT_ASSEMBLER
        for button in self.all_assemblers:
            if button.text() == source_text:
                DEFAULT_ASSEMBLER = button.text()
                button.setChecked(True)
                self.assembler_label.setText("Assembler: " + DEFAULT_ASSEMBLER)
                write_configuration_file('Assembler', DEFAULT_ASSEMBLER)
            else:
                button.setChecked(False)

    def update_jbrowse_labels(self):
        global JBROWSE_ROOT
        directory_url = QFileDialog.getExistingDirectory(self, 'Open Directory',
                                                         '/Library', QFileDialog.ShowDirsOnly)
        if directory_url:
            JBROWSE_ROOT = directory_url
            self.jbrowse_label.setText("JBrowse Root: " + JBROWSE_ROOT)
            self.jbrowse_label.sizeHint()
            self.jbrowse_label.repaint()
            write_configuration_file('JBrowse_Root', JBROWSE_ROOT)


class Home(QWidget):
    def __init__(self, parent):
        super(Home, self).__init__(parent)
        new_label = QLabel("NEW LABEL", self)
        new_label.move(145, 50)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JBrowseApplication()
    sys.exit(app.exec_())
