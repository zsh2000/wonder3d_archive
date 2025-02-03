import numpy as np
import os
import json
import shutil

def inv_RT(RT):
    RT_h = np.concatenate([RT, np.array([[0,0,0,1]])], axis=0)
    RT_inv = np.linalg.inv(RT_h)
    #RT_inv = RT_inv[[0, 2, 1, 3]]
    #RT_inv[2] *= -1

    return RT_inv


fix_cam_pose_dir = "./instant-nsr-pl/datasets/fixed_poses"
face_list = ["front", "front_left", "left", "back", "right", "front_right"]

final_json = {}
final_json["camera_angle_x"] = 0.6911112070083618

frame_list = []

for face in face_list:
    w2c = np.loadtxt(os.path.join(fix_cam_pose_dir,'%03d_%s_RT.txt'%(0, face)))
    c2w = inv_RT(w2c)

    print(w2c, c2w, face)

    img_path = os.path.join("outputs/cropsize-192-cfg1.0/0_alpha/masked_colors/rgb_%03d_%s.png"%(0, face))
    os.makedirs(os.path.join("/home/zheng720/gaussian-splatting/nerf_dog5_full_pose/", "train"), exist_ok=True)
    shutil.copy(img_path, os.path.join("/home/zheng720/gaussian-splatting/nerf_dog5_full_pose/", "train", os.path.basename(img_path)))

    frame_list.append({
        "file_path": os.path.join("./train", os.path.basename(img_path)[:-4]),
            "transform_matrix": c2w.tolist()})

final_json["frames"] = frame_list
out_file = open("/home/zheng720/gaussian-splatting/nerf_dog5_full_pose/transforms_train.json", "w")
json.dump(final_json, out_file, indent=4) ### this saves the array in .json format
