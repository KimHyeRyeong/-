import threading

from database import init_db
from database import db_session
from model import create_models
from model import create_symbol_table
from model import create_avg_table
from model import create_img_table
import model

image_table_1 = create_img_table("imgtable1")
image_table_2 = create_img_table("imgtable2")
image_table_3 = create_img_table("imgtable3")



def input_information():
    unit, time = 0,0
    while True:
        # print("시간 단위를 입력해 주세요. 1.일 2.시간 3.분 4.초")
        # unit = input("->")
        # intUnit = int(unit)
        # if intUnit > 0 and intUnit < 5:
        #     if intUnit == 1 :
        #         unit = "일"
        #     elif intUnit == 2 :
        #         unit = "시간"
        #     elif intUnit == 3 :
        #         unit = "분"
        #     else :
        #         unit = "초"
        #     break
        # else:
        #     print("잘못된 입력입니다.")

        try:
            print("시간 단위를 입력해 주세요. 1.일 2.시간 3.분 4.초")
            unit = int(input("->"))
            if unit > 0 and unit < 5:
                if unit == 1 :
                    unit = "일"
                elif unit == 2 :
                    unit = "시간"
                elif unit == 3 :
                    unit = "분"
                else :
                    unit = "초"
                break
        
        except ValueError :
            print("잘못된 입력입니다.")
        
    while True :
        try:
            print("시간 간격을 입력해 주세요(정수 입력)")
            time = int(input("->"))
            break
        except ValueError :
            print("잘못된 입력입니다.")

    return unit, time

def time_translate(unitinfo, timeinfo):
    tableNumber = 0
    while tableNumber < 3 :
        if unitinfo[tableNumber] == "초" :
            pass

        elif unitinfo[tableNumber] == "분" :
            minute = 60 * timeinfo[tableNumber] 
            timeinfo[tableNumber] = minute

        elif unitinfo[tableNumber] == "시간":
            hour = 3600 * timeinfo[tableNumber]
            timeinfo[tableNumber] = hour

        else :
            date = 86400 * timeinfo[tableNumber]
            timeinfo[tableNumber] = date

        tableNumber = tableNumber + 1
    return timeinfo


def run():

    print("프로그램을 시작합니다..")
    print("그래프를 표현할 3개의 데이터를 입력받습니다.")
    
    tableNumber = 0
    unitinfo = []
    timeinfo = []

    while tableNumber < 3 :
        print("테이블{0}의 데이터 정보를 입력받습니다.".format(tableNumber+1))
        aList = input_information()
        print("테이블{0}은 {1}{2}마다 데이터를 생성합니다.".format(tableNumber+1, aList[1],aList[0] ))
        timeinfo.append(aList[1])
        unitinfo.append(aList[0])


        tableNumber = tableNumber + 1

    timeinfo = time_translate(unitinfo, timeinfo)

    new_table_1 = create_models("table1")
    new_table_2 = create_models("table2")
    new_table_3 = create_models("table3")


    new_avgtable = create_avg_table("avgtable")

    new_symbol_table = create_symbol_table("symtable")

    init_db()

    model.add_unit_entry(new_avgtable)



        
    p1 = threading.Thread(target=model.data_generator1, args=(new_table_1, timeinfo[0],))
    p2 = threading.Thread(target=model.data_generator2, args=(new_table_2, timeinfo[1],))
    p3 = threading.Thread(target=model.data_generator3, args=(new_table_3, timeinfo[2],))
    p4 = threading.Thread(target=model.data_update, args=(new_table_1,new_table_2,new_table_3, new_avgtable,new_symbol_table,))
    
    p1.start()
    p2.start()
    p3.start()
    p4.start()
if __name__ == '__main__':
    run()
