from database import Base
from database import db_session

import random
import datetime
from time import sleep


from sqlalchemy import Column, Integer, REAL, Float, String, DateTime
def create_img_table(tablename):
        
    class image_table(Base):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True}
        id = Column(Integer, primary_key = True)
        datetime = Column(DateTime)
        image = Column(String(50))

        def __init__(self, datetime, image):
            self.datetime = datetime
            self.image = image
    return image_table
    
def create_models(tablename):
    #기본 테이블 생성. 테이블마다 이름을 다르게 하여 생성.
    #컬럼 값으로 자동으로 증가하는 id값, 현재 시간, 데이터를 가짐
    class TbTable(Base):
        __tablename__ = tablename
        __table_args__ = {'extend_existing':True}
        id = Column(Integer, primary_key = True)
        datetime = Column(DateTime)
        data = Column(Float)

        def __init__(self, datetime, data):
            self.datetime = datetime
            self.data = data
        
        def __repr__(self):
            return "<TbTest('%d', '%s', '%f'>" %(self.id, str(self.datetime), self.data)
    
    return TbTable

def create_avg_table(tablename):
    #시간별 평균 데이터를 구하기위한 테이블.
    #단위별로(예제로는 3,5,10분 사용함) 평균값을 가짐

    class avg_table(Base):
        __tablename__ = tablename
        __tabe_args__ = {'extend_existing':True}

        id = Column(Integer, primary_key = True)
        unit = Column(String(20))
        avg1 = Column(Float)
        avg2 = Column(Float)
        avg3 = Column(Float)

        def __init__(self, unit, avg1, avg2, avg3):
            self.unit = unit
            self.avg1 = avg1
            self.avg2 = avg2
            self.avg3 = avg3
        
        def __repr__(self):
            return "<avg_table('%d', '%s', '%f, '%f', '%f)>"%(self.id, str(self.unit), self.avg1, self.avg2, self.avg3)
    
    return avg_table

    
def create_symbol_table(tablename):
    class symbol_table(Base):
        __tablename__ = tablename
        __table_args__ = {'extend_existing':True}
        id = Column(Integer, primary_key = True)
        data1 = Column(Integer)
        data2 = Column(Integer)
        data3 = Column(Integer)

        def __init__(self, data1, data2, data3):
            self.data1 = data1
            self.data2 = data2
            self.data3 = data3
        
        def __repr__(self):
            return "<symbol_table('%d')>"%(self.data)
    return symbol_table

def add_entry(table, datetime, data):
    #기본 테이블에 데이터 추가하기. session을 이용하여 데이터를 추가할 수 있음.
    #commit으로 넣은 데이터값을 업데이트 해줘야함
    t = table(datetime, data)
    db_session.add(t)
    db_session.commit()

def add_unit_entry(table):
    #평균테이블에 단위를 넣어주기 위한 함수. 만들고싶은 테이블의 형태는 
    # unit avg1 avg2 avg3
    # 3분
    # 5분
    # 10분
    #이러한 형태이고, unit은 미리 넣어줘야함. 각각 평균값들은 계속해서 업데이트됨.

    queries = db_session.query(table)

    id = 0
    for i in queries :
        id = i.id
    #만약 기존에 생성되어있다면 진행하지 않음.

    if id < 3 and id >=0:
        db_session.add_all([           # u    1 2 3
            table('3minute',0,0,0),    # 3분  0 0 0
            table('5minute',0,0,0),    # 5분  0 0 0
            table('10minute',0,0,0)    # 10분 0 0 0
        ])
        db_session.commit()



def data_generator1(table, second):
    #랜덤 데이터 생성 함수. 그라파나에서 기존의 시간보다 9시간을 추가하므로(utc) 9시간을 빼서 넣어줬음.
    while True:
        r = random.uniform(-1,1)
        current = datetime.datetime.now()
        add_entry(table, current - datetime.timedelta(hours=9),r)


        sleep(second)


def data_generator2(table, second):
    #랜덤 데이터 생성 함수. 그라파나에서 기존의 시간보다 9시간을 추가하므로(utc) 9시간을 빼서 넣어줬음.
    while True:
        r = random.uniform(0,1)
        current = datetime.datetime.now()
        add_entry(table, current - datetime.timedelta(hours=9),r)


        sleep(second)

def data_generator3(table, second):
    #graph3을 표현할 데이터 생성기
    while True:
        r = random.randint(0,4)
        if r == random.randint(0,4) :
            r = random.randint(4,10)

        current = datetime.datetime.now()
        add_entry(table, current - datetime.timedelta(hours=9),r)


        sleep(second)


