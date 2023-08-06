# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'multiplayer_session.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_MultiplayerSessionWindow(object):
    def setupUi(self, MultiplayerSessionWindow):
        if not MultiplayerSessionWindow.objectName():
            MultiplayerSessionWindow.setObjectName(u"MultiplayerSessionWindow")
        MultiplayerSessionWindow.resize(773, 418)
        MultiplayerSessionWindow.setDockNestingEnabled(True)
        self.action_add_player = QAction(MultiplayerSessionWindow)
        self.action_add_player.setObjectName(u"action_add_player")
        self.action_add_row = QAction(MultiplayerSessionWindow)
        self.action_add_row.setObjectName(u"action_add_row")
        self.rename_session_action = QAction(MultiplayerSessionWindow)
        self.rename_session_action.setObjectName(u"rename_session_action")
        self.change_password_action = QAction(MultiplayerSessionWindow)
        self.change_password_action.setObjectName(u"change_password_action")
        self.delete_session_action = QAction(MultiplayerSessionWindow)
        self.delete_session_action.setObjectName(u"delete_session_action")
        self.actionbar = QAction(MultiplayerSessionWindow)
        self.actionbar.setObjectName(u"actionbar")
        self.actionasdf = QAction(MultiplayerSessionWindow)
        self.actionasdf.setObjectName(u"actionasdf")
        self.central_widget = QWidget(MultiplayerSessionWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.central_widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_players = QWidget()
        self.tab_players.setObjectName(u"tab_players")
        self.tabWidget.addTab(self.tab_players, "")
        self.tab_session = QWidget()
        self.tab_session.setObjectName(u"tab_session")
        self.session_tab_layout = QGridLayout(self.tab_session)
        self.session_tab_layout.setSpacing(6)
        self.session_tab_layout.setContentsMargins(11, 11, 11, 11)
        self.session_tab_layout.setObjectName(u"session_tab_layout")
        self.session_game_group = QGroupBox(self.tab_session)
        self.session_game_group.setObjectName(u"session_game_group")
        self.session_game_layout = QGridLayout(self.session_game_group)
        self.session_game_layout.setSpacing(6)
        self.session_game_layout.setContentsMargins(11, 11, 11, 11)
        self.session_game_layout.setObjectName(u"session_game_layout")
        self.generate_game_label = QLabel(self.session_game_group)
        self.generate_game_label.setObjectName(u"generate_game_label")
        self.generate_game_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.session_game_layout.addWidget(self.generate_game_label, 1, 0, 1, 2)

        self.generate_game_button = QPushButton(self.session_game_group)
        self.generate_game_button.setObjectName(u"generate_game_button")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generate_game_button.sizePolicy().hasHeightForWidth())
        self.generate_game_button.setSizePolicy(sizePolicy)

        self.session_game_layout.addWidget(self.generate_game_button, 2, 0, 1, 1)


        self.session_tab_layout.addWidget(self.session_game_group, 0, 0, 1, 2)

        self.session_admin_group = QGroupBox(self.tab_session)
        self.session_admin_group.setObjectName(u"session_admin_group")
        self.session_admin_layout = QGridLayout(self.session_admin_group)
        self.session_admin_layout.setSpacing(6)
        self.session_admin_layout.setContentsMargins(11, 11, 11, 11)
        self.session_admin_layout.setObjectName(u"session_admin_layout")
        self.copy_permalink_button = QPushButton(self.session_admin_group)
        self.copy_permalink_button.setObjectName(u"copy_permalink_button")

        self.session_admin_layout.addWidget(self.copy_permalink_button, 1, 0, 1, 1)

        self.session_status_button = QPushButton(self.session_admin_group)
        self.session_status_button.setObjectName(u"session_status_button")

        self.session_admin_layout.addWidget(self.session_status_button, 0, 1, 1, 1)

        self.view_game_details_button = QPushButton(self.session_admin_group)
        self.view_game_details_button.setObjectName(u"view_game_details_button")

        self.session_admin_layout.addWidget(self.view_game_details_button, 0, 0, 1, 1)

        self.advanced_options_tool = QPushButton(self.session_admin_group)
        self.advanced_options_tool.setObjectName(u"advanced_options_tool")
        sizePolicy.setHeightForWidth(self.advanced_options_tool.sizePolicy().hasHeightForWidth())
        self.advanced_options_tool.setSizePolicy(sizePolicy)

        self.session_admin_layout.addWidget(self.advanced_options_tool, 1, 1, 1, 1)


        self.session_tab_layout.addWidget(self.session_admin_group, 1, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.session_tab_layout.addItem(self.verticalSpacer, 4, 0, 1, 2)

        self.connectivity_group = QGroupBox(self.tab_session)
        self.connectivity_group.setObjectName(u"connectivity_group")
        self.connectivity_layout = QGridLayout(self.connectivity_group)
        self.connectivity_layout.setSpacing(6)
        self.connectivity_layout.setContentsMargins(11, 11, 11, 11)
        self.connectivity_layout.setObjectName(u"connectivity_layout")
        self.server_connection_button = QPushButton(self.connectivity_group)
        self.server_connection_button.setObjectName(u"server_connection_button")

        self.connectivity_layout.addWidget(self.server_connection_button, 1, 0, 1, 1)

        self.edit_game_connections_button = QPushButton(self.connectivity_group)
        self.edit_game_connections_button.setObjectName(u"edit_game_connections_button")

        self.connectivity_layout.addWidget(self.edit_game_connections_button, 1, 1, 1, 1)

        self.server_connection_label = QLabel(self.connectivity_group)
        self.server_connection_label.setObjectName(u"server_connection_label")

        self.connectivity_layout.addWidget(self.server_connection_label, 0, 0, 1, 1)

        self.multiworld_client_status_label = QLabel(self.connectivity_group)
        self.multiworld_client_status_label.setObjectName(u"multiworld_client_status_label")
        self.multiworld_client_status_label.setTextFormat(Qt.MarkdownText)
        self.multiworld_client_status_label.setWordWrap(True)

        self.connectivity_layout.addWidget(self.multiworld_client_status_label, 2, 0, 1, 2)


        self.session_tab_layout.addWidget(self.connectivity_group, 2, 0, 1, 2)

        self.tabWidget.addTab(self.tab_session, "")
        self.tab_history = QTableWidget()
        if (self.tab_history.columnCount() < 5):
            self.tab_history.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tab_history.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tab_history.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tab_history.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tab_history.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tab_history.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tab_history.setObjectName(u"tab_history")
        self.tab_history.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tab_history.setSortingEnabled(True)
        self.tabWidget.addTab(self.tab_history, "")
        self.tab_audit = QTableWidget()
        if (self.tab_audit.columnCount() < 3):
            self.tab_audit.setColumnCount(3)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tab_audit.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tab_audit.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tab_audit.setHorizontalHeaderItem(2, __qtablewidgetitem7)
        self.tab_audit.setObjectName(u"tab_audit")
        self.tab_audit.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tab_audit.setSortingEnabled(True)
        self.tabWidget.addTab(self.tab_audit, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.progress_label = QLabel(self.central_widget)
        self.progress_label.setObjectName(u"progress_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.progress_label.sizePolicy().hasHeightForWidth())
        self.progress_label.setSizePolicy(sizePolicy1)
        self.progress_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.progress_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.progress_label)

        self.background_process_layout = QHBoxLayout()
        self.background_process_layout.setSpacing(6)
        self.background_process_layout.setObjectName(u"background_process_layout")
        self.background_process_button = QPushButton(self.central_widget)
        self.background_process_button.setObjectName(u"background_process_button")
        self.background_process_button.setMinimumSize(QSize(140, 0))

        self.background_process_layout.addWidget(self.background_process_button)

        self.progress_bar = QProgressBar(self.central_widget)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)
        self.progress_bar.setInvertedAppearance(False)

        self.background_process_layout.addWidget(self.progress_bar)


        self.verticalLayout.addLayout(self.background_process_layout)

        MultiplayerSessionWindow.setCentralWidget(self.central_widget)
        self.menu_bar = QMenuBar(MultiplayerSessionWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 773, 17))
        MultiplayerSessionWindow.setMenuBar(self.menu_bar)

        self.retranslateUi(MultiplayerSessionWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MultiplayerSessionWindow)
    # setupUi

    def retranslateUi(self, MultiplayerSessionWindow):
        MultiplayerSessionWindow.setWindowTitle(QCoreApplication.translate("MultiplayerSessionWindow", u"Multiworld Session", None))
        self.action_add_player.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Add player", None))
        self.action_add_row.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Add row", None))
        self.rename_session_action.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Change title", None))
        self.change_password_action.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Change password", None))
        self.delete_session_action.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Delete session", None))
        self.actionbar.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"bar", None))
        self.actionasdf.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"asdf", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_players), QCoreApplication.translate("MultiplayerSessionWindow", u"Players", None))
        self.session_game_group.setTitle(QCoreApplication.translate("MultiplayerSessionWindow", u"Session Game", None))
        self.generate_game_label.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"<Game not generated>", None))
        self.generate_game_button.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Generate Game", None))
        self.session_admin_group.setTitle(QCoreApplication.translate("MultiplayerSessionWindow", u"Session Administration", None))
        self.copy_permalink_button.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Copy Permalink", None))
        self.session_status_button.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Start", None))
        self.view_game_details_button.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"View Spoiler", None))
        self.advanced_options_tool.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Advanced options...", None))
        self.connectivity_group.setTitle(QCoreApplication.translate("MultiplayerSessionWindow", u"Connectivity", None))
        self.server_connection_button.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Connect to Server", None))
        self.edit_game_connections_button.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Edit Game Connections", None))
        self.server_connection_label.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Server: Disconnected", None))
        self.multiworld_client_status_label.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_session), QCoreApplication.translate("MultiplayerSessionWindow", u"Session and Connectivity", None))
        ___qtablewidgetitem = self.tab_history.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Provider", None));
        ___qtablewidgetitem1 = self.tab_history.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Receiver", None));
        ___qtablewidgetitem2 = self.tab_history.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Pickup", None));
        ___qtablewidgetitem3 = self.tab_history.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Location", None));
        ___qtablewidgetitem4 = self.tab_history.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Time", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_history), QCoreApplication.translate("MultiplayerSessionWindow", u"History", None))
        ___qtablewidgetitem5 = self.tab_audit.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"User", None));
        ___qtablewidgetitem6 = self.tab_audit.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Message", None));
        ___qtablewidgetitem7 = self.tab_audit.horizontalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Time", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_audit), QCoreApplication.translate("MultiplayerSessionWindow", u"Audit Log", None))
        self.progress_label.setText("")
        self.background_process_button.setText(QCoreApplication.translate("MultiplayerSessionWindow", u"Stop", None))
    # retranslateUi

