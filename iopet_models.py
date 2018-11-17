from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Boolean
from iopet_db import Base

class Chat(Base):
    __tablename__ = 'chat'
    chat_id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('chat_room.room_id'))
    chat_send = Column(Integer)
    chat_type = Column(Integer)
    chat_message = Column(String(1000))
    chat_datetime = Column(DateTime)
    chat_read = Column(Boolean)


class ChatRoom(Base):
    __tablename__ = 'chat_room'
    room_id = Column(Integer, primary_key=True)
    hospital_id = Column(Integer, ForeignKey('hospital.hospital_id'))
    pet_id = Column(Integer, ForeignKey('pet.pet_id'))


class Disease(Base):
    __tablename__ = 'disease'
    disease_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('disease_category.category_id'))
    disease_name = Column(String(100))
    disease_recommend = Column(String(600))
    disease_diag = Column(String(600))
    disease_related = Column(String(600))


class DiseaseCategory(Base):
    __tablename__ = 'disease_category'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(100))


class DiseaseMedicine(Base):
    __tablename__ = 'disease_medicine'
    disease_medicine_id = Column(Integer, primary_key=True)
    disease_id = Column(Integer, ForeignKey('disease.disease_id'))
    medi_id = Column(Integer, ForeignKey('medicine.medi_id'))

class DiseaseSymptom(Base):
    __tablename__ = 'disease_symptom'
    disease_symptom_id = Column(Integer, primary_key=True)
    disease_id = Column(Integer, ForeignKey('disease.disease_id'))
    symptom_name = Column(String(200))

class Hospital(Base):
    __tablename__ = 'hospital'
    hospital_id = Column(Integer, primary_key=True)
    hospital_user_id = Column(String(20))
    hospital_user_pw = Column(String(20))
    hospital_name = Column(String(20))
    hospital_revenue = Column(Integer)

class Medicine(Base):
    __tablename__ = 'medicine'
    medi_id = Column(Integer, primary_key=True)
    medi_name = Column(String(100))
    medi_intro = Column(String(200))
    medi_side = Column(String(200))
    medi_warn = Column(String(200))
    medi_vol = Column(Float)
    medi_period = Column(Integer)
    medi_method = Column(Integer)
    medi_doses = Column(Integer)
    medi_price = Column(Integer)

class Diagnosis(Base):
    __tablename__ = 'diagnosis'
    diagn_id = Column(Integer, primary_key=True)
    diagn_name = Column(String(30))
    diagn_date = Column(DateTime)
    diagn_opinion = Column(String(1000))
    diagn_price = Column(Integer)
    hospital_id = Column(Integer, ForeignKey('hospital.hospital_id'))
    pet_id = Column(Integer, ForeignKey('pet.pet_id'))

class Stock(Base):
    __tablename__ = 'stock'
    stock_id = Column(Integer, primary_key=True)
    stock_name = Column(String(20))
    stock_price = Column(Integer)

class Pet(Base):
    __tablename__ = 'pet'
    pet_id = Column(Integer, primary_key=True)
    pet_name = Column(String(20))
    pet_age = Column(Integer)
    pet_spec = Column(String(20))
    pet_weight = Column(Float)
    pet_sex = Column(Integer)
    pet_adms = Column(Boolean)
    pet_profile = Column(String(600))
    pet_person = Column(String(10))
    pet_contact = Column(Integer)
    # datetime = Column(DateTime)
    hospital_id = Column(String(250),  ForeignKey('hospital.hospital_id'))

    def __init__(self):
        print("created")

    def __repr__(self):
        return "<TbTest('{}', '{}', '{}'>".format(self.pet_id, self.pet_name, self.pet_age)