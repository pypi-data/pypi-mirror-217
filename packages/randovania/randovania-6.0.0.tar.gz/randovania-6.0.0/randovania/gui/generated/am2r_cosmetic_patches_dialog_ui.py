# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'am2r_cosmetic_patches_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_AM2RCosmeticPatchesDialog(object):
    def setupUi(self, AM2RCosmeticPatchesDialog):
        if not AM2RCosmeticPatchesDialog.objectName():
            AM2RCosmeticPatchesDialog.setObjectName(u"AM2RCosmeticPatchesDialog")
        AM2RCosmeticPatchesDialog.resize(396, 246)
        self.gridLayout = QGridLayout(AM2RCosmeticPatchesDialog)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.reset_button = QPushButton(AM2RCosmeticPatchesDialog)
        self.reset_button.setObjectName(u"reset_button")

        self.gridLayout.addWidget(self.reset_button, 2, 2, 1, 1)

        self.accept_button = QPushButton(AM2RCosmeticPatchesDialog)
        self.accept_button.setObjectName(u"accept_button")

        self.gridLayout.addWidget(self.accept_button, 2, 0, 1, 1)

        self.cancel_button = QPushButton(AM2RCosmeticPatchesDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.gridLayout.addWidget(self.cancel_button, 2, 1, 1, 1)

        self.scrollArea = QScrollArea(AM2RCosmeticPatchesDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setObjectName(u"scroll_area_contents")
        self.scroll_area_contents.setGeometry(QRect(0, 0, 380, 190))
        self.verticalLayout = QVBoxLayout(self.scroll_area_contents)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scroll_area_contents)

        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)


        self.retranslateUi(AM2RCosmeticPatchesDialog)

        QMetaObject.connectSlotsByName(AM2RCosmeticPatchesDialog)
    # setupUi

    def retranslateUi(self, AM2RCosmeticPatchesDialog):
        AM2RCosmeticPatchesDialog.setWindowTitle(QCoreApplication.translate("AM2RCosmeticPatchesDialog", u"Blank Game - Cosmetic Options", None))
        self.reset_button.setText(QCoreApplication.translate("AM2RCosmeticPatchesDialog", u"Reset to Defaults", None))
        self.accept_button.setText(QCoreApplication.translate("AM2RCosmeticPatchesDialog", u"Accept", None))
        self.cancel_button.setText(QCoreApplication.translate("AM2RCosmeticPatchesDialog", u"Cancel", None))
    # retranslateUi

