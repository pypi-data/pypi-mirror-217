# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_am2r_patches.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PresetAM2RPatches(object):
    def setupUi(self, PresetAM2RPatches):
        if not PresetAM2RPatches.objectName():
            PresetAM2RPatches.setObjectName(u"PresetAM2RPatches")
        PresetAM2RPatches.resize(770, 660)
        self.root_widget = QWidget(PresetAM2RPatches)
        self.root_widget.setObjectName(u"root_widget")
        self.root_widget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.root_widget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = QScrollArea(self.root_widget)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_contents = QWidget()
        self.scroll_contents.setObjectName(u"scroll_contents")
        self.scroll_contents.setGeometry(QRect(0, 0, 766, 656))
        self.scroll_layout = QVBoxLayout(self.scroll_contents)
        self.scroll_layout.setSpacing(6)
        self.scroll_layout.setContentsMargins(11, 11, 11, 11)
        self.scroll_layout.setObjectName(u"scroll_layout")
        self.scroll_layout.setContentsMargins(0, 2, 0, 0)
        self.top_spacer = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.scroll_layout.addItem(self.top_spacer)

        self.room_group = QGroupBox(self.scroll_contents)
        self.room_group.setObjectName(u"room_group")
        self.unlock_layout = QVBoxLayout(self.room_group)
        self.unlock_layout.setSpacing(6)
        self.unlock_layout.setContentsMargins(11, 11, 11, 11)
        self.unlock_layout.setObjectName(u"unlock_layout")
        self.septogg_helpers_check = QCheckBox(self.room_group)
        self.septogg_helpers_check.setObjectName(u"septogg_helpers_check")

        self.unlock_layout.addWidget(self.septogg_helpers_check)

        self.septogg_helpers_label = QLabel(self.room_group)
        self.septogg_helpers_label.setObjectName(u"septogg_helpers_label")
        self.septogg_helpers_label.setWordWrap(True)

        self.unlock_layout.addWidget(self.septogg_helpers_label)

        self.change_level_design_check = QCheckBox(self.room_group)
        self.change_level_design_check.setObjectName(u"change_level_design_check")

        self.unlock_layout.addWidget(self.change_level_design_check)

        self.change_level_design_label = QLabel(self.room_group)
        self.change_level_design_label.setObjectName(u"change_level_design_label")
        self.change_level_design_label.setWordWrap(True)

        self.unlock_layout.addWidget(self.change_level_design_label)

        self.respawn_bomb_blocks_check = QCheckBox(self.room_group)
        self.respawn_bomb_blocks_check.setObjectName(u"respawn_bomb_blocks_check")

        self.unlock_layout.addWidget(self.respawn_bomb_blocks_check)

        self.respawn_bomb_blocks_label = QLabel(self.room_group)
        self.respawn_bomb_blocks_label.setObjectName(u"respawn_bomb_blocks_label")
        self.respawn_bomb_blocks_label.setWordWrap(True)

        self.unlock_layout.addWidget(self.respawn_bomb_blocks_label)


        self.scroll_layout.addWidget(self.room_group)

        self.misc_group = QGroupBox(self.scroll_contents)
        self.misc_group.setObjectName(u"misc_group")
        self.raven_beak_damage_table_handling_layout = QVBoxLayout(self.misc_group)
        self.raven_beak_damage_table_handling_layout.setSpacing(6)
        self.raven_beak_damage_table_handling_layout.setContentsMargins(11, 11, 11, 11)
        self.raven_beak_damage_table_handling_layout.setObjectName(u"raven_beak_damage_table_handling_layout")
        self.skip_cutscenes_check = QCheckBox(self.misc_group)
        self.skip_cutscenes_check.setObjectName(u"skip_cutscenes_check")

        self.raven_beak_damage_table_handling_layout.addWidget(self.skip_cutscenes_check)

        self.skip_cutscenes_label = QLabel(self.misc_group)
        self.skip_cutscenes_label.setObjectName(u"skip_cutscenes_label")
        self.skip_cutscenes_label.setWordWrap(True)

        self.raven_beak_damage_table_handling_layout.addWidget(self.skip_cutscenes_label)


        self.scroll_layout.addWidget(self.misc_group)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.scroll_layout.addItem(self.verticalSpacer)

        self.scroll_area.setWidget(self.scroll_contents)

        self.verticalLayout.addWidget(self.scroll_area)

        PresetAM2RPatches.setCentralWidget(self.root_widget)

        self.retranslateUi(PresetAM2RPatches)

        QMetaObject.connectSlotsByName(PresetAM2RPatches)
    # setupUi

    def retranslateUi(self, PresetAM2RPatches):
        PresetAM2RPatches.setWindowTitle(QCoreApplication.translate("PresetAM2RPatches", u"Other", None))
        self.room_group.setTitle(QCoreApplication.translate("PresetAM2RPatches", u"Room Design", None))
        self.septogg_helpers_check.setText(QCoreApplication.translate("PresetAM2RPatches", u"Enable Septogg Helpers", None))
        self.septogg_helpers_label.setText(QCoreApplication.translate("PresetAM2RPatches", u"<html><head/><body><p>Septoggs will appear in certain rooms, helping you reach higher platforms if you don't have the means to reach them yourself. Due to SR-388's cave structure, this setting is <b>highly recommended</b>.</p></body></html>", None))
        self.change_level_design_check.setText(QCoreApplication.translate("PresetAM2RPatches", u"Dynamically change room geometry", None))
        self.change_level_design_label.setText(QCoreApplication.translate("PresetAM2RPatches", u"<html><head/><body><p>Dynamically changes the room geometry based on whether you have certain items collected. Certain bomb blocks will become shoot blocks, some crumble blocks will dissapear etc.</p></body></html>", None))
        self.respawn_bomb_blocks_check.setText(QCoreApplication.translate("PresetAM2RPatches", u"Respawn destructable bomb blocks", None))
        self.respawn_bomb_blocks_label.setText(QCoreApplication.translate("PresetAM2RPatches", u"<html><head/><body><p>Makes most destructable bomb blocks respawn. Disabling this will make certain rooms easier to traverse if you only have Power Bombs.</p></body></html>", None))
        self.misc_group.setTitle(QCoreApplication.translate("PresetAM2RPatches", u"Miscellaneous", None))
        self.skip_cutscenes_check.setText(QCoreApplication.translate("PresetAM2RPatches", u"Skip most cutscenes", None))
        self.skip_cutscenes_label.setText(QCoreApplication.translate("PresetAM2RPatches", u"<html><head/><body><p>Enabling this will skip most cutscene related events, such as the Drill Sequence, the cutscenes you'll see when viewing a Metroid for the first time and similar.</p></body></html>", None))
    # retranslateUi

