import kiui
from kiui.op import recenter
from kiui.cam import orbit_camera
import rembg
import os
import cv2

from PIL import Image

import numpy as np


os.makedirs("single_img_input_revised_wb", exist_ok=True)
kiui.seed_everything(42)


img_list = os.listdir("/home/zheng720/wonder3d/Wonder3D/img_for_mask_1122")
for img_name in img_list:
    img_path = os.path.join("/home/zheng720/wonder3d/Wonder3D/img_for_mask_1122", img_name)
    # img_path_for_mask = os.path.join("/home/zheng720/wonder3d/Wonder3D/img_for_mask_1122/", img_name)
    input_image = kiui.read_image(img_path, mode='uint8')
    # img_for_mask = kiui.read_image(img_path_for_mask, mode='uint8')
    # input_image = cv2.resize(input_image, (256, 256))
    # img_for_mask = cv2.resize(img_for_mask, (256, 256))

    bg_remover = rembg.new_session()

    # bg removal
    carved_image = rembg.remove(input_image, session=bg_remover) # [H, W, 4]
    mask = carved_image[..., -1] > 0

    # recenter
    image = recenter(carved_image, mask, border_ratio=0.2)

    image = cv2.resize(image, (256, 256))

    print(image)
    im1 = Image.fromarray(image)


    white_background = Image.new("RGB", im1.size, (255, 255, 255))

        # Composite the image onto the white background
    composite = Image.alpha_composite(white_background.convert("RGBA"), im1)
    

    # #import rembg
    # im1 = rembg.remove(im1)

    composite.save("./single_img_input_revised_wb/" + str(img_name))