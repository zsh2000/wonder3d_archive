import numpy as np
import os
import json
import shutil
from kiui.cam import orbit_camera

def inv_RT(RT):
    RT_h = np.concatenate([RT, np.array([[0,0,0,1]])], axis=0)
    RT_inv = np.linalg.inv(RT_h)
    #RT_inv = RT_inv[[0, 2, 1, 3]]
    #RT_inv[2] *= -1

    return RT_inv

save_dir = "/home/zheng720/gaussian-splatting/nerf_dog5_full_pose_1115/"

fix_cam_pose_dir = "./instant-nsr-pl/datasets/fixed_poses"
face_list = ["front", "front_left", "left", "back", "right", "front_right"]

final_json = {}
final_json["camera_angle_x"] = 0.6911112070083618

frame_list = []

for i in range(180):
    c2w = orbit_camera(0, i*2, radius=1.3, opengl=True)
    c2w[2:3] *= -1
    c2w = c2w[[0,2,1,3]]
    #w2c = np.loadtxt(os.path.join(fix_cam_pose_dir,'%03d_%s_RT.txt'%(0, face)))
    #c2w = inv_RT(w2c)

    #print(w2c, c2w, face)

    img_path = os.path.join("./cropped_img_1115/", str(i) + ".png")
    os.makedirs(os.path.join(save_dir, "train"), exist_ok=True)
    shutil.copy(img_path, os.path.join(save_dir, "train", os.path.basename(img_path)))

    frame_list.append({
        "file_path": os.path.join("./train", os.path.basename(img_path)[:-4]),
            "transform_matrix": c2w.tolist()})

final_json["frames"] = frame_list

transforms_train_path = os.path.join(save_dir, "transforms_train.json")
out_file = open(transforms_train_path, "w")
json.dump(final_json, out_file, indent=4) ### this saves the array in .json format

shutil.copy(transforms_train_path, transforms_train_path.replace("_train.json", "_test.json"))

shutil.copytree(os.path.join(save_dir, "train"), os.path.join(save_dir, "test"), dirs_exist_ok=True)
