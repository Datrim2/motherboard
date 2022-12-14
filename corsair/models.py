from sqlalchemy import String, Integer, Column, LargeBinary, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MotherBoard(Base):
    __tablename__ = "MotherBoard"
    mb_id = Column('id', Integer(), primary_key=True, autoincrement=True)
    id_web = Column('id_web', Integer(), nullable=False)
    title = Column('Title', String(200), nullable=False)
    subname = Column('Subname', String(200))
    link = Column('Link', String(400), nullable=False)
    description = Column('Desc', String(2000), nullable=False)
    ean = Column('Ean', String(200), nullable=False)
    release = Column('Release', DateTime(), nullable=False)
    product = Column('Product_line', String(200), nullable=False)
    picture = Column('Picture', LargeBinary, nullable=False)
    color = Column('Color', String(200))
    label = Column('Label', String(200))

class Memory(Base):
    __tablename__ = "RAM"
    ram_id = Column('id', Integer(), primary_key=True, autoincrement=True)
    motherboard_id = Column('motherboard_id', ForeignKey("MotherBoard.id"))
    specifications_id = Column('specifications_id', ForeignKey("Specifications.id"))
    type_memory = Column('type_memory', String(200), nullable=False)
    vendor = Column('Vendor', String(200), nullable=False)
    model = Column('Model', String(200),  nullable=False)
    ddr = Column('DDR', String(200), nullable=False)
    spd = Column('SPD Speed', String(200), nullable=False)
    support = Column('Supported Speed', String(200), nullable=False)
    chipset = Column('Chipset', String(200), nullable=False)
    voltage = Column('Voltage', String(200), nullable=False)
    sided = Column('Sided', String(200), nullable=False)
    size = Column('Size', String(200), nullable=False)
    dimm = Column('1|2|4 DIMM', String(200), nullable=False)
    
class Specifications(Base):
    __tablename__ = "Specifications"
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    model = Column('Model', String(200), nullable=False)
    cl = Column('CL', String(200), nullable=False)
    tRCmin = Column('tRCmin', String(20), nullable=False)
    tRFCmin = Column('tRFCmin', String(20), nullable=False)
    tRASmin = Column('tRASmin', String(200), nullable=False)
    MaxOper = Column('Maximum Operating', String(20))
    ul = Column('UL', String(200), nullable=False)
    otemperature = Column('Operating Temperature', String(200), nullable=False)
    stemperature = Column('Storage Temperature', String(200), nullable=False)
    desc = Column('Description', String(2000), nullable=False)
    features_id = Column('features_id', ForeignKey("Features.id"))
    timing_id = Column('timing_id', ForeignKey("Timing.id"))
    dop = Column('DOP', String(200))
    picture = Column('Picture', LargeBinary, nullable=False)

class Features(Base):
    __tablename__ = 'Features'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    f1 = Column('F#1', String(200), nullable=False)
    f2 = Column('F#2', String(200), nullable=False)
    f3 = Column('F#3', String(200), nullable=False)
    f4 = Column('F#4', String(200), nullable=False)
    f5 = Column('F#5', String(200), nullable=False)
    f6 = Column('F#6', String(200), nullable=False)
    f7 = Column('F#7', String(200), nullable=False)
    f8 = Column('F#8', String(200), nullable=False)
    f9 = Column('F#9', String(200), nullable=False)
    f10 = Column('F#19', String(200), nullable=False)
    f11 = Column('F#10', String(200), nullable=False)
    f12 = Column('F#11', String(200), nullable=False)
    f13 = Column('F#12', String(200), nullable=False)
    f14 = Column('F#13', String(200), nullable=False)
    f15 = Column('F#14', String(200), nullable=False)
    f16 = Column('F#15', String(200), nullable=False)
    f17 = Column('F#16', String(200), nullable=False)
    f18 = Column('F#17', String(200), nullable=False)
    f19 = Column('F#18', String(200), nullable=False)
    f20 = Column('F#20', String(200), nullable=False)

class Timing(Base):
    __tablename__ = 'Timing'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    default = Column('Default', String(200), nullable=False)
    xmp1 = Column('XMP1', String(200), nullable=False)
    xmp2 = Column('XMP2', String(200), nullable=False)
    xmp3 = Column('XMP3', String(200), nullable=False)
    expo1 = Column('EXPO1', String(200), nullable=False)
    expo2 = Column('EXPO2', String(200), nullable=False)
    dname = Column('Default_name', String(200), nullable=False)

class Specifications_corsair(Base):
    __tablename__ = 'Specifications_corsair'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    code = Column('code', String(200), nullable=False)
    name = Column('name', String(200), nullable=False)
    desc = Column('description', String(200))
    fan = Column('Fan Included', String(200))
    memSeries = Column('Memory Series', String(200))
    memType = Column('Memory Type', String(200))
    memColor = Column('Memory Color', String(200))
    spdLat = Column('SPD Latency', String(200))
    spdSpeed = Column('SPD Speed', String(200))
    spdVolt = Column('SPD Voltage', String(200))
    spdRat = Column('Speed Rating', String(200))
    compatibility = Column('Compatibility', String(200))
    memSize = Column('Memory Size', String(200))
    testLat = Column('Tested Latency', String(200))
    testVolt = Column('Tested Voltage', String(200))
    testSpeed = Column('Tested Speed', String(200))
    heatSpread = Column('Heat Spreader', String(200))
    packMemFormat = Column('Package Memory Format', String(200))
    profile = Column('Performance Profile', String(200))
    packMemPin = Column('Package Memory Pin', String(200))
    memPackCont = Column('Memory Package contents', String(200))
    memComp = Column('Memory Compatibility', String(200))

class Images(Base):
    __tablename__ = 'Images'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    spec_id = Column('spec_corsair_id', ForeignKey("Specifications_corsair.id"))
    type = Column('type', String(50))
    desc = Column('desc', String(2000))
    image = Column('image', LargeBinary)
    
class CorsairAll(Base):
    __tablename__ = 'corsair'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    code = Column('code', String(200), nullable=False)
    name = Column('name', String(200))
    url = Column('url', String(2000))
    status = Column('status', Integer())