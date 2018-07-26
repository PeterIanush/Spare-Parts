"""GUI"""
from mainguiSP import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore

"""sqlAlchemy"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User
from incoming import IncomingHandlers
from equipment import EquipmentHandlers
from parts import PartsHandlers
from maintenance import MaintenanceHandlers
from operators import OperatorsHandlers
from outgoing import OutgoingHandlers
from crimping_die import CrimpingDieHandlers
from crimping_maintenance import CrimpingMaintenanceHandlers
from crimping_terminal import  CrimpingTerminalHandlers
from reportStock import  StockRepotHandlers

"""for creating .exe"""
import  pyodbc
Base = declarative_base()

class InitMain(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):

        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.stackedWidget_SP.setCurrentWidget(self.pageLogin)
        self.logining()
        self.lineEditLogin.editingFinished.connect(self.check_state)
        self.initSessionKanban()
        self.initSessionStopNet()


    def validator_login(self):

        reg_ex = QtCore.QRegExp('[0-9a-zA-Z]{4,8}')
        input_validator = QtGui.QRegExpValidator(reg_ex)
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditLogin.setValidator(input_validator)

    def check_state(self, *args, **kwargs):

        self.validator_login()
        state, *others = self.lineEditLogin.validator().validate(self.lineEditLogin.text(), 1)
        if state != 1:
            print('Bad data')
        else:
            print('Thanx')

    def logining(self):

        self.buttonBox.rejected.connect(self.click_cancel_logining)
        self.buttonBox.accepted.connect(self.click_OK_logining)
        #self.buttonBox.accepted.connect(self.page_main_show)

    def page_main_show(self):

        self.stackedWidget_SP.setCurrentWidget(self.page_main)
        self.pushButton_Main_Spare_Parts.clicked.connect(self.move_to_pageSP)
        self.pushButton_Main_Report.clicked.connect(self.move_to_pageReports)
        self.pushButton_Main_Spare_Parts.clicked.connect(self.pageMainClick)
        self.pushButtonInput.clicked.connect(self.move_to_incoming)
        self.pushButtonEquipment.clicked.connect(self.move_to_equipment)
        self.pushButtonParts.clicked.connect(self.move_to_parts)
        self.pushButtonEngeneer.clicked.connect(self.move_to_maintenance)
        self.pushButtonOperator.clicked.connect(self.move_to_operators)
        self.pushButtonStok.clicked.connect(self.move_to_outgoing)
        self.pushButton_Crimping_Die.clicked.connect(self.move_to_crimping_main)
        self.pushButton_Crimping_Select_Back.clicked.connect(self.move_to_page_main)
        self.pushButton_Main_Page_Back.clicked.connect(self.move_to_page_main)
        self.pushButton_Crimping_Select_Crimping_Tool.clicked.connect(self.move_to_crimping_die)
        self.pushButton_Crimping_Select_Tool.clicked.connect(self.move_to_crimping_terminal)
        self.pushButton_Crimping_Maintenance.clicked.connect(self.move_to_crimping_maintenace)
        self.pushButton_Reports_Back.clicked.connect(self.move_to_page_main)
        self.pushButtonStockReport.clicked.connect(self.move_to_report_Stock)


    def click_OK_logining(self):
        '''check login in DB'''
        login = self.lineEditLogin.text()
        password = self.lineEditPassword.text()
        users = session.query(User).filter(User.login == login).all()
        if len(users) == 0:
            self.labelLogining.setStyleSheet("QLabel{ background-color : red; color : white; }")
            self.lineEditLogin.clear()
            self.lineEditPassword.clear()
        else:
            if users[0].password == password:
                self.page_main_show()
            else:
                self.labelPassword.setStyleSheet("QLabel{ background-color : red; color : white; }")

    def move_to_pageReports(self):

        self.stackedWidget_SP.setCurrentWidget(self.pageReports)

    def move_to_pageSP(self):

        self.stackedWidget_SP.setCurrentWidget(self.page_main)

    def click_cancel_logining(self):

        self.close()


    def get_current_window(self):

        self.current_page = self.stackedWidget_SP.currentWidget()
        self.group_box_pageMain = self.stackedWidget_SP.currentWidget().sender().parent().title()
        self.list_w = self.stackedWidget_SP.currentWidget().findChildren(QtWidgets.QGroupBox)

    def move_to_previos_widget(self):

        self.stackedWidget_SP.setCurrentWidget(self.current_page)

    def move_to_incoming(self):

        self.incoming = IncomingHandlers(self)

    def move_to_equipment(self):

        self.equipment = EquipmentHandlers(self)

    def move_to_parts(self):

        self.part = PartsHandlers(self)

    def move_to_maintenance(self):

        self.maintenance = MaintenanceHandlers(self)

    def move_to_operators(self):

        self.operators = OperatorsHandlers(self)

    def move_to_outgoing(self):

        self.outgoing = OutgoingHandlers(self)

    def move_to_page_main(self):

        self.stackedWidget_SP.setCurrentWidget(self.page_main)

    def move_to_crimping_main(self):

        self.stackedWidget_SP.setCurrentWidget(self.page_Crimping_Select)

    def move_to_crimping_die(self):

        self.crimping_die = CrimpingDieHandlers(self)

    def move_to_crimping_maintenace(self):

        self.crimping_mintenance = CrimpingMaintenanceHandlers(self)

    def move_to_crimping_terminal(self):

        self.crimping_terminal = CrimpingTerminalHandlers(self)

    def move_to_report_Stock(self):

        self.report_Stock = StockRepotHandlers(self)



    def pageMainClick(self):

        self.stackedWidget_SP.setCurrentWidget(self.pageMain)

    def initSessionKanban(self):

        engine = create_engine("mssql+pyodbc://sa:Prettl!@#4@kanban")
        #Base.metadata.bind = engine
        dbSession = sessionmaker(bind=engine)
        self.session = dbSession()
        self.tableWidget_Stock_report.horizontalHeader().count()

    def initSessionStopNet(self):

        engine = create_engine("mssql+pyodbc://sa:Prettl!@#4@stopnet")
        #BaseStN.metadata.bind = engine
        dbSession = sessionmaker(bind=engine)
        self.sessionStN = dbSession()
        #self.label_maintenance_Name.set




if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    engine = create_engine("mssql+pyodbc://sa:Prettl!@#4@kanban")
    Base.metadata.bind = engine
    DbSession = sessionmaker(bind=engine)
    session = DbSession()
    app.session = session

    window = InitMain()
    window.show()
    sys.exit(app.exec_())



