import os

img_list = os.listdir("./first_frame_dog7_wb_256_rgba")

for img_name in img_list:

    with open("official_script_0116_dog7.sh", "a") as file:
        file.write("accelerate launch --config_file 1gpu.yaml test_mvdiffusion_seq.py ")
        file.write("--config configs/mvdiffusion-joint-ortho-6views.yaml validation_dataset.root_dir=./first_frame_dog7_wb_256_rgba")
        file.write(" validation_dataset.filepaths=[\"" + img_name + "\"] save_dir=./outputs_0116_dog7_rgba \n")

