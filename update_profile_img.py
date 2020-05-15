from PIL import Image, ImageFont, ImageDraw
import locale
import re
import covid_check
from datetime import date

#load the daily data from web scrapper

today = date.today().strftime("%-d.%m.%Y")
with open("covid_tr.csv", "r") as file:
    first_line = file.readline()
    for last_line in file:
        pass

data = {\
'date':'',\
'conf_new':'',\
'conf_total':'',\
'deaths_new':'',\
'deaths_total':'',\
'rec_new':'',\
'rec_total':'',\
'intube_total':'',\
'severe_total':'',\
'tests_new':'',\
'tests_total':'',\
'conf_death_rate':'',\
'active':'',\
}
data = dict(zip(list(data.keys()),last_line.rstrip().split(',')))

if data['date'] == today:
    print("Reading from file")
else:
    data = covid_check.daily_data()
#data = {\
#    'date':'',\
#    'tests_total':'',\
#    'conf_total':'',\
#    'deaths_total':'',\
#    'severe_total':'',\
#    'intube_total':'',\
#    'rec_total':'',\
#    'tests_new':'',\
#    'conf_new':'',\
#    'deaths_new':'',\
#    'rec_new':'',\
#    'conf_death_rate':'',\
#    'active':'',\
#}

#data['conf_total'] = "120204"
#data['deaths_total'] = "3174"
#data['active'] = "68144"


#Confirmed Cases and Deaths are written on top of my profile image
#1000s seperated by "."
text1 = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',data['conf_total'])
text2 = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',data['deaths_total'])
text3 = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',data['active'])

uparr = "↑"

fontsize = 90
fillcolor1 = "white"
shadowcolor1 = "black"

fillcolor2 = "white"
shadowcolor2 = "red"

fillcolor3 = "white"
shadowcolor3 = "green"

font = ImageFont.truetype("Impact.ttf", fontsize)
arrfont = ImageFont.truetype("LucidaGrande.ttc", int(fontsize/2))
img  = Image.open("profile_img_cropped.png")

width, height = img.size
#print(width, height)

draw = ImageDraw.Draw(img)

#get the width and heigth of the texts, this function gets the actual width and height
#of the box the text is placed into.

(a,b,fwidth1,fheight1) = font.getmask(text1).getbbox()
(a,b,fwidth2,fheight2) = font.getmask(text2).getbbox()
(a,b,fwidth3,fheight3) = font.getmask(text3).getbbox()

print("fwidth1,fheight1",fwidth1,fheight1)
print("fwidth2,fheight2",fwidth2,fheight2)
print("fwidth3,fheight3",fwidth3,fheight3)


x = (width - fwidth1)/2 - 5
y = (height - (fheight1+fheight2+fheight3+32))/2

print("x,y",x,y)

#now, second line is center aligned wrt width and 4 pixel under the first.
x2 = x + (fwidth1-fwidth2)/2
y2 = y + fheight1 + 4

x3 = x + (fwidth1-fwidth3)/2
y3 = y + fheight1 + fheight2 + 8

#draw the text on top of the image with an outline as given color and size.
draw.text((x, y),   text1, font=font, fill=fillcolor1, stroke_fill=shadowcolor1, stroke_width=2)
#draw.text((x+fwidth1, y+20),   uparr, font=arrfont, fill=fillcolor1, stroke_fill=shadowcolor1, stroke_width=2)
draw.text((x2, y2), text2, font=font, fill=fillcolor2, stroke_fill=shadowcolor2, stroke_width=2)
draw.text((x3, y3), text3, font=font, fill=fillcolor3, stroke_fill=shadowcolor3, stroke_width=2)

#prepare for cropping
#left = 90
#top = 150
#w = 320

#img_cropped = img.crop((left, top, left+w, top+w))

#display the profile image to be updated
#img_cropped.show()
img.show()

img.save("update_profile_img.png")
#img_cropped.save("update_profile_img_crop.png")
