#!/usr/bin/python3

import appdirs
import sys
import os
import platform

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt

import qdarkstyle

if platform.system() == 'Linux':
    RESOURCES = '/usr/local/share/axie-counter'
LIGHTNING_ICON_ICO = os.path.join(RESOURCES, 'lightning_icon.ico')
LIGHTNING_ICON_PNG = os.path.join(RESOURCES, 'lightning_icon.png')
print(LIGHTNING_ICON_ICO)


class MainCounter(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # ---- UI ----
        self.setWindowTitle(self.tr("Axie Energy Counter"))
        self.setStyleSheet(
            "margin-top: 50; margin-bottom:50; margin-right: 50")
        self.setMinimumWidth(1024)
        # ---- Content ----
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)


class MainWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # ---- Content ----
        self.layout = QHBoxLayout()
        # Number
        self.number = 0
        self.number_label = QLabel("0")
        self.number_label.setAlignment(Qt.AlignCenter)

        number_font = QFont()
        number_font.setPointSize(500)
        number_font.setWeight(600)
        self.number_label.setFont(number_font)

        self.layout.addWidget(self.number_label)

        # Buttons
        self.buttons_lyt = QVBoxLayout()
        self.buttons_lyt.setSpacing(0)

        pxmap = QPixmap(LIGHTNING_ICON_PNG)
        self.lighting_icon = QLabel()
        self.lighting_icon.setFixedWidth(pxmap.width())
        self.lighting_icon.setStyleSheet('margin: 0 50 0 0')
        self.lighting_icon.setAlignment(Qt.AlignCenter)
        self.lighting_icon.setPixmap(pxmap)

        self.plus_one = ChangeButton('+')
        self.plus_one.setFixedSize(pxmap.width(), pxmap.width()*1.1)

        self.minus_one = ChangeButton('-')
        self.minus_one.setFixedSize(pxmap.width(), pxmap.width()*1.1)

        self.buttons_lyt.addSpacerItem(QSpacerItem(
            QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.buttons_lyt.addWidget(self.plus_one)
        self.buttons_lyt.addWidget(self.lighting_icon)
        self.buttons_lyt.addWidget(self.minus_one)
        self.buttons_lyt.addSpacerItem(QSpacerItem(
            QSizePolicy.Expanding, QSizePolicy.Maximum))

        self.layout.addLayout(self.buttons_lyt)

        self.setLayout(self.layout)

        # Functionality
        self.plus_one.pressed.connect(self.increase)
        self.minus_one.pressed.connect(self.decrease)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Plus, Qt.Key_Right,Qt.Key_Up):
            self.increase()
        if event.key() in (Qt.Key_Minus, Qt.Key_Left, Qt.Key_Down):
            self.decrease()

    def increase(self):
        if self.number == 10:
            return
        self.number += 1
        self.number_label.setText(str(self.number))

    def decrease(self):
        if self.number == 0:
            return
        self.number -= 1
        self.number_label.setText(str(self.number))


class ChangeButton(QPushButton):
    def __init__(self, _type, *args, **kwargs):
        super().__init__(*args, *kwargs)
        # Text
        if _type not in ('+', '-'):
            raise ValueError('ChangeButton type has to be "+" or "-"')
        self.setText(f'{_type}1')
        self.setFont(ChangeButtonFont())
        # Style
        self.setStyleSheet(f"""
        QPushButton {{
        background-color: {"#3B7436" if _type=='+' else "#934D37"}; border-radius: 35px; border-width:0px;
        }}
        QPushButton::hover {{
        border-width: 2px; border-color: white; border-style: solid;
        }}
        QPushButton::pressed {{
        background-color:white; color:{"#3B7436" if _type=='+' else "#934D37"}
        }}
        """)

    def keyPressEvent(self, event):
        # Pass to parent so that it doesn't override
        self.parent().keyPressEvent(event)


class ChangeButtonFont(QFont):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.setPointSize(90)
        self.setWeight(500)


app = QApplication(sys.argv)
# Style
app.setWindowIcon(QIcon(LIGHTNING_ICON_ICO))
try:
    from PyQt5.QtWinExtras import QtWin
    myappid = 'axie'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
app.setFont(QFont('Roboto'))
# Main Window
w = MainCounter()
w.show()
app.exec()
