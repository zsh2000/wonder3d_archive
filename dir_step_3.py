# !pip install rembg
import rembg
from PIL import Image
import os

img_dir = "./img_for_wonder3d/"

save_dir = "./img_for_wonder3d_rgba/"

os.makedirs(save_dir, exist_ok=True)

for img_name in os.listdir(img_dir):
    img_path = os.path.join(img_dir, img_name)

    img = Image.open(img_path)

    result = rembg.remove(img)
    #result = result.resize(newsize)
    result.save(os.path.join(save_dir, img_name))
#result.show()
