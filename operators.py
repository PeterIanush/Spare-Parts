from models import DB_Operators, View_Employees
from PyQt5.QtWidgets import QTableWidgetItem
class OperatorsHandlers:
    def __init__(self, main):

        self.main = main
        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_operators)
        self.main.pushButton_Operators_Back.clicked.connect(self.backButton)
        self.main.lineEdit_operators_Name.returnPressed.connect(self.searchOperators)
        self.accept_reject()
        self.comboBoxTeam()


    def accept_reject(self):

        self.main.buttonBox_Operators.accepted.connect(self.accept)
        self.main.buttonBox_Operators.rejected.connect(self.clearUIdata)

    def accept(self):

        self.bindAllHandlers()

        if len(self.tab_number) == 0:
            self.main.label_operators_Tab_Number.setStyleSheet("QLabel{ background-color : red; color : white; }")
            self.main.label_operators_Tab_Number.setText('Could You please enter curent data')
        else:

            self.writeToDB()
            self.clearUIdata()


    def clearUIdata(self):

        self.main.lineEdit_operators_Name.clear()
        self.main.lineEdit_operators_Tab_Number.clear()

    def bindAllHandlers(self):

        self.name = self.main.label_operators_Name.text()
        self.number_card = self.main.lineEdit_operators_Name.text()
        self.tab_number = self.main.lineEdit_operators_Tab_Number.text()
        self.team = self.main.comboBox_Operators_Team.currentText()

    def backButton(self):

        self.clearUIdata()
        self.main.stackedWidget_SP.setCurrentWidget(self.main.pageMain)

    def writeToDB(self):

        try:
            operators = DB_Operators(name=self.name, number_card=self.number_card, tab_number=self.tab_number, \
                                     team=self.team)

            self.main.session.add(operators)
            self.main.session.commit()

        except:
            print("Can't write to DB")

    def comboBoxTeam(self):

        text_data = self.main.sessionStN.query(View_Employees.department).all()
        self.main.comboBox_Operators_Team.insertItems(0, [value for value, in text_data])

    def searchOperators(self):

        search = self.main.lineEdit_operators_Name.text()

        employee = self.main.sessionStN.query(View_Employees).filter(View_Employees.secureKey == search).first()
        if employee is None:
            print('Please enter current key')
            self.clearUIdata()
        else:
            self.main.label_operators_Name.setText(employee.surname + ' ' + employee.name)
            self.main.lineEdit_operators_Tab_Number.setText(employee.tabNumber)

        self.searchTeam()

    def searchTeam(self):

        headers = ['id', 'name', 'number_card', 'tab_number', 'team', 'date']
        number_card = self.main.lineEdit_operators_Name.text()
        viewsearch = self.main.session.query(DB_Operators).all()

        self.main.tableWidget_Operators.clear()
        self.main.tableWidget_Operators.setHorizontalHeaderLabels(headers)
        numrows = len(viewsearch)
        if numrows > 0:
            numcolums = len(headers)
            tabwidget = self.main.tableWidget_Operators
            tabwidget.setRowCount(numrows)
            tabwidget.setColumnCount(numcolums)
            tabwidget.setHorizontalHeaderLabels(headers)
            for row, record in enumerate(viewsearch):
                for col, column_name in enumerate(headers):
                    value = vars(record)[column_name]
                    item = QTableWidgetItem(str(value))
                    tabwidget.setItem(row, col, item)