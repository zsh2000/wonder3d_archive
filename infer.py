
# First clone the repo, and use the commands in the repo

import torch
import requests
from PIL import Image
import numpy as np
from torchvision.utils import make_grid, save_image
from diffusers import DiffusionPipeline  # only tested on diffusers[torch]==0.19.3, may have conflicts with newer versions of diffusers
import cv2
import torchvision.transforms as T
import os

def load_wonder3d_pipeline():

    pipeline = DiffusionPipeline.from_pretrained(
    'flamehaze1115/wonder3d-v1.0', # or use local checkpoint './ckpts'
    custom_pipeline='flamehaze1115/wonder3d-pipeline',
    torch_dtype=torch.float16
    )

    # enable xformers
    pipeline.unet.enable_xformers_memory_efficient_attention()

    if torch.cuda.is_available():
        pipeline.to('cuda:0')
    return pipeline

pipeline = load_wonder3d_pipeline()

img_dir = "./img_for_wonder3d"
img_list = os.listdir(img_dir)

save_dir = "./img_for_wonder3d_4mv_wb"
os.makedirs(save_dir, exist_ok=True)

for img_name in img_list:
    # Download an example image.
    cond = Image.open(os.path.join(img_dir, img_name)).resize((256, 256))
    
    # The object should be located in the center and resized to 80% of image height.
    cond = Image.fromarray(np.array(cond)[:, :, :3])
    seed = 43
    generator = torch.Generator(device=pipeline.unet.device).manual_seed(seed)
    # Run the pipeline!
    images = pipeline(cond, generator=generator, num_inference_steps=20, output_type='pt', guidance_scale=1.0).images
    print(images.shape)
    #result = make_grid(images, nrow=6, ncol=2, padding=0, value_range=(0, 1))
    transform = T.ToPILImage()
    img1 = transform(images[6])
    img2 = transform(images[8])
    img3 = transform(images[9])
    img4 = transform(images[10])

    img1.save(os.path.join(save_dir, str(seed) + "_6_" + img_name))
    img2.save(os.path.join(save_dir, str(seed) + "_8_" + img_name))
    img3.save(os.path.join(save_dir, str(seed) + "_9_" + img_name))
    img4.save(os.path.join(save_dir, str(seed) + "_10_" + img_name))
    #cv4.imwrite("image_0_6.png", images[6, [2,1,0], :, :].permute(1,2,0).detach().cpu().numpy()*255.)
    #cv2.imwrite("image_0_8.png", images[8, [2,1,0], :, :].permute(1,2,0).detach().cpu().numpy()*255.)
    #cv2.imwrite("image_0_9.png", images[9, [2,1,0], :, :].permute(1,2,0).detach().cpu().numpy()*255.)
    #cv2.imwrite("image_0_10.png", images[10, [2,1,0], :, :].permute(1,2,0).detach().cpu().numpy()*255.)
    
    #save_image(result, 'result.png')
