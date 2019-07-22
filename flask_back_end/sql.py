# import pymysql
# conn = pymysql.connect(
#     host="127.0.0.1",
#     user="root", password="123456",
#     database="sub-health",
#     charset="utf8")


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class To_json():
  def to_json(self):
    dict = self.__dict__
    if "_sa_instance_state" in dict:
        del dict["_sa_instance_state"]
    return dict


class Comp_lang(Base, To_json):
  # 表名称
  __tablename__ = 'comp_lang'
  # news表里id字段
  id = Column(Integer, primary_key=True, autoincrement=True)
  # news表里title字段
  desc = Column(String(length=500), nullable=True)
  core_id = Column(Integer)



class Core(Base, To_json):
    __tablename__ = 'core'
    id = Column(Integer, primary_key=True, autoincrement=True)
    core = Column(String(length=256))
    symptom_id = Column(Integer)

class Symptom(Base, To_json):
    __tablename__ = 'symptom'
    id = Column(Integer, primary_key=True, autoincrement=True)
    symptom = Column(String(length=255), nullable=True)
    advice = Column(String(length=500), nullable=True)
    kind = Column(Integer)
    

class Question(Base, To_json):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String(length=255), nullable=True)
    symptom_id = Column(Integer)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=50), nullable=True)
    password = Column(String(length=50), nullable=True)