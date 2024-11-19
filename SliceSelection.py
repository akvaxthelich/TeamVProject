# Slice Selection Algorithm using OpenCV python library
# Processes all slides in the 'preds' folder to find valid slices per patient
# First preprocesses slides to group them by patient 
# Then for each patient analyzes slides by thresholding and detecting contours
# Saves all range results in an array and returns

import os
import cv2

# Input arguments:
    # folder_path: Path to the folder containing slides
    # min_bone_area: The minimum area (in pixels) that the bones need to have for slice to qualify
def process_slices(folder_path, min_bone_area):

    patient_slices = {}

    # Iterate through all files in the folder
    for file_name in sorted(os.listdir(folder_path)):
        if file_name.endswith('_pred.png'):
            # Extract patient ID and slice number
            parts = file_name.split('_')
            patient_id = parts[0]
            slice_num = int(parts[1])
            
            # Group by patient ID
            if patient_id not in patient_slices:
                patient_slices[patient_id] = []
            patient_slices[patient_id].append((slice_num, file_name))
    
    # Array to store valid ranges for each patient
    patient_ranges = {}

    for patient_id, slices in patient_slices.items():
        valid_start, valid_end = None, None

        # Process slices for the current patient
        for slice_num, file_name in sorted(slices):
            # Load and preprocess the image
            img_path = os.path.join(folder_path, file_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            _, binary_img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

            # Detect contours
            contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            bone_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_bone_area]

            # Check for valid bones
            if len(bone_contours) >= 2:  # Both femur and tibia detected
                if valid_start is None:
                    valid_start = slice_num
                valid_end = slice_num

        # Save the range for this patient
        if valid_start is not None and valid_end is not None:
            patient_ranges[patient_id] = (valid_start, valid_end)
        else:
            patient_ranges[patient_id] = None  # No valid slices found for this patient

    return patient_ranges

# Example usage
folder_path = './preds'
slice_ranges = process_slices(folder_path, 4000)

# Print the results
for patient_id, valid_range in slice_ranges.items():
    if valid_range:
        print(f"Patient {patient_id}: Valid slices from {valid_range[0]} to {valid_range[1]}")
    else:
        print(f"Patient {patient_id}: No valid slices found.")
