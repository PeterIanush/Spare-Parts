import datetime
from utils import toDateTime as convert
from models import DB_Sp_Incoming, DB_Sp_History_Movement
from utils import toDate as dateconvert

class IncomingHandlers:
    def __init__(self, main):
        self.main = main
        self.main.dateTimeEdit_Date_Order.setDateTime(datetime.datetime.now())
        self.main.dateEdit_Date_Incoming.setDateTime(datetime.datetime.now())
        self.accept_reject()
        self.main.pushButton_Incoming_Back.clicked.connect(self.backButton)
        self.main.stackedWidget_SP.setCurrentWidget(self.main.page_Incoming)


    def accept_reject(self):

        self.main.buttonBox_Incoming.accepted.connect(self.accept)
        self.main.buttonBox_Incoming.rejected.connect(self.reject)

    def accept(self):
        print('accept')
        self.bindAllHandlers()
        self.writeDataToDB()



    def reject(self):
        print('reject')
        self.main.lineEdit_Incoming_SPN.clear()
        self.main.lineEdit_DPN.clear()
        self.main.lineEdit_Invoice_Number.clear()
        self.main.lineEdit_QTY.clear()
        self.main.lineEdit_Description.clear()
        self.main.lineEdit_Store_place.clear()
        self.main.lineEdit_Price.clear()
        self.main.dateTimeEdit_Date_Order.clear()
        self.main.dateEdit_Date_Incoming.clear()

    def bindAllHandlers(self):
        self.list = []
        self.spn = self.main.lineEdit_Incoming_SPN.text()
        self.dpn = self.main.lineEdit_DPN.text()
        self.invoice_number = self.main.lineEdit_Invoice_Number.text()
        self.qty = self.main.lineEdit_QTY.text()
        self.description = self.main.lineEdit_Description.text()
        self.store_place = self.main.lineEdit_Store_place.text()
        self.price = self.main.lineEdit_Price.text()
        self.date_incoming = self.main.dateEdit_Date_Incoming
        self.date_order = self.main.dateTimeEdit_Date_Order
        self.login = self.main.lineEditLogin.text()
        self.movement = 'Incoming'
        self.type_detail = ''
        if self.main.radioButton_Incoming_SP.isChecked() == True:
            self.type_detail = 'spare_parts'
        else:
            self.type_detail = 'wearing_parts'
        self.list.append((self.spn, self.dpn, self.invoice_number, \
                          self.qty, self.description, self.store_place, \
                          self.price, self.date_order, self.date_incoming, self.type_detail))

    def backButton(self):
        self.reject()
        self.main.stackedWidget_SP.setCurrentWidget(self.main.pageMain)


    def writeDataToDB(self):

        try:
            incomingData = DB_Sp_Incoming(spn=self.spn, dpn=self.dpn, invoice_number=self.invoice_number, \
                                          qty=self.qty, description=self.description, store= self.store_place, \
                                          price=self.price, date_order=convert(self.date_order), \
                                          date_incoming=dateconvert(self.date_incoming), \
                                          type_sp=self.type_detail)


            self.main.session.add(incomingData)
            self.main.session.commit()

            incomingHistoryData = DB_Sp_History_Movement(id_incoming=str(incomingData.id), dpn=self.dpn, qty=self.qty, \
                                                         description=self.description, movement=self.movement, \
                                                         responsible=self.login)
            self.main.session.add(incomingHistoryData)
            self.main.session.commit()
            self.reject()
        except:
            print("Can't write to DB")

