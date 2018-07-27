from models import View_Employees, DB_History_Crimping_Terminal, DB_Crimping_Terminal, DB_Equipment
from datetime import datetime


class CrimpingTerminalHandlers:
    def __init__(self, main):

        self.main = main
        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_Crimping_Terminal)
        self.main.pushButton_Crimping_Terminal_Back.clicked.connect(self.backButton)
        self.main.dateEdit_Crimping_Terminal.setDateTime(datetime.now())
        self.main.lineEdit_Crimping_Terminal_Employee.returnPressed.connect(self.searchEmployee)
        self.accept_reject()
        self.comboBoxEmployee()

    def accept_reject(self):

        self.main.buttonBox_Crimping_Terminal.accepted.connect(self.accept)
        self.main.buttonBox_Crimping_Terminal.rejected.connect(self.reject)

    def accept(self):

        self.bindAllHandless()
        if len(self.crimping_tool) == 0:
            self.main.label_Crimping_Terminal_Crimping_Tool.setStyleSheet("QLabel{ background-color : red; color : white; }")
            print('Could You please enter curent data')
        else:

            if self.main.radioButton_Crimping_Terminal_Incoming.isChecked() == True:
                self.writeToDB()
            else:
                self.writeHistoryToDB()
            self.clearUIdata()

    def reject(self):

        self.clearUIdata()
        self.main.close()

    def clearUIdata(self):

        self.main.lineEdit_Crimping_Terminal_Crimping_Tool.clear()
        self.main.lineEdit_Crimping_Terminal_Employee.clear()

    def bindAllHandless(self):

        self.crimping_tool = self.main.lineEdit_Crimping_Terminal_Crimping_Tool.text()
        self.employee = self.main.lineEdit_Crimping_Terminal_Employee.text()
        self.equipment = self.main.comboBox_Crimping_Terminal_Equipment.currentText()
        self.movement = ''
        if self.main.radioButton_Crimping_Terminal_Incoming.isChecked == True:
            self.movement = 'Incoming'
        else:
            self.movement = 'Outgoing'


    def backButton(self):

        self.clearUIdata()
        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_Crimping_Select)

    def writeToDB(self):

        try:
            crimping_terminal = DB_Crimping_Terminal(crimping_tool=self.crimping_tool, equipment=self.equipment, employee=self.employee)

            self.main.session.add(crimping_terminal)
            self.main.session.commit()
        except:
            print("Can't write to DB")

    def writeHistoryToDB(self):

        try:
            crimping_history = DB_History_Crimping_Terminal(crimping_tool=self.crimping_tool, equipment=self.equipment, \
                                                       employee=self.employee)
            self.main.session.add(crimping_history)
            self.main.session.commit()
        except:
            print("Can't write to DB")

    def comboBoxEmployee(self):

        text_equipment = self.main.session.query(DB_Equipment.eqp_description).all()

        self.main.comboBox_Crimping_Terminal_Equipment.insertItems(0, [value for value, in text_equipment])

    def searchEmployee(self):

        search = self.main.lineEdit_Crimping_Terminal_Employee.text()

        employee = self.main.sessionStN.query(View_Employees).filter(View_Employees.secureKey == search).first()
        if employee is None:
            print('Please enter current key')
            self.clearUIdata()
        else:
            self.main.label_Crimping_Terminal_Employee.setText(employee.surname + ' ' + employee.name)
