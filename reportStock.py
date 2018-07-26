import xlwt
import xlsxwriter
from os import PathLike
from numpy import unicode

from models import DB_Sp_Incoming
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog

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
        self.main.tableWidget_Stock_report.setHorizontalHeaderLabels(headers)
        records = self.main.session.query(DB_Sp_Incoming).all()
        numrows = len(records)
        if numrows > 0:
            numcolums = len(headers)
            tabwidget = self.main.tableWidget_Stock_report

            tabwidget.setRowCount(numrows)
            tabwidget.setColumnCount(numcolums)
            tabwidget.setHorizontalHeaderLabels(headers)
            for row, record in enumerate(records):
                for col, column_name in enumerate(headers):
                    value = vars(record)[column_name]
                    fieldValue = QTableWidgetItem(str(value))
                    tabwidget.setItem(row, col, fieldValue)
        else:
            print('Empty data')

    def savefile(self):
            filename = QFileDialog.getSaveFileName(self.main, 'Save File', '', '.xls(*.xls)')
            self.wbk = xlwt.Workbook(encoding="utf-8")
            self.sheet = self.wbk.add_sheet('sheet1', cell_overwrite_ok=True)
            self.writeTosheet(self.sheet)

            self.wbk.save(filename[0])


    def writeTosheet(self, sheet):

        print(self.main.tableWidget_Stock_report.horizontalHeader())
        for currentColumn in range(0, self.main.tableWidget_Stock_report.columnCount()):
            for h in self.headers:
                try:
                    teext = h
                    sheet.write(0, currentColumn, teext)
                except AttributeError:
                    pass
        for currentColumn in range(0, self.main.tableWidget_Stock_report.columnCount()):
            for currentRow in range(1, self.main.tableWidget_Stock_report.rowCount()+1):
                try:
                    teext = self.main.tableWidget_Stock_report.item(currentRow-1, currentColumn).text()
                    sheet.write(currentRow, currentColumn, teext)

                except AttributeError:
                    pass
