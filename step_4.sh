accelerate launch --config_file 1gpu.yaml test_mvdiffusion_seq.py \
            --config configs/mvdiffusion-joint-ortho-6views.yaml validation_dataset.root_dir=./img_for_wonder3d_rgba \
            validation_dataset.filepaths=[] save_dir=./outputs_1122
