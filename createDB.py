from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, TIMESTAMP, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """table users"""
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    login = Column(String(20), nullable=False)
    password = Column(String(50), nullable=False)
    createdAt = Column('created_at', DateTime(timezone=False), default=func.now())
    permissionGroup = Column('group', String(20), nullable=False)
    def __str__(self):
        return 'User(id=' + str(self.id) + ', login=' + self.login + ', password=' + self.password + \
               ', group=' + self.permissionGroup + ')'


class Create_DB_Sp_Incoming(Base):
    """class create incoming table for Spare Parts project"""

    __tablename__ = 'SPIncoming'
    id = Column(Integer, primary_key=True)
    spn = Column(String(20), nullable=False)
    dpn = Column(String(50), nullable=False)
    invoice_number = Column(String(50), nullable=False)
    qty = Column(String(50), nullable=False)
    price = Column(String(50), nullable=False)
    store = Column(String(20), nullable=False)
    description = Column(String(100), nullable=False)
    date_order = Column(DateTime(timezone=False), default=func.now())
    date_incoming = Column(DateTime(timezone=False), default=func.now())
    type_sp = Column(String(20), nullable=False)
    def __str__(self):
        return 'Create_DB_Sp_Incoming(id=' + str(self.id) + ', spn=' + self.spn + \
               ', dpn=' + self.dpn + ', invoice_number=' + self.invoice_number + \
               ', qty=' + self.qty + ', price=' + self.price + ', qty=' + self.qty + \
               ', store=' + self.store + ', description=' + self.description + ', date_order=' + self.date_order + \
               ', date_incoming=' + self.date_incoming + ', type_sp=' + self.type_sp +')'

class Create_DB_Parts(Base):
    """class create parts table for Spare Parts project"""

    __tablename__ = 'SPParts'
    id = Column(Integer, primary_key=True)
    dpn = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    sap_number = Column(String(50), nullable=False)
    project = Column(String(50), nullable=False)
    mqb_number = Column(String(10), nullable=False)
    max_termin = Column(Integer, nullable=False)
    min_termin = Column(Integer, nullable=False)
    def __str__(self):
        return 'Create_DB_Parts(id=' + str(self.id) + ', dpn=' + self.dpn + \
               ', description=' + self.description + ', sap_number=' + self.sap_number + \
               ', project=' + self.project + ', mqb_number=' + self.mqb_number + ', max_termin=' + self.max_termin + \
               ', min_termin=' + self.min_termin +')'

class Create_DB_Equipment(Base):
    """class create equipment table for Spare Parts project"""

    __tablename__ = 'SPEquipment'
    id = Column(Integer, primary_key=True)
    eqp_description = Column(String(50), nullable=False)
    serial_number = Column(String(50), nullable=False)
    qs_number = Column(String(50), nullable=False)
    mqb_number = Column(String(10), nullable=False)
    date = Column(DateTime(timezone=False), default=func.now())
    def __str__(self):
        return 'Create_DB_Equipment(id=' + str(self.id) + ', eqp_description=' + self.eqp_description + \
               ', serial_number=' + self.serial_number + ', qs_number=' + self.qs_number + \
               ', mqb_number=' + self.mqb_number + ', date' + self.date +')'

class Create_DB_Maintenance(Base):
    """class create maintenance table for Spare Parts project"""

    __tablename__ = 'SPMaintenance'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    number_card = Column(String(100), nullable=False)
    tab_number = Column(String(10), nullable=False)
    area = Column(String(20), nullable=False)
    date = Column(DateTime(timezone=False), default=func.now())
    def __str__(self):
        return 'Create_DB_Maintenance(id=' + str(self.id) + ', name=' + self.name + \
               ', number_card=' + self.number_card + ', tab_number=' + self.tab_number + \
               ', area=' + self.area +')'

class Create_DB_Operators(Base):
    """class create operators table for Spare Parts project"""

    __tablename__ = 'SPOperators'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    number_card = Column(String(100), nullable=False)
    tab_number = Column(String(10), nullable=False)
    team = Column(String(20), nullable=False)
    date = Column(DateTime(timezone=False), default=func.now())
    def __str__(self):
        return 'Create_DB_Operators(id=' + str(self.id) + ', name=' + self.name + \
               ', number_card=' + self.number_card + ', tab_number=' + self.tab_number + \
               ', team=' + self.team + ')'

class Create_DB_Outgoing(Base):
    """class create outgoing table for Spare Parts"""

    __tablename__ = 'SPOutgoing'
    id = Column(Integer, primary_key=True)
    dpn = Column(String(50), nullable=False)
    equipment = Column(String(50), nullable=False)
    number_card = Column(String(100), nullable=False)
    maintenance_name = Column(String(50), nullable=False)
    reason = Column(String(100), nullable=False)
    qty = Column(Integer, nullable=False)
    mqb_number = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=False), default=func.now())
    def __str__(self):
        return 'Create_DB_Outgoing(id=' + str(self.id) + ', dpn=' + self.dpn + \
               ', equipment=' + self.equipment + ', number_card=' + self.number_card + \
               ', maintenance_name=' + self.maintenance_name + ', reason=' + self.reason + ', qty=' + self.qty + \
               ', mqb_number=' + self.mqb_number + ', date=' + self.date + ')'

