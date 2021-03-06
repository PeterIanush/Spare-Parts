from fileWriter import savefile

from models import DB_Sp_History_Movement
from PyQt5.QtWidgets import QTableWidgetItem

class HistoryIncomingRepotHandlers:

    def __init__(self, main):
        self.main = main

        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_History_Incoming_report_report)
        self.main.buttonBox_History_Incoming_report_Back.clicked.connect(self.backButton)
        self.main.pushButton_History_Incoming_report_refresh.clicked.connect(self.search)
        self.main.pushButton_History_Incoming_report_excel.clicked.connect(self.savefile)
        self.accept_reject()

    def backButton(self):
        self.main.stackedWidget_SP.setCurrentWidget(self.main.pageReports)

    def accept_reject(self):

        self.main.buttonBox_History_Incoming_report_report.accepted.connect(self.accept)
        self.main.buttonBox_History_Incoming_report_report.rejected.connect(self.reject)

    def accept(self):
        self.main.tableWidget_History_Incoming_report_report.clear()
        self.backButton()

    def reject(self):
        self.main.close()

    def search(self):

        self.headers = ['id_incoming', 'dpn', 'qty', 'responsible', 'movement', 'description']

        self.main.tableWidget_History_Incoming_report_report.clear()
        self.main.tableWidget_History_Incoming_report_report.setHorizontalHeaderLabels(self.headers)
        records = self.main.session.query(DB_Sp_History_Movement).all()
        numrows = len(records)
        if numrows > 0:
            numcolums = len(self.headers)
            tabwidget = self.main.tableWidget_History_Incoming_report_report

            tabwidget.setRowCount(numrows)
            tabwidget.setColumnCount(numcolums)
            tabwidget.setHorizontalHeaderLabels(self.headers)
            for row, record in enumerate(records):
                for col, column_name in enumerate(self.headers):
                    value = vars(record)[column_name]
                    fieldValue = QTableWidgetItem(str(value))
                    tabwidget.setItem(row, col, fieldValue)
        else:
            print('Empty data')

    def savefile(self):

       savefile(tableWidget=(self.main.tableWidget_History_Incoming_report_report), headers=self.headers)

