import os
from PIL import Image

# Define the input and output directories
input_folder = "./first_frame_dog7_wb_256"
output_folder = "./first_frame_dog7_wb_256_rgba"
os.makedirs(output_folder, exist_ok=True)

# Loop through each file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".png"):  # Process only PNG files
        # Open the image
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path).convert("RGBA")

        # Get pixel data
        pixels = image.getdata()

        # Define a new pixel data list where (255, 255, 255) becomes transparent
        new_pixels = [
            (r, g, b, 0) if (r, g, b) == (255, 255, 255) else (r, g, b, a)
            for (r, g, b, a) in pixels
        ]

        # Update image with the new pixels
        image.putdata(new_pixels)

        # Save the modified image to the output folder
        output_path = os.path.join(output_folder, filename)
        image.save(output_path)

print("Processing complete. Modified images saved to", output_folder)

