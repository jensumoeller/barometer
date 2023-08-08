from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, ssd1306
from PIL import ImageFont, ImageDraw, Image
import time

# Initialisieren des OLED Displays
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, height=32, width=128, rotate=0)

oled_font = ImageFont.truetype('FreeSans.ttf', 18)
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline = "white", fill = "black")
    draw.text((5, 5), "OLED-Display", font = oled_font, fill = "white")

time.sleep(10)
