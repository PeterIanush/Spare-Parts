from models import DB_Maintenance, View_Employees, DB_Area
from PyQt5.QtWidgets import QTableWidgetItem
class MaintenanceHandlers:
    def __init__(self, main):
        self.main = main
        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_maintenance)
        self.main.pushButton_Maintenance_Back.clicked.connect(self.backButton)
        self.main.lineEdit_maintenance_Name.returnPressed.connect(self.searchMaintenance)
        self.accept_reject()
        self.comboBoxArea()

    def accept_reject(self):

        self.main.ButtomBox_maintenance.accepted.connect(self.accept)
        self.main.ButtomBox_maintenance.rejected.connect(self.reject)

    def accept(self):

        self.bindAllHandless()

        if len(self.tab_number) == 0:
            self.main.label_maintenance_Tab_Numer.setStyleSheet("QLabel{ background-color : red; color : white; }")
            self.main.label_maintenance_Tab_Numer.setText('Could You please enter curent tabel number')
        else:

            self.writeToDB()
            self.clearUIdata()

    def reject(self):

        self.clearUIdata()
        self.main.close()

    def clearUIdata(self):

        self.main.lineEdit_maintenance_Name.clear()
        self.main.lineEdit_maintenance_Tab_Number.clear()

    def bindAllHandless(self):

        self.name =  self.main.label_maintenance_Name.text()
        self.card_number = self.main.lineEdit_maintenance_Name.text()
        self.tab_number = self.main.lineEdit_maintenance_Tab_Number.text()
        self.area = self.main.comboBox_maintenance_Area.currentText()

    def defualtLayout(self):

        self.main.label_maintenance_Name.clear()

    def backButton(self):

        self.clearUIdata()
        self.main.stackedWidget_SP.setCurrentWidget(self.main.pageMain)

    def writeToDB(self):

        try:
            maintenance = DB_Maintenance(name=self.name, number_card=self.card_number, tab_number=self.tab_number, \
                                         area=self.area)
            self.main.session.add(maintenance)
            self.main.session.commit()

        except:
            print("Can't write to DB")

    def searchMaintenance(self):

        search = self.main.lineEdit_maintenance_Name.text()
        try:

            self.empl = self.main.sessionStN.query(View_Employees).filter(View_Employees.secureKey == search).first()

        except:
            print('Empty data')
            self.empl = ''


        if self.empl == '':
            print('Please enter current key')
            self.clearUIdata()
            self.main.label_maintenance_Name.setStyleSheet("QLabel{ background-color : red; color : white; }")
            self.main.label_maintenance_Name.setText('Could You please enter curent secure card')
        else:
            #TODO: make method for change to default all objects
            self.defualtLayout()
            self.main.label_maintenance_Name.setText(self.empl.surname + ' ' + self.empl.name)
            self.main.lineEdit_maintenance_Tab_Number.setText(self.empl.tabNumber)

        self.searchArea()


    def comboBoxArea(self):

        text_area = self.main.session.query(DB_Area.area).all()

        self.main.comboBox_maintenance_Area.insertItems(0, [value for value, in text_area])

    def searchArea(self):

        headers = ['id', 'name', 'number_card', 'tab_number', 'area', 'date']

        viewsearch = self.main.session.query(DB_Maintenance).all()

        self.main.tableWidget_Maintenance.clear()
        self.main.tableWidget_Maintenance.setHorizontalHeaderLabels(headers)
        numrows = len(viewsearch)
        if numrows > 0:
            numcolums = len(headers)
            tabwidget = self.main.tableWidget_Maintenance
            tabwidget.setRowCount(numrows)
            tabwidget.setColumnCount(numcolums)
            tabwidget.setHorizontalHeaderLabels(headers)
            for row, record in enumerate(viewsearch):
                for col, column_name in enumerate(headers):
                    value = vars(record)[column_name]
                    item = QTableWidgetItem(str(value))
                    tabwidget.setItem(row, col, item)