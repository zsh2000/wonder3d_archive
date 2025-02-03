import os
from PIL import Image

def convert_rgba_to_rgb(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process all files in the input directory
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)

        # Skip non-image files
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        try:
            # Open the image and convert it
            with Image.open(input_path).convert("RGBA") as rgba_image:
                # Create a white background image
                white_background = Image.new("RGB", rgba_image.size, (255, 255, 255))
                # Composite the RGBA image onto the white background
                rgb_image = Image.alpha_composite(white_background.convert("RGBA"), rgba_image).convert("RGB")

                # Save the image in the output directory
                output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".jpg")
                rgb_image.save(output_path, "JPEG")
                print(f"Converted and saved: {output_path}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

# Directories
input_directory = "get_rgba_first_frame_short_video_256"
output_directory = "rgb_first_frame_short_video_256"

# Convert all images
convert_rgba_to_rgb(input_directory, output_directory)

