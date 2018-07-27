from models import View_Employees, DB_History_Crimping_Maintenance, DB_Crimping_Maintenance
from datetime import datetime


class CrimpingMaintenanceHandlers:
    def __init__(self, main):

        self.main = main
        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_Crimping_Maintenance)
        self.main.pushButton_Crimping_Maintenance_Back.clicked.connect(self.backButton)
        self.main.dateEdit_Crimping_Maintenance.setDateTime(datetime.now())
        self.main.lineEdit_Crimping_Maintenance_Employee.returnPressed.connect(self.searchEmployee)
        self.accept_reject()


    def accept_reject(self):

        self.main.buttonBox_Crimping_Maintenance.accepted.connect(self.accept)
        self.main.buttonBox_Crimping_Maintenance.rejected.connect(self.reject)

    def accept(self):

        self.bindAllHandless()
        if len(self.crimping_tool) == 0:
            self.main.label_Crimping_Maintenance_Crimping_Tool.setStyleSheet("QLabel{ background-color : red; color : white; }")
            self.main.label_Crimping_Maintenance_Crimping_Tool.setText('Could You please enter curent data')
        else:

            if self.main.radioButton_Crimping_Maintenance_Incomming.isChecked() == True:
                self.writeToDB()
            else:
                self.writeHistoryToDB()
            self.clearUIdata()

    def reject(self):

        self.clearUIdata()
        self.main.close()

    def clearUIdata(self):

        self.main.lineEdit_Crimping_Maintenance_Crimping_Tool.clear()
        self.main.lineEdit_Crimping_Maintenance_Employee.clear()

    def bindAllHandless(self):

        self.crimping_tool = self.main.lineEdit_Crimping_Maintenance_Crimping_Tool.text()
        self.employee = self.main.label_Crimping_Maintenance_Employee.text()

        self.movement = ''
        if self.main.radioButton_Crimping_Maintenance_Incomming.isChecked() == True:
            self.movement = 'Incoming for servise'
        else:
            self.movement = 'Outgoing from service'


    def backButton(self):

        self.clearUIdata()
        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_Crimping_Select)

    def writeToDB(self):

        try:
            crimping_m = DB_Crimping_Maintenance(crimping_tool=self.crimping_tool, maintenance=self.employee)

            self.main.session.add(crimping_m)
            self.main.session.commit()
        except:
            print("Can't write to DB")

    def writeHistoryToDB(self):

        try:
            crimping_history = DB_History_Crimping_Maintenance(crimping_tool=self.crimping_tool, \
                                                               maintenance=self.employee, state=self.movement)
            self.main.session.add(crimping_history)
            self.main.session.commit()
        except:
            print("Can't write to DB")


    def searchEmployee(self):

        search = self.main.lineEdit_Crimping_Maintenance_Employee.text()

        employee = self.main.sessionStN.query(View_Employees).filter(View_Employees.secureKey == search).first()
        if employee is None:
            print('Please enter current key')
            self.clearUIdata()
        else:
            self.main.label_Crimping_Maintenance_Employee.setText(employee.surname + ' ' + employee.name)
