# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_connection_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_GameConnectionWindow(object):
    def setupUi(self, GameConnectionWindow):
        if not GameConnectionWindow.objectName():
            GameConnectionWindow.setObjectName(u"GameConnectionWindow")
        GameConnectionWindow.resize(472, 288)
        self.centralwidget = QWidget(GameConnectionWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.root_layout = QGridLayout(self.centralwidget)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(4, 4, 4, 4)
        self.meta_group = QGroupBox(self.centralwidget)
        self.meta_group.setObjectName(u"meta_group")
        self.meta_group.setFlat(True)
        self.meta_layout = QHBoxLayout(self.meta_group)
        self.meta_layout.setObjectName(u"meta_layout")
        self.meta_layout.setContentsMargins(1, 1, 1, 1)
        self.add_builder_button = QToolButton(self.meta_group)
        self.add_builder_button.setObjectName(u"add_builder_button")
        self.add_builder_button.setPopupMode(QToolButton.InstantPopup)
        self.add_builder_button.setToolButtonStyle(Qt.ToolButtonTextOnly)

        self.meta_layout.addWidget(self.add_builder_button)


        self.root_layout.addWidget(self.meta_group, 1, 0, 1, 1)

        self.builders_scroll = QScrollArea(self.centralwidget)
        self.builders_scroll.setObjectName(u"builders_scroll")
        self.builders_scroll.setWidgetResizable(True)
        self.builders_content = QWidget()
        self.builders_content.setObjectName(u"builders_content")
        self.builders_content.setGeometry(QRect(0, 0, 462, 244))
        self.builders_layout = QVBoxLayout(self.builders_content)
        self.builders_layout.setObjectName(u"builders_layout")
        self.builders_layout.setContentsMargins(4, 4, 4, 4)
        self.builders_scroll.setWidget(self.builders_content)

        self.root_layout.addWidget(self.builders_scroll, 0, 0, 1, 1)

        GameConnectionWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(GameConnectionWindow)

        QMetaObject.connectSlotsByName(GameConnectionWindow)
    # setupUi

    def retranslateUi(self, GameConnectionWindow):
        GameConnectionWindow.setWindowTitle(QCoreApplication.translate("GameConnectionWindow", u"Game Connections", None))
        self.meta_group.setTitle("")
        self.add_builder_button.setText(QCoreApplication.translate("GameConnectionWindow", u"Add new connection", None))
    # retranslateUi

