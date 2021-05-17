import sys
import os
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter

img_path = sys.argv[1]

basename = os.path.basename(img_path)
dirname = os.path.dirname(img_path)
basename_without_ext = os.path.splitext(os.path.basename(img_path))[0]

img = Image.open(img_path)
img = ImageEnhance.Color(img)
img = img.enhance(1.2)

# https://qiita.com/pashango2/items/145d858eff3c505c100a

img = img.resize((128, 128),Image.LANCZOS)

# Dilation
img = img.filter(ImageFilter.MinFilter())

# Color
img = ImageEnhance.Color(img)
img = img.enhance(1.8)

# Contrast
#img = ImageEnhance.Contrast(img)
#img = img.enhance(1.5)

# Sharpness
#img = ImageEnhance.Sharpness(img)
#img = img.enhance(3.0)

# Sharpness
#img = ImageEnhance.Sharpness(img)
#img = img.enhance(3.0)

#img = img.resize((16, 16),Image.BOX)
#img = img.resize((16, 16),Image.BILINEAR)
#img = img.resize((16, 16),Image.HAMMING)
#img = img.resize((16, 16),Image.LANCZOS)
img = img.resize((16, 16))

img.filter(ImageFilter.MaxFilter())

img_zoom = img.resize((512, 512))
img_zoom.show()
#img.save(dirname + '/' + basename_without_ext + '_05.png')

exit()
