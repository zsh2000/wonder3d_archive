# !pip install rembg
import rembg
from PIL import Image

img = Image.open("./example_images/0.png")

result = rembg.remove(img)

result.save("./example_images/0_alpha.png")
#result.show()
