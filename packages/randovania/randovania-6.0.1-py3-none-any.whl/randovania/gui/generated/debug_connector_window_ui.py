# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'debug_connector_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_DebugConnectorWindow(object):
    def setupUi(self, DebugConnectorWindow):
        if not DebugConnectorWindow.objectName():
            DebugConnectorWindow.setObjectName(u"DebugConnectorWindow")
        DebugConnectorWindow.resize(697, 430)
        self.central_widget = QWidget(DebugConnectorWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setMaximumSize(QSize(16777215, 16777215))
        self.central_widget.setLayoutDirection(Qt.LeftToRight)
        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.setSpacing(6)
        self.grid_layout.setContentsMargins(11, 11, 11, 11)
        self.grid_layout.setObjectName(u"grid_layout")
        self.reset_button = QPushButton(self.central_widget)
        self.reset_button.setObjectName(u"reset_button")

        self.grid_layout.addWidget(self.reset_button, 4, 3, 1, 1)

        self.messages_list = QListWidget(self.central_widget)
        self.messages_list.setObjectName(u"messages_list")

        self.grid_layout.addWidget(self.messages_list, 0, 2, 4, 2)

        self.inventory_box = QGroupBox(self.central_widget)
        self.inventory_box.setObjectName(u"inventory_box")
        self.gridLayout_2 = QGridLayout(self.inventory_box)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.inventory_scroll_area = QScrollArea(self.inventory_box)
        self.inventory_scroll_area.setObjectName(u"inventory_scroll_area")
        self.inventory_scroll_area.setWidgetResizable(True)
        self.inventory_scroll_contents = QWidget()
        self.inventory_scroll_contents.setObjectName(u"inventory_scroll_contents")
        self.inventory_scroll_contents.setGeometry(QRect(0, 0, 329, 304))
        self.inventory_scroll_layout = QVBoxLayout(self.inventory_scroll_contents)
        self.inventory_scroll_layout.setSpacing(6)
        self.inventory_scroll_layout.setContentsMargins(11, 11, 11, 11)
        self.inventory_scroll_layout.setObjectName(u"inventory_scroll_layout")
        self.inventory_scroll_layout.setContentsMargins(0, 0, -1, -1)
        self.inventory_label = QLabel(self.inventory_scroll_contents)
        self.inventory_label.setObjectName(u"inventory_label")

        self.inventory_scroll_layout.addWidget(self.inventory_label)

        self.inventory_scroll_area.setWidget(self.inventory_scroll_contents)

        self.gridLayout_2.addWidget(self.inventory_scroll_area, 0, 0, 1, 1)


        self.grid_layout.addWidget(self.inventory_box, 2, 0, 2, 2)

        self.collect_location_combo = QComboBox(self.central_widget)
        self.collect_location_combo.setObjectName(u"collect_location_combo")

        self.grid_layout.addWidget(self.collect_location_combo, 0, 0, 1, 2)

        self.collect_location_button = QPushButton(self.central_widget)
        self.collect_location_button.setObjectName(u"collect_location_button")

        self.grid_layout.addWidget(self.collect_location_button, 1, 1, 1, 1)

        self.collect_randomly_check = QCheckBox(self.central_widget)
        self.collect_randomly_check.setObjectName(u"collect_randomly_check")

        self.grid_layout.addWidget(self.collect_randomly_check, 4, 2, 1, 1)

        self.current_region_combo = QComboBox(self.central_widget)
        self.current_region_combo.setObjectName(u"current_region_combo")

        self.grid_layout.addWidget(self.current_region_combo, 4, 1, 1, 1)

        self.current_location_label = QLabel(self.central_widget)
        self.current_location_label.setObjectName(u"current_location_label")

        self.grid_layout.addWidget(self.current_location_label, 4, 0, 1, 1)

        DebugConnectorWindow.setCentralWidget(self.central_widget)
        self.menuBar = QMenuBar(DebugConnectorWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 697, 17))
        DebugConnectorWindow.setMenuBar(self.menuBar)

        self.retranslateUi(DebugConnectorWindow)

        QMetaObject.connectSlotsByName(DebugConnectorWindow)
    # setupUi

    def retranslateUi(self, DebugConnectorWindow):
        DebugConnectorWindow.setWindowTitle(QCoreApplication.translate("DebugConnectorWindow", u"Debug Backend", None))
        self.reset_button.setText(QCoreApplication.translate("DebugConnectorWindow", u"Finish", None))
        self.inventory_box.setTitle(QCoreApplication.translate("DebugConnectorWindow", u"Inventory", None))
        self.inventory_label.setText("")
        self.collect_location_button.setText(QCoreApplication.translate("DebugConnectorWindow", u"Collect Location", None))
        self.collect_randomly_check.setText(QCoreApplication.translate("DebugConnectorWindow", u"Collect locations randomly periodically", None))
        self.current_location_label.setText(QCoreApplication.translate("DebugConnectorWindow", u"Current Location", None))
    # retranslateUi

