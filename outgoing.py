from models import DB_Outgoing, View_Employees, DB_Reason, DB_Equipment, DB_Sp_Incoming
from PyQt5.QtWidgets import QTableWidgetItem
import datetime



class OutgoingHandlers:
    def __init__(self, main):

        self.main = main
        self.main.label_Outgoing_Date.setText(str(datetime.datetime.now()))
        self.main.pushButton_Outgoing_Back.clicked.connect(self.backButton)
        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_Outgoing)
        self.main.lineEdit_Outgoing_Scan_Key.returnPressed.connect(self.searchMaintenance)
        self.main.lineEdit_Outgoing_DPN.returnPressed.connect(self.searchDPN)
        self.accept_reject()
        self.comboBoxEquipment()
        self.comboBoxReason()

    def accept_reject(self):

        self.main.buttonBox_Outgoing.accepted.connect(self.accept)
        self.main.buttonBox_Outgoing.rejected.connect(self.clearUIdata)

    def accept(self):

        self.bindAllHandlers()
        self.validateQty()


    def clearUIdata(self):

        self.main.lineEdit_Outgoing_DPN.clear()
        self.main.label_Outgoing_maintenance.clear()
        self.main.lineEdit_Outgoing_QTY.clear()
        self.main.lineEdit_Outgoing_Scan_Key.clear()

    def bindAllHandlers(self):

        self.dpn = self.main.lineEdit_Outgoing_DPN.text()
        self.equipment = self.main.comboBox_Outgoing_Equipment.currentText()
        self.employee = self.main.label_Outgoing_maintenance.text()
        self.reason = self.main.comboBox_Outgoing_Reason.currentText()
        self.qty = self.main.lineEdit_Outgoing_QTY.text()
        self.secure_key = self.main.lineEdit_Outgoing_Scan_Key.text()
        self.login = self.main.lineEditLogin.text()
        self.movement = 'Outgoing'
        self.mqb = ''
        if self.main.radioButton_Outgoing_MQB1.isChecked() == True:
            self.mqb = 1
        else:
            self.mqb = 2

    def backButton(self):

        self.clearUIdata()
        self.main.stackedWidget_SP.setCurrentWidget(self.main.pageMain)


    def writeDataToDB(self):

        try:
            outgoingData = DB_Outgoing(dpn=self.dpn, equipment=self.equipment, number_card=self.secure_key, \
                                       maintenance_name=self.employee, reason=self.reason, qty=self.qty, \
                                       mqb_number=self.mqb)
            self.main.session.add(outgoingData)
            self.main.session.commit()

        except:
            print("Can't write to DB")



    def joinDataToDB(self):

        try:

            self.main.session.query(DB_Sp_Incoming).filter(DB_Sp_Incoming.dpn == self.dpn). \
                delete(synchronize_session='evaluate')

        except:
            print("Can't delete from DB")

    def searchDPN(self):

        headers = ['spn', 'dpn', 'invoice_number', 'qty', 'price', 'store', 'description',\
                   'date_order', 'date_incoming', 'type_sp']

        search = self.main.lineEdit_Outgoing_DPN.text()

        self.main.tableView_Outgoing.clear()
        self.main.tableView_Outgoing.setHorizontalHeaderLabels(headers)
        record = self.main.session.query(DB_Sp_Incoming).filter(DB_Sp_Incoming.dpn == search).first()

        if record != None:
            numcolums = len(headers)
            tabwidget = self.main.tableView_Outgoing

            tabwidget.setColumnCount(numcolums)
            tabwidget.setHorizontalHeaderLabels(headers)
            tabwidget.setRowCount(1)
            #for row, record in enumerate(record):
            for col, column_name in enumerate(headers):
                value = vars(record)[column_name]
                fieldValue = QTableWidgetItem(str(value))
                tabwidget.setItem(0, col, fieldValue)
        else:
            print('Empty data')
    def validateQty(self):

        search = self.main.lineEdit_Outgoing_DPN.text()
        dpnQty = int(self.main.lineEdit_Outgoing_QTY.text())
        record = self.main.session.query(DB_Sp_Incoming).filter(DB_Sp_Incoming.dpn == search).first()
        valueDpn = int(vars(record)['qty'])
        if dpnQty <= valueDpn:
            print("Correct data")
            self.writeDataToDB()
            self.updateOutgoing()
            self.clearUIdata()
        else:
            print("You stuped developer")
            self.main.label_Outgoing_QTY.setStyleSheet("QLabel{ background-color : red; color : white; }")
            self.main.label_Outgoing_QTY.setText('Available quantity exceeded')

    def searchMaintenance(self):

        search = self.main.lineEdit_Outgoing_Scan_Key.text()

        employee = self.main.sessionStN.query(View_Employees).filter(View_Employees.secureKey == search).first()
        if employee is None:
            print('Please enter current key')
            self.clearUIdata()
        else:
            self.main.label_Outgoing_maintenance.setText(employee.surname + ' ' + employee.name)

    def updateOutgoing(self):

        search = self.main.lineEdit_Outgoing_DPN.text()
        qty = self.main.lineEdit_Outgoing_QTY.text()
        self.record = self.main.session.query(DB_Sp_Incoming).filter(DB_Sp_Incoming.dpn == search).first()
        self.new_qty = int(vars(self.record)['qty']) - int(qty)
        self.record.qty=str(self.new_qty)
        try:

            self.main.session.add(self.record)
            self.main.session.commit()

        except:
            print("Can't write to DB")




    def comboBoxReason(self):

        text_reason = self.main.session.query(DB_Reason.reason).all()

        self.main.comboBox_Outgoing_Reason.insertItems(0, [value for value, in text_reason])

    def comboBoxEquipment(self):

        text_equipment = self.main.session.query(DB_Equipment.eqp_description).all()

        self.main.comboBox_Outgoing_Equipment.insertItems(0, [value for value, in text_equipment])
