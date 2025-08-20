import os
from pathlib import Path
from PIL import Image
from rembg import remove, new_session
import threading


def remove_backgrounds(input_dir, temp_dir):
    """
    Remove backgrounds from all images in the input directory
    """
    print("🚀 Starting background removal...")

    input_path = Path(input_dir)
    temp_path = Path(temp_dir)
    temp_path.mkdir(parents=True, exist_ok=True)

    valid_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}
    session = new_session()

    processed_count = 0
    for image_file in input_path.iterdir():
        if image_file.suffix.lower() in valid_extensions and image_file.is_file():
            try:
                print(f"Removing background from {image_file.name}...")

                input_image = Image.open(image_file)
                output_image = remove(input_image, session=session)

                # Save to temporary directory
                temp_file = temp_path / f"nobg_{image_file.stem}.png"
                output_image.save(temp_file)
                processed_count += 1

            except Exception as e:
                print(f"Error processing {image_file}: {str(e)}")

    print(f"✅ Background removal complete! {processed_count} images processed.")
    return temp_dir


def resize_to_exact_pixels(
    input_dir,
    output_dir,
    target_width,
    target_height,
    background_color=(255, 255, 255, 0),
):
    """
    Resize all images to exact pixel dimensions
    """
    print("📏 Starting resizing to exact dimensions...")

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    valid_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}

    processed_count = 0
    for image_file in input_path.iterdir():
        if image_file.suffix.lower() in valid_extensions and image_file.is_file():
            try:
                print(
                    f"Resizing {image_file.name} to {target_width}x{target_height}..."
                )

                # Open the image
                img = Image.open(image_file).convert("RGBA")

                # Resize to exact target dimensions
                resized_img = img.resize((target_width, target_height), Image.LANCZOS)

                # Create output path
                output_file = (
                    output_path
                    / f"{image_file.stem}_{target_width}x{target_height}.png"
                )

                # Save the image
                resized_img.save(output_file, "PNG")
                processed_count += 1

            except Exception as e:
                print(f"Error resizing {image_file}: {str(e)}")

    print(f"✅ Resizing complete! {processed_count} images resized.")


def get_user_dimensions():
    """
    Get exact target dimensions from user input
    """
    print("\n=== Target Pixel Dimensions ===")

    while True:
        try:
            width = int(input("Enter target WIDTH in pixels: "))
            height = int(input("Enter target HEIGHT in pixels: "))

            if width <= 0 or height <= 0:
                print("❌ Dimensions must be positive integers. Please try again.")
                continue

            print(f"✅ All images will be resized to: {width} x {height} pixels")
            return width, height

        except ValueError:
            print("❌ Please enter valid integers for width and height.")


def get_background_preference():
    """
    Ask user for background preference
    """
    print("\n=== Background Options ===")
    print("1. Transparent background (default - keeps transparency from rembg)")
    print("2. White background")
    print("3. Black background")

    choice = input("Choose background option (1-3, default 1): ").strip()

    if choice == "2":
        return (255, 255, 255, 255)  # White
    elif choice == "3":
        return (0, 0, 0, 255)  # Black
    else:
        return (255, 255, 255, 0)  # Transparent


def clean_temp_directory(temp_dir):
    """
    Clean up temporary files
    """
    temp_path = Path(temp_dir)
    if temp_path.exists():
        for file in temp_path.iterdir():
            if file.is_file():
                file.unlink()
        temp_path.rmdir()
        print("🧹 Temporary files cleaned up")


if __name__ == "__main__":
    print("🎯 Complete Image Processing Pipeline")
    print("=====================================")

    # Get directories
    input_directory = input(
        "Enter the path to your INPUT folder with original images: "
    ).strip()
    final_output_directory = input(
        "Enter the path to your FINAL OUTPUT folder: "
    ).strip()

    # Create temporary directory for background-removed images
    temp_directory = "temp_bg_removed"

    # Get target dimensions
    target_width, target_height = get_user_dimensions()

    # Get background preference
    background_color = get_background_preference()

    try:
        # Step 1: Remove backgrounds (using rembg)
        bg_removed_dir = remove_backgrounds(input_directory, temp_directory)

        # Step 2: Resize to exact dimensions
        resize_to_exact_pixels(
            bg_removed_dir,
            final_output_directory,
            target_width,
            target_height,
            background_color,
        )

        # Step 3: Clean up temporary files
        clean_temp_directory(temp_directory)

        print("\n" + "=" * 50)
        print("🎉 PROCESSING COMPLETE!")
        print(f"📁 Final images saved to: {final_output_directory}")
        print(f"📏 All images are now: {target_width} x {target_height} pixels")
        print(f"✅ Backgrounds removed and resized successfully!")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error during processing: {e}")
        # Clean up temp files even if there's an error
        clean_temp_directory(temp_directory)
