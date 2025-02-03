import kiui
from kiui.op import recenter
from kiui.cam import orbit_camera
import numpy as np
import tqdm
import torch

def RT_opengl2opencv(RT):
     # Build the coordinate transform matrix from world to computer vision camera
    # R_world2cv = R_bcam2cv@R_world2bcam
    # T_world2cv = R_bcam2cv@T_world2bcam

    R = RT[:3, :3]
    t = RT[:3, 3]

    R_bcam2cv = torch.tensor([[1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])

    R_world2cv = R_bcam2cv @ R
    t_world2cv = R_bcam2cv @ t

    RT = torch.cat([R_world2cv, t_world2cv[:,None]], 1)

    return RT

azimuth = np.arange(0, 360, 2, dtype=np.int32)
elevation = 0

def inv_RT(RT):
    RT_h = torch.concatenate([RT, torch.tensor([[0,0,0,1]])])
    RT_inv = torch.linalg.inv(RT_h)

    return RT_inv[:3, :]

pose_list = []
for azi in tqdm.tqdm(azimuth):
    c2w = torch.from_numpy(orbit_camera(elevation, azi, radius=1.3, opengl=True))
    c2w[2:3] *= -1
    c2w = c2w[[0,2,1,3]]
    RT = torch.linalg.inv(c2w)[:3]
    RT_opencv = RT_opengl2opencv(RT)
    pose = inv_RT(RT_opencv)
    pose_list.append(pose.cpu().numpy())
    print(pose)

pose_for_save = np.stack(pose_list)
np.save("precomputed_test_pose.npy", pose_for_save)
print(pose_for_save.shape)
