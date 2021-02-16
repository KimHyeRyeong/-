from PIL import Image, ImageDraw,ImageFont
import os
import datetime

img = Image.open('감자.jpg')

fontsFolder = "C:\\Users\\user\\Desktop\\Pythonworkspace\\study"
selectFont = ImageFont.truetype(os.path.join(fontsFolder,'CookieRun Regular.ttf'), 50)
draw = ImageDraw.Draw(img)
current = datetime.datetime.now()
draw.text((460,870), str(current), fill="white", font=selectFont, align='center')
img.save('감자2.jpg')