class Create_DB_Crimping_Die(Base):
    """class create crimping die table for Spare Parts"""

    __tablename__ = 'SPCrimpingDie'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=False), default=func.now())
    crimping_tool = Column(String(50), nullable=False)
    equipment = Column(String(50), nullable=False)
    employee = Column(String(50), nullable=False)
    def __str__(self):
        return 'Create_DB_Crimping_Die(id=' + str(self.id) + ', date=' + self.date + \
               ', crimping_tool=' + self.crimping_tool + ', equipment=' + self.equipment + ', employee=' + self.employee + ')'

class Create_DB_Sp_History_Movement(Base):
    """class create incoming table for Spare Parts project"""

    __tablename__ = 'SPHistoryMovement'
    id = Column(Integer, primary_key=True)
    id_incoming = Column(String(50), nullable=False)
    dpn = Column(String(50), nullable=False)
    qty = Column(String(50), nullable=False)
    responsible = Column(String(50), nullable=False)
    movement = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    def __str__(self):
        return 'Create_DB_Sp_History_Movement(id=' + str(self.id) + ', id_incoming=' + self.id_incoming + \
               ', dpn=' + self.dpn + ', qty=' + self.qty + ', description=' + self.description + \
               ', responsible=' + self.responsible + ', movement=' + self.movement + ')'


class Create_DB_History_Crimping_Die(Base):
    """class create history crimping die table for Spare Parts"""

    __tablename__ = 'SPHistoryCrimpingDie'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=False), default=func.now())
    crimping_tool = Column(String(50), nullable=False)
    equipment = Column(String(50), nullable=False)
    employee = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    def __str__(self):
        return'Create_DB_History_Crimping_Die(id=' + str(self.id) + ', date=' + self.date + \
                ', crimping_tool=' + self.crimping_tool + ', equipment=' + self.equipment + \
                ', employee=' + self.employee + ', description=' + self.description + ')'

class Create_DB_Crimping_Maintenance(Base):
    """'class create crimping maintanancce table for Spare Parts"""

    __tablename__ = 'SPCrimpingMaintenance'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=False), default=func.now())
    crimping_tool = Column(String(50), nullable=False)
    maintenance = Column(String(50), nullable=False)
    def __str__(self):
        return'Create_DB_Crimping_Maintenance(id=' + str(self.id) + ', date=' + self.date + \
                ', crimping_tool=' + self.crimping_tool + ', maintenance=' + self.maintenance + ')'


class Create_DB_History_Crimping_Maintenance(Base):
    """'class create history crimping maintanancce table for Spare Parts"""

    __tablename__ = 'SPHistoryCrimpingMaintenance'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=False), default=func.now())
    crimping_tool = Column(String(50), nullable=False)
    maintenance = Column(String(50), nullable=False)
    state = Column(String(100), nullable=False)
    def __str__(self):
        return'Create_DB_History_Crimping_Maintenance(id=' + str(self.id) + ', date=' + self.date + \
                ', crimping_tool=' + self.crimping_tool + ', maintenance=' + self.maintenance + \
                ', state=' + self.state + ')'

class Create_DB_Crimping_Terminal(Base):
    """class create history crimping terminal table for Spare Parts"""

    __tablename__ = 'SPCrimpingTerminal'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=False), default=func.now())
    crimping_tool = Column(String(50), nullable=False)
    equipment = Column(String(50), nullable=False)
    employee = Column(String(50), nullable=False)
    def __str__(self):
        return'Create_DB_History_Crimping_Maintenance(id=' + str(self.id) + ', date=' + self.date + \
                ', crimping_tool=' + self.crimping_tool + ', maintenance=' + self.maintenance + \
                ', state=' + self.state + ')'


class Create_DB_History_Crimping_Terminal(Base):
    """class create history crimping terminal table for Spare Parts"""

    __tablename__ = 'SPHistoryCrimpingTerminal'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=False), default=func.now())
    crimping_tool = Column(String(50), nullable=False)
    equipment = Column(String(50), nullable=False)
    employee = Column(String(50), nullable=False)

class Create_DB_Project(Base):
    """class create project table for Spare Parts"""

    __tablename__ = 'SPProjects'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=False), default=func.now())
    project = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)

class Create_DB_Area(Base):
    """class create project table for Spare Parts"""

    __tablename__ = 'SPArea'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=False), default=func.now())
    area = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)

class Create_DB_Reason(Base):
    """class create reason table for Spare Parts"""

    __tablename__ = 'SPReason'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=False), default=func.now())
    reason = Column(String(100), nullable=False)
    description = Column(String(50), nullable=True)






engine = create_engine("mssql+pyodbc://sa:Prettl!@#4@kanban")

Base.metadata.create_all(engine)