def input_data(table):

    current = datetime.datetime.now()

    queries = db_session.query(table)
    datalist_3 = []
    datalist_5 = []
    datalist_10 = []

    for q in queries:
        if q.datetime + datetime.timedelta(hours=9)>=current - datetime.timedelta(minutes=3):
                datalist_3.append(q.data)
    for q in queries:
        if q.datetime + datetime.timedelta(hours=9)>=current - datetime.timedelta(minutes=5):
                datalist_5.append(q.data)
    for q in queries:
        if q.datetime + datetime.timedelta(hours=9)>=current - datetime.timedelta(minutes=10):
                datalist_10.append(q.data)
    
    return datalist_3, datalist_5, datalist_10

    
    
def data_update(table1, table2, table3, avgtable, symtable): #3분, 5분, 10분 간격으로 데이터의 평균 구함
    avg1_3, avg1_5, avg1_10 = 0,0,0
    avg2_3, avg2_5, avg2_10 = 0,0,0
    avg3_3, avg3_5, avg3_10 = 0,0,0
    while True:

        datalist1_3, datalist1_5, datalist1_10 = [], [], []
        datalist2_3, datalist2_5, datalist2_10 = [], [], []
        datalist3_3, datalist3_5, datalist3_10 = [], [], []

        datalist1_3, datalist1_5, datalist1_10 = input_data(table1)
        datalist2_3, datalist2_5, datalist2_10 = input_data(table2)
        datalist3_3, datalist3_5, datalist3_10 = input_data(table3)

        if len(datalist1_3) != 0 :
            avg1_3 = sum(datalist1_3)/len(datalist1_3)
        if len(datalist1_5) != 0 :
            avg1_5 = sum(datalist1_5)/len(datalist1_5)
        if len(datalist1_10) != 0 :
            avg1_10 = sum(datalist1_10)/len(datalist1_10)

        if len(datalist2_3) != 0 :
            avg2_3 = sum(datalist2_3)/len(datalist2_3)
        if len(datalist2_5) != 0 :
            avg2_5 = sum(datalist2_5)/len(datalist2_5)
        if len(datalist2_10) != 0 :
            avg2_10 = sum(datalist2_10)/len(datalist2_10)

        if len(datalist3_3) != 0 :
            avg3_3 = sum(datalist3_3)/len(datalist3_3)
        if len(datalist3_5) != 0 :
            avg3_5 = sum(datalist3_5)/len(datalist3_5)
        if len(datalist3_10) != 0 :
            avg3_10 = sum(datalist3_10)/len(datalist3_10)
        

        temp_1 = db_session.query(avgtable).filter(avgtable.unit == '3minute').first()

        #심볼1표현
        #-1 ~ -0.3 : 1, -0.3 ~ 0.3 :2, 0.3 ~ 1 : 3 으로 표현
        temp_1.avg1 = avg1_3 
        s_data1, s_data2, s_data3 = 0, 0, 0
        if(temp_1.avg1 > -1 and temp_1.avg1 < 0):
            s_data1 = 1
        elif temp_1.avg1 > 0 and temp_1.avg1 < 0.1:
            s_data1 = 2
        else :
            s_data1 = 3

        #심볼2표현
        #0 ~ 0.33 : 1, 0.33 ~ 0.66 :2, 0.66 ~ 0.99 : 3 으로 표현
        temp_1.avg2 = avg2_3

        if(temp_1.avg2 >0 and temp_1.avg2 < 0.33):
            s_data2 = 1
        elif temp_1.avg2 > 0.33 and temp_1.avg2 < 0.66:
            s_data2 = 2
        else :
            s_data2 = 3


        temp_1.avg3 = avg3_3
        #심볼3표현
        #0 ~ -3 : 1, 3 ~6 :2, 6 ~ 9 : 3 으로 표현
        if(temp_1.avg3 >0 and temp_1.avg3 < 2):
            s_data3 = 1
        elif temp_1.avg3 > 2 and temp_1.avg3 < 2.5:
            s_data3 = 2
        else :
            s_data3 = 3

        db_session.add(symtable(s_data1,s_data2,s_data3))

        temp_1 = db_session.query(avgtable).filter(avgtable.unit == '5minute').first()
        temp_1.avg1 = avg1_5
        temp_1.avg2 = avg2_5
        temp_1.avg3 = avg3_5

        temp_1 = db_session.query(avgtable).filter(avgtable.unit == '10minute').first()
        temp_1.avg1 = avg1_10
        temp_1.avg2 = avg2_10
        temp_1.avg3 = avg3_10


        db_session.commit()  
        sleep(5)