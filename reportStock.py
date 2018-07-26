from fileWriter import savefile

from models import DB_Sp_Incoming
from PyQt5.QtWidgets import QTableWidgetItem

class StockRepotHandlers:

    def __init__(self, main):
        self.main = main

        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_Stock_report)
        self.main.pushButton_Stock_report_Back.clicked.connect(self.backButton)
        self.main.pushButton_Stock_report_refresh.clicked.connect(self.search)
        self.main.pushButton_Stock_report_excel.clicked.connect(self.savefile)
        self.accept_reject()

    def backButton(self):
        self.main.stackedWidget_SP.setCurrentWidget(self.main.pageReports)

    def accept_reject(self):

        self.main.buttonBox_Stock_report_.accepted.connect(self.accept)
        self.main.buttonBox_Stock_report_.rejected.connect(self.reject)

    def accept(self):
        print('accept')

    def reject(self):
        self.main.close()

    def search(self):

        self.headers = ['spn', 'dpn', 'invoice_number', 'qty', 'price', 'store', 'description',\
                   'date_order', 'date_incoming', 'type_sp']

        self.main.tableWidget_Stock_report.clear()
        self.main.tableWidget_Stock_report.setHorizontalHeaderLabels(self.headers)
        records = self.main.session.query(DB_Sp_Incoming).all()
        numrows = len(records)
        if numrows > 0:
            numcolums = len(self.headers)
            tabwidget = self.main.tableWidget_Stock_report

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

       savefile(tableWidget=(self.main.tableWidget_Stock_report), headers=self.headers)

