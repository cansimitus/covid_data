from PIL import Image, ImageFont, ImageDraw
import locale
import covid_check

#load the daily data from web scrapper
data = covid_check.daily_data()

#Confirmed Cases and Deaths are written on top of my profile image
text1 = data['conf_total']
text2 = data['deaths_total']

fontsize = 90
fillcolor1 = "white"
shadowcolor1 = "black"
fillcolor2 = "white"
shadowcolor2 = "red"
font = ImageFont.truetype("Impact.ttf", fontsize)
img = Image.open("profile_img.png")

#width, height = img.size
#print(width, height)

draw = ImageDraw.Draw(img)

#get the width and heigth of the texts, this function gets the actual width and height
#of the box the text is placed into.
(a,b,fwidth1,fheight1)= font.getmask(text1).getbbox()
(a,b,fwidth2,fheight2) = font.getmask(text2).getbbox()

#find the initial coordinated by opening the image in GIMP and record.
x = 150
y = 160

#now, second line is center aligned wrt width and 4 pixel under the first.
x2 = x + (fwidth1-fwidth2)/2
y2 = y + fheight1 + 4

#draw the text on top of the image with an outline as given color and size.
draw.text((x, y), text1, font=font, fill=fillcolor1, stroke_fill=shadowcolor1, stroke_width=2)
draw.text((x2, y2), text2, font=font, fill=fillcolor2, stroke_fill=shadowcolor2, stroke_width=2)

#prepare for cropping
left = 135
top = 110
w = 250

img_cropped = img.crop((left, top, left+w, top+w))

#display the profile image to be updated
img_cropped.show()

img.save("update_profile_img.png")
img_cropped.save("update_profile_img_crop.png")
