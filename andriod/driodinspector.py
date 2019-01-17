from subprocess import Popen
from PIL import Image, ImageDraw
import os
# f ='source.png'
# img = Image.open(f)
# g = ImageDraw.Draw(img)
# g.show()
print(os.getcwd())
p = Popen('andriod\inspect.bat')
p.wait()
print('done')