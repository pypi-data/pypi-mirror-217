# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'games_tab_am2r_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from randovania.gui.widgets.generate_game_widget import *  # type: ignore

class Ui_AM2RGameTabWidget(object):
    def setupUi(self, AM2RGameTabWidget):
        if not AM2RGameTabWidget.objectName():
            AM2RGameTabWidget.setObjectName(u"AM2RGameTabWidget")
        AM2RGameTabWidget.resize(574, 449)
        self.tab_intro = QWidget()
        self.tab_intro.setObjectName(u"tab_intro")
        self.intro_layout = QVBoxLayout(self.tab_intro)
        self.intro_layout.setSpacing(6)
        self.intro_layout.setContentsMargins(11, 11, 11, 11)
        self.intro_layout.setObjectName(u"intro_layout")
        self.intro_cover_layout = QHBoxLayout()
        self.intro_cover_layout.setSpacing(6)
        self.intro_cover_layout.setObjectName(u"intro_cover_layout")
        self.game_cover_label = QLabel(self.tab_intro)
        self.game_cover_label.setObjectName(u"game_cover_label")

        self.intro_cover_layout.addWidget(self.game_cover_label)

        self.intro_label = QLabel(self.tab_intro)
        self.intro_label.setObjectName(u"intro_label")
        self.intro_label.setWordWrap(True)

        self.intro_cover_layout.addWidget(self.intro_label)


        self.intro_layout.addLayout(self.intro_cover_layout)

        self.quick_generate_button = QPushButton(self.tab_intro)
        self.quick_generate_button.setObjectName(u"quick_generate_button")

        self.intro_layout.addWidget(self.quick_generate_button)

        self.intro_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.intro_layout.addItem(self.intro_spacer)

        AM2RGameTabWidget.addTab(self.tab_intro, "")
        self.tab_generate_game = GenerateGameWidget()
        self.tab_generate_game.setObjectName(u"tab_generate_game")
        AM2RGameTabWidget.addTab(self.tab_generate_game, "")
        self.faq_tab = QWidget()
        self.faq_tab.setObjectName(u"faq_tab")
        self.faq_layout = QGridLayout(self.faq_tab)
        self.faq_layout.setSpacing(6)
        self.faq_layout.setContentsMargins(11, 11, 11, 11)
        self.faq_layout.setObjectName(u"faq_layout")
        self.faq_layout.setContentsMargins(0, 0, 0, 0)
        self.faq_scroll_area = QScrollArea(self.faq_tab)
        self.faq_scroll_area.setObjectName(u"faq_scroll_area")
        self.faq_scroll_area.setWidgetResizable(True)
        self.faq_scroll_area_contents = QWidget()
        self.faq_scroll_area_contents.setObjectName(u"faq_scroll_area_contents")
        self.faq_scroll_area_contents.setGeometry(QRect(0, 0, 562, 408))
        self.faq_scroll_layout = QGridLayout(self.faq_scroll_area_contents)
        self.faq_scroll_layout.setSpacing(6)
        self.faq_scroll_layout.setContentsMargins(11, 11, 11, 11)
        self.faq_scroll_layout.setObjectName(u"faq_scroll_layout")
        self.faq_label = QLabel(self.faq_scroll_area_contents)
        self.faq_label.setObjectName(u"faq_label")
        self.faq_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.faq_label.setWordWrap(True)

        self.faq_scroll_layout.addWidget(self.faq_label, 0, 0, 1, 1)

        self.faq_scroll_area.setWidget(self.faq_scroll_area_contents)

        self.faq_layout.addWidget(self.faq_scroll_area, 0, 0, 1, 1)

        AM2RGameTabWidget.addTab(self.faq_tab, "")
        self.differences_tab = QWidget()
        self.differences_tab.setObjectName(u"differences_tab")
        self.verticalLayout_2 = QVBoxLayout(self.differences_tab)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.differences_scroll_area = QScrollArea(self.differences_tab)
        self.differences_scroll_area.setObjectName(u"differences_scroll_area")
        self.differences_scroll_area.setWidgetResizable(True)
        self.differences_scroll_contents = QWidget()
        self.differences_scroll_contents.setObjectName(u"differences_scroll_contents")
        self.differences_scroll_contents.setGeometry(QRect(0, 0, 842, 375))
        self.verticalLayout = QVBoxLayout(self.differences_scroll_contents)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.differences_label = QLabel(self.differences_scroll_contents)
        self.differences_label.setObjectName(u"differences_label")

        self.verticalLayout.addWidget(self.differences_label)

        self.differences_scroll_area.setWidget(self.differences_scroll_contents)

        self.verticalLayout_2.addWidget(self.differences_scroll_area)

        AM2RGameTabWidget.addTab(self.differences_tab, "")

        self.retranslateUi(AM2RGameTabWidget)

        AM2RGameTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AM2RGameTabWidget)
    # setupUi

    def retranslateUi(self, AM2RGameTabWidget):
        self.game_cover_label.setText(QCoreApplication.translate("AM2RGameTabWidget", u"TextLabel", None))
        self.intro_label.setText(QCoreApplication.translate("AM2RGameTabWidget", u"<html><head/><body><p align=\"justify\">AM2R: TODO!</p></body></html>", None))
        self.quick_generate_button.setText(QCoreApplication.translate("AM2RGameTabWidget", u"Quick generate", None))
        AM2RGameTabWidget.setTabText(AM2RGameTabWidget.indexOf(self.tab_intro), QCoreApplication.translate("AM2RGameTabWidget", u"Introduction", None))
        AM2RGameTabWidget.setTabText(AM2RGameTabWidget.indexOf(self.tab_generate_game), QCoreApplication.translate("AM2RGameTabWidget", u"Play", None))
        self.faq_label.setText(QCoreApplication.translate("AM2RGameTabWidget", u"# updated from code", None))
        AM2RGameTabWidget.setTabText(AM2RGameTabWidget.indexOf(self.faq_tab), QCoreApplication.translate("AM2RGameTabWidget", u"FAQ", None))
        self.differences_label.setText(QCoreApplication.translate("AM2RGameTabWidget", u"<html><head/><body><p>Randovania makes some changes to the original game in order to improve the game experience.</p><p>TODO: currently just writing down so I don't forget for the patchert</p><p><br/>- higher difficulties don't reduce amount of missile/supers/pbs/health per expansion, for that functionality use rdv's built-in features</p><p>- in GFS Thoth, both transitions on the Bridge are doors now for bettter door rando compat</p><p>- in Hydro Station, the connection from &quot;Water Turbine Station&quot; to &quot;Hydro Station Exterior&quot; has a door now for better door rando compat</p><p>- Reactor is always exploded, the Power Bomb Expansion from there is now located in the long destroyed shaft</p><p><br/></p></body></html>", None))
        AM2RGameTabWidget.setTabText(AM2RGameTabWidget.indexOf(self.differences_tab), QCoreApplication.translate("AM2RGameTabWidget", u"Differences", None))
        pass
    # retranslateUi

