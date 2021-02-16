from fastapi import FastAPI
from typing import Optional
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse

#PIL 관련
from PIL import Image, ImageDraw,ImageFont
import os
import datetime

from database import db_session
from database import init_db

from controller import image_table_1, image_table_2, image_table_3

from database import Base
from pydantic import BaseModel

from datetime import datetime

init_db()
app = FastAPI()

image_table_1.query.delete()

#DB에 이미지 삽입
db_session.add_all([
    image_table_1('2021-02-07', '20210207_000029_SDO_AIA_304_512.jpg'),
    image_table_1('2021-02-08', '20210208_000029_SDO_AIA_304_512.jpg'),
    image_table_1('2021-02-09', '20210209_000017_SDO_AIA_304_512.jpg'),
    image_table_1('2021-02-10', '20210210_000017_SDO_AIA_304_512.jpg'),
    image_table_1('2021-02-11', '20210211_000017_SDO_AIA_304_512.jpg'),
    image_table_1('2021-02-12', '20210212_000005_SDO_AIA_304_512.jpg'),
    image_table_1('2021-02-13', '20210213_235529_SDO_AIA_304_512.jpg'),
    image_table_1('2021-02-14', '20210214_235941_SDO_AIA_304_512.jpg'),
    image_table_1('2021-02-15', '20210215_000005_SDO_AIA_304_512.jpg')
])

db_session.add_all([
    image_table_2('2021-02-10', '20210210_0000_c2_512.jpg'),
    image_table_2('2021-02-11', '20210211_0000_c2_512.jpg'),
    image_table_2('2021-02-12', '20210212_0000_c2_512.jpg'),
    image_table_2('2021-02-13', '20210213_0000_c2_512.jpg'),
    image_table_2('2021-02-14', '20210214_0000_c2_512.jpg'),
    image_table_2('2021-02-15', '20210215_2112_c2_1024.jpg'),
    
])

db_session.add_all([
    image_table_3('2021-02-10', '20210210_0006_c3_512.jpg'),
    image_table_3('2021-02-11', '20210211_0006_c3_512.jpg'),
    image_table_3('2021-02-12', '20210212_0006_c3_512.jpg'),
    image_table_3('2021-02-13', '20210213_0006_c3_512.jpg'),
    image_table_3('2021-02-14', '20210214_0006_c3_512.jpg'),
    image_table_3('2021-02-15', '20210215_2118_c3_1024.jpg'),
    
])

db_session.commit()

def image_processing(from_value,date_value, table, first_path):
    dt = db_session.query(table).filter(table.datetime == date_value).first()
    file_path = first_path + dt.image


    img = Image.open(file_path)
    img = img.resize((210,210))

    fontsFolder = "C:\\Users\\user\\Desktop\\Pythonworkspace\\2020 winter"
    selectFont = ImageFont.truetype(os.path.join(fontsFolder,'NanumBarunGothic.ttf'), 18)
    draw = ImageDraw.Draw(img)

    temp = from_value
    draw.text((12,10), temp, fill="white", font=selectFont, align='center')
    save_path = first_path + 'new_file.jpg'
    img.save(save_path)

def no_data_html():
    html_content = """
        <body>
        <center>
        <h3 style ="color: yellow;">no data</h3>
        </body>
    """
    return HTMLResponse(content=html_content, status_code = 200)

@app.get("/AIA", response_class=HTMLResponse)
async def read_AIA(from_value: str):

    date_value = from_value[0:10]
    if db_session.query(image_table_1).filter(image_table_1.datetime == date_value).first() != None :
        image_processing(from_value, date_value, image_table_1, "AIA\\")
        return generate_html()

    else :
        return no_data_html()

def generate_html():
    html_content = """
        <body style="margin:0px;">
        <center>
        <img src = "http://localhost:8080/AIA/new_file.jpg">
        </center>
        </body>
        """
    return HTMLResponse(content=html_content, status_code = 200)





@app.get("/C2", response_class=HTMLResponse)
async def read_C2(from_value: str):

    date_value = from_value[0:10]
    if db_session.query(image_table_2).filter(image_table_2.datetime == date_value).first() != None :
        image_processing(from_value, date_value, image_table_2, "C2\\")

        return generate_html_C2()

    else :
        return no_data_html()

def generate_html_C2():
    html_content = """
        <body style="margin:0px;">
        <center>
        <img src = "http://localhost:8080/C2/new_file.jpg">
        </center>
        </body>
        """
    return HTMLResponse(content=html_content, status_code = 200)


@app.get("/C3", response_class=HTMLResponse)
async def read_C3(from_value: str):

    date_value = from_value[0:10]
    if db_session.query(image_table_3).filter(image_table_3.datetime == date_value).first() != None :
        image_processing(from_value, date_value, image_table_3, "C3\\")

        return generate_html_C3()

    else :
        return no_data_html()

def generate_html_C3():
    html_content = """
        <body style="margin:0px;">
        <center>
        <img src = "http://localhost:8080/C3/new_file.jpg">
        </center>
        </body>
        """
    return HTMLResponse(content=html_content, status_code = 200)