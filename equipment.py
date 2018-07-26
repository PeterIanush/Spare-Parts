import datetime

from models import DB_Equipment

class EquipmentHandlers:

    def __init__(self, main):
        self.main = main
        self.main.label_EQIUPMENT_Date.setText(str(datetime.datetime.now().date()))
        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_EQIUPMENT)
        self.accept_reject()
        self.main.pushButton_EQUIPMENT_Back.clicked.connect(self.backButton)

    def accept_reject(self):

        self.main.buttonBox_EQIUPMENT.accepted.connect(self.accept)
        self.main.buttonBox_EQIUPMENT.rejected.connect(self.clearUIdata)

    def accept(self):

        self.bindAllHandlers()
        self.writeToDB()

    def clearUIdata(self):

        self.main.lineEdit_EQP_Description.clear()
        self.main.lineEdit_Serial_number.clear()
        self.main.lineEdit_QS_Number.clear()

    def bindAllHandlers(self):

        self.eqpDescription = self.main.lineEdit_EQP_Description.text()
        self.serialnumber = self.main.lineEdit_Serial_number.text()
        self.qsnumber = self.main.lineEdit_QS_Number.text()
        self.plant = ''
        if self.main.radioButton_EQIUPMENT_MQB1.isChecked() == True:
            self.plant = 'MQB1'
        else:
            self.plane = 'MQB2'

    def backButton(self):
        self.clearUIdata()
        self.main.stackedWidget_SP.setCurrentWidget(self.main.pageMain)

    def writeToDB(self):

        try:
            equipmentData = DB_Equipment(eqp_description=self.eqpDescription, serial_number=self.serialnumber,\
                                         qs_number=self.qsnumber, mqb_number=self.plant)
            self.main.session.add(equipmentData)
            self.main.session.commit()

        except:
            print("Can't write to DB")

        self.clearUIdata()