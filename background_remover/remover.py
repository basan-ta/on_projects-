import os
from pathlib import Path
from rembg import remove
from PIL import Image


def process_images(input_dir, output_dir):
    """
    Process all images in the input directory, remove backgrounds,
    and save them to the output directory.

    Args:
        input_dir (str): Path to the directory containing input images
        output_dir (str): Path to the directory where processed images will be saved
    """
    # Convert to Path objects for easier handling
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Check if input directory exists
    if not input_path.exists():
        raise ValueError(f"Input directory '{input_dir}' does not exist")

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    # Supported image extensions
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}

    # Process each image in the input directory
    for image_file in input_path.iterdir():
        if image_file.suffix.lower() in valid_extensions and image_file.is_file():
            try:
                print(f"Processing {image_file.name}...")

                # Open and process the image
                input_image = Image.open(image_file)
                output_image = remove(input_image)

                # Create output path with PNG extension (to preserve transparency)
                output_file = output_path / f"{image_file.stem}_nobg.png"

                # Save the image
                output_image.save(output_file)
                print(f"Saved processed image to {output_file}")

            except Exception as e:
                print(f"Error processing {image_file}: {str(e)}")

    print("Processing complete!")


if __name__ == "__main__":
    # Set your input and output directories here
    input_directory = "./input_images"
    output_directory = "./output_images"

    # Process all images
    process_images(input_directory, output_directory)
