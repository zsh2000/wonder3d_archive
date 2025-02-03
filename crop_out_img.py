import os
import cv2

img_dir = "/home/zheng720/wonder3d/Wonder3D/instant-nsr-pl/exp/0_alpha_256/@20241113-113324/save/it3000-test/"
img_list = os.listdir(img_dir)

os.makedirs("./cropped_img_1115", exist_ok=True)
for img_name in img_list:
    img_path = os.path.join(img_dir, img_name)
    selected_img = cv2.imread(img_path)[:, 1024:2048, :]
    cv2.imwrite(os.path.join("./cropped_img_1115", os.path.basename(img_path)), selected_img)

    
