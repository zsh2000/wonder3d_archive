from PIL import Image
import os

# Input and output directories
input_dir = "./single_img_input"
output_dir = "./single_img_input_wb"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process each image in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith((".png", ".tif", ".tiff")):  # Add other formats if needed
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Load the RGBA image
        rgba_image = Image.open(input_path).convert("RGBA")

        # Create a white background
        white_background = Image.new("RGB", rgba_image.size, (255, 255, 255))

        # Composite the image onto the white background
        composite = Image.alpha_composite(white_background.convert("RGBA"), rgba_image)

        # Save the output image
        composite.save(output_path, "PNG")  # Save as PNG to preserve quality
        print(f"Processed {filename} and saved to {output_path}")

