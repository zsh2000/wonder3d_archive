
import os
import cv2

# Path to the folder containing the images
input_folder = "img_for_wonder3d"
output_folder = "img_for_wonder3d_resized"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate through each file in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            # Read the image
            img = cv2.imread(input_path)
            if img is None:
                print(f"Could not read {input_path}, skipping...")
                continue

            # Resize the image to 512x512
            resized_img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_AREA)

            # Save the resized image to the output folder
            cv2.imwrite(output_path, resized_img)
            print(f"Resized and saved: {output_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

