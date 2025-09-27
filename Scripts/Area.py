import numpy as np
from PIL import Image
import sys
import os

def count_pixels_greater_than_threshold(image_path, threshold_numerator, threshold_denominator, output_path=None):
    """
    Opens a TIFF image, counts pixels greater than the threshold (330), and 
    optionally saves a binary mask image.

    Args:
        image_path (str): The file path to the input TIFF image.
        threshold_numerator (int): The numerator of the threshold fraction (e.g., 330).
        threshold_denominator (int): The denominator of the threshold fraction (e.g., 65535).
        output_path (str, optional): The file path to save the binary mask image.

    Returns:
        int or dict: The total count of pixels across all bands or a dictionary of counts per band.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at '{image_path}'", file=sys.stderr)
        return None

    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error: Could not open image file. Details: {e}", file=sys.stderr)
        return None

    # Convert to NumPy array
    img_array = np.array(img)
    
    # The comparison logic is P > 330 for a 16-bit integer image (0-65535 range)
    integer_threshold = threshold_numerator

    # Handle single-band vs. multi-band images
    if img_array.ndim == 2:
        # Single-band (Grayscale) image
        
        # Create the boolean mask
        mask = img_array > integer_threshold
        
        # Count the 'True' values (pixels > 330)
        pixel_count = np.sum(mask)
        
        if output_path:
            # Convert the boolean mask to an 8-bit image (0 or 255) for saving
            # The True values (pixels > 330) will be white (255)
            mask_img = Image.fromarray(mask.astype(np.uint8) * 255)
            try:
                mask_img.save(output_path)
                print(f"\nSuccessfully saved binary mask to: {output_path}")
            except Exception as e:
                print(f"\nError: Could not save output image to {output_path}. Details: {e}", file=sys.stderr)

        return pixel_count
    
    elif img_array.ndim == 3:
        # Multi-band (e.g., RGB) image. Shape is (Height, Width, Bands)
        counts = {}
        
        # For simplicity, we'll count the pixels in the FIRST band
        # You may need to adapt this logic based on your specific TIFF structure
        band_data = img_array[..., 0] # Get the first band/channel
        
        mask = band_data > integer_threshold
        band_count = np.sum(mask)
        counts['Total_Count_First_Band'] = band_count
        
        if output_path:
            mask_img = Image.fromarray(mask.astype(np.uint8) * 255)
            try:
                mask_img.save(output_path)
                print(f"\nSuccessfully saved binary mask of the *first band* to: {output_path}")
            except Exception as e:
                print(f"\nError: Could not save output image to {output_path}. Details: {e}", file=sys.stderr)

        return counts

    else:
        return f"Image array has an unexpected number of dimensions: {img_array.ndim}"


# --- Execution Block ---
if __name__ == "__main__":
    
    # The script expects 3 command-line arguments: script_name, input_file, output_file
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input_tiff_file> <output_jpg_file>", file=sys.stderr)
        sys.exit(1)

    # Get file paths from command-line arguments
    INPUT_IMAGE_PATH = sys.argv[1]
    OUTPUT_IMAGE_PATH = sys.argv[2]
    
    # Set the fixed threshold (330/65535)
    THRESHOLD_NUM = 330
    THRESHOLD_DEN = 65535 

    # Run the main function
    count_result = count_pixels_greater_than_threshold(
        INPUT_IMAGE_PATH, 
        THRESHOLD_NUM, 
        THRESHOLD_DEN,
        OUTPUT_IMAGE_PATH
    )

    if count_result is not None:
        print("\n--- Pixel Analysis Result ---")
        print(f"Input File: {INPUT_IMAGE_PATH}")
        print(f"Threshold (Value > 330):")
        
        if isinstance(count_result, int):
            print(f"Total Pixels Greater Than 330: {count_result}")
        elif isinstance(count_result, dict):
            # For multi-band image, print the count for the primary band analyzed
            print(f"Pixels Greater Than 330 (First Band): {count_result.get('Total_Count_First_Band')}")
        
        print("-----------------------------")