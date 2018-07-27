from models import View_Employees, DB_History_Crimping_Die, DB_Crimping_Die, DB_Equipment
from datetime import datetime


class CrimpingDieHandlers:
    def __init__(self, main):

        self.main = main
        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_Crimping_Die)
        self.main.pushButton_Crimping_Die_Back.clicked.connect(self.backButton)
        self.main.dateEdit_Crimping_Die_Date.setDateTime(datetime.now())
        self.main.lineEdit_Crimping_Die_Employee.returnPressed.connect(self.searchEmployee)
        self.accept_reject()
        self.comboBoxEmployee()

    def accept_reject(self):

        self.main.buttonBox_Crimping_Die.accepted.connect(self.accept)
        self.main.buttonBox_Crimping_Die.rejected.connect(self.reject)

    def accept(self):

        self.bindAllHandless()
        if len(self.crimping_tool) == 0:
            self.main.label_Crimping_Die_Crimping_Tool.setStyleSheet("QLabel{ background-color : red; color : white; }")
            self.main.label_Crimping_Die_Crimping_Tool.setText('Could You please enter curent data')
        else:

            if self.main.radioButton_Crimping_Die__Incomming.isChecked() == True:
                self.writeToDB()
            else:
                self.writeHistoryToDB()
            self.clearUIdata()

    def reject(self):

        self.clearUIdata()
        self.main.close()


    def clearUIdata(self):

        self.main.lineEdit_Crimping_Die_Crimping_Tool.clear()
        self.main.lineEdit_Crimping_Die_Employee.clear()

    def bindAllHandless(self):

        self.crimping_tool = self.main.lineEdit_Crimping_Die_Crimping_Tool.text()
        self.employee = self.main.label_Crimping_Die_Employee.text()
        self.equipment = self.main.comboBox_Crimping_Die_Equipment.currentText()
        self.movement = ''
        if self.main.radioButton_Crimping_Die__Incomming.isChecked == True:
            self.movement = 'Incoming'
        else:
            self.movement = 'Outgoing'


    def backButton(self):

        self.clearUIdata()
        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_Crimping_Select)

    def writeToDB(self):

        try:
            crimping_die = DB_Crimping_Die(crimping_tool=self.crimping_tool, equipment=self.equipment, employee=self.employee)

            self.main.session.add(crimping_die)
            self.main.session.commit()
        except:
            print("Can't write to DB")

    def writeHistoryToDB(self):

        try:
            crimping_history = DB_History_Crimping_Die(crimping_tool=self.crimping_tool, equipment=self.equipment, \
                                                       employee=self.employee, description=self.movement)
            self.main.session.add(crimping_history)
            self.main.session.commit()
        except:
            print("Can't write to DB")

    def comboBoxEmployee(self):

        text_equipment = self.main.session.query(DB_Equipment.eqp_description).all()

        self.main.comboBox_Crimping_Die_Equipment.insertItems(0, [value for value, in text_equipment])

    def searchEmployee(self):

        search = self.main.lineEdit_Crimping_Die_Employee.text()

        employee = self.main.sessionStN.query(View_Employees).filter(View_Employees.secureKey == search).first()
        if employee is None:
            print('Please enter current key')
            self.clearUIdata()
        else:
            self.main.label_Crimping_Die_Employee.setText(employee.surname + ' ' + employee.name)
