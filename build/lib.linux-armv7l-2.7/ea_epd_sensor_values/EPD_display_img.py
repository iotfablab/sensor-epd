# Display an .xbm image centered (not re-scaled) on EPD. Max. image size 264x176.

from PIL import Image
from EPD import EPD


WHITE = 1
BLACK = 0


def EPD_display_img(epd, img_dir):

    epd.clear()
    
    image = Image.new('1', epd.size, WHITE)
    img = Image.open(img_dir, 'r')
    img_w, img_h = img.size

    #
    image.paste(img,( (epd.width - img_w)/2,  (epd.height - img_h)/2))

    epd.display(image)
    epd.update()


