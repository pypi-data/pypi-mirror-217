# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_preset_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from randovania.gui.lib.preset_tree_widget import *  # type: ignore

class Ui_SelectPresetDialog(object):
    def setupUi(self, SelectPresetDialog):
        if not SelectPresetDialog.objectName():
            SelectPresetDialog.setObjectName(u"SelectPresetDialog")
        SelectPresetDialog.resize(548, 438)
        self.gridLayout = QGridLayout(SelectPresetDialog)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.accept_button = QPushButton(SelectPresetDialog)
        self.accept_button.setObjectName(u"accept_button")

        self.gridLayout.addWidget(self.accept_button, 3, 0, 1, 1)

        self.create_preset_tree = PresetTreeWidget(SelectPresetDialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.create_preset_tree.setHeaderItem(__qtreewidgetitem)
        self.create_preset_tree.setObjectName(u"create_preset_tree")
        self.create_preset_tree.setHeaderHidden(True)

        self.gridLayout.addWidget(self.create_preset_tree, 2, 0, 1, 1)

        self.cancel_button = QPushButton(SelectPresetDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.gridLayout.addWidget(self.cancel_button, 3, 1, 1, 1)

        self.create_scroll_area = QScrollArea(SelectPresetDialog)
        self.create_scroll_area.setObjectName(u"create_scroll_area")
        self.create_scroll_area.setWidgetResizable(True)
        self.create_scroll_area_contents = QWidget()
        self.create_scroll_area_contents.setObjectName(u"create_scroll_area_contents")
        self.create_scroll_area_contents.setGeometry(QRect(0, 0, 264, 350))
        self.create_scroll_area_layout = QVBoxLayout(self.create_scroll_area_contents)
        self.create_scroll_area_layout.setSpacing(6)
        self.create_scroll_area_layout.setContentsMargins(11, 11, 11, 11)
        self.create_scroll_area_layout.setObjectName(u"create_scroll_area_layout")
        self.create_scroll_area_layout.setContentsMargins(4, 4, 4, 4)
        self.create_preset_description = QLabel(self.create_scroll_area_contents)
        self.create_preset_description.setObjectName(u"create_preset_description")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.create_preset_description.sizePolicy().hasHeightForWidth())
        self.create_preset_description.setSizePolicy(sizePolicy)
        self.create_preset_description.setMinimumSize(QSize(0, 40))
        self.create_preset_description.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.create_preset_description.setWordWrap(True)

        self.create_scroll_area_layout.addWidget(self.create_preset_description)

        self.create_scroll_area.setWidget(self.create_scroll_area_contents)

        self.gridLayout.addWidget(self.create_scroll_area, 2, 1, 1, 1)

        self.world_name_label = QLabel(SelectPresetDialog)
        self.world_name_label.setObjectName(u"world_name_label")

        self.gridLayout.addWidget(self.world_name_label, 0, 0, 1, 1)

        self.world_name_edit = QLineEdit(SelectPresetDialog)
        self.world_name_edit.setObjectName(u"world_name_edit")

        self.gridLayout.addWidget(self.world_name_edit, 0, 1, 1, 1)

        self.game_selection_combo = QComboBox(SelectPresetDialog)
        self.game_selection_combo.setObjectName(u"game_selection_combo")

        self.gridLayout.addWidget(self.game_selection_combo, 1, 0, 1, 2)


        self.retranslateUi(SelectPresetDialog)

        QMetaObject.connectSlotsByName(SelectPresetDialog)
    # setupUi

    def retranslateUi(self, SelectPresetDialog):
        SelectPresetDialog.setWindowTitle(QCoreApplication.translate("SelectPresetDialog", u"Select Preset", None))
        self.accept_button.setText(QCoreApplication.translate("SelectPresetDialog", u"Accept", None))
        self.cancel_button.setText(QCoreApplication.translate("SelectPresetDialog", u"Cancel", None))
        self.create_preset_description.setText(QCoreApplication.translate("SelectPresetDialog", u"<html><head/><body><p>This content should have been replaced by code.</p></body></html>", None))
        self.world_name_label.setText(QCoreApplication.translate("SelectPresetDialog", u"World name", None))
        self.world_name_edit.setPlaceholderText(QCoreApplication.translate("SelectPresetDialog", u"World name", None))
    # retranslateUi

