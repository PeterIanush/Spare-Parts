from PyQt5.QtWidgets import QTableWidgetItem
from models import DB_Parts, DB_Sp_Incoming, DB_Project

class PartsHandlers:
    def __init__(self, main):
        self.main = main
        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_Parts)
        self.main.pushButton_Parts_Back.clicked.connect(self.backButtton)
        self.main.lineEdit_Parts_DPN.returnPressed.connect(self.searchParts)
        self.accept_reject()
        self.comboBoxProject()

    def accept_reject(self):

        self.main.buttonBox_Parts.accepted.connect(self.accept)
        self.main.buttonBox_Parts.rejected.connect(self.clearUIdata)

    def accept(self):

        self.bindAllHandless()
        self.writeToDB()
        self.clearUIdata()
        self.comboBoxProject()

    def clearUIdata(self):

        self.main.lineEdit_Parts_DPN.clear()
        self.main.lineEdit_SAP_NUMBER.clear()
        self.main.comboBox_Parts_Project.clear()

    def bindAllHandless(self):

        self.search_dpn = ''
        self.search_description = ''
        self.mqb_number = ''
        if self.main.radioButton_Parts_DPN.isChecked() == True:
            self.search_dpn = self.main.lineEdit_Parts_DPN.text()
            self.search_description = ''
        else:
            self.search_description = self.main.lineEdit_Parts_DPN.text()
            self.search_dpn = self.main.tableWidget_Parts.currentItem().text()
        self.sap_number = self.main.lineEdit_SAP_NUMBER.text()
        self.project = self.main.comboBox_Parts_Project.currentText()

        if self.main.radioButton_Parts_MQB1.isChecked() == True:
            self.mqb_number = 'MQB1'
        else:
            self.mqb_number = 'MQB2'

        self.maxtermin = 0
        self.mintermin = 0

    def backButtton(self):

        self.clearUIdata()
        self.main.stackedWidget_SP.setCurrentWidget(self.main.pageMain)

    def writeToDB(self):

        try:
            parts = DB_Parts(dpn=self.search_dpn, sap_number=self.sap_number, project=self.project, \
                             mqb_number=self.mqb_number, max_termin=self.maxtermin, min_termin=self.mintermin, \
                             description=self.search_description)
            self.main.session.add(parts)
            self.main.session.commit()

        except:
            print("Can't write DB")

    def searchParts(self):
        self.headers = ['id', 'spn', 'dpn', 'invoice_number', 'qty', 'price', 'qty', \
                        'store', 'description', 'date_order', 'date_incoming', 'type_sp']
        search = self.main.lineEdit_Parts_DPN.text()

        if self.main.radioButton_Parts_DPN.isChecked() == True:
            viewsearch = self.main.session.query(DB_Sp_Incoming).filter(DB_Sp_Incoming.dpn == search).all()

        else:
            viewsearch = self.main.session.query(DB_Sp_Incoming).filter(DB_Sp_Incoming.description == search).all()

        self.main.tableWidget_Parts.clear()
        self.main.tableWidget_Parts.setHorizontalHeaderLabels(self.headers)
        numrows = len(viewsearch)
        if numrows > 0:
            numcolums = len(self.headers)
            tabwidget = self.main.tableWidget_Parts
            tabwidget.setRowCount(numrows)
            tabwidget.setColumnCount(numcolums)
            tabwidget.setHorizontalHeaderLabels(self.headers)
            for row, record in enumerate(viewsearch):
                for col, column_name in enumerate(self.headers):
                    value = vars(record)[column_name]
                    item = QTableWidgetItem(str(value))
                    tabwidget.setItem(row, col, item)

    def comboBoxProject(self):

        text_project = self.main.session.query(DB_Project.project).all()

        self.main.comboBox_Parts_Project.insertItems(0, [value for value, in text_project])


