import os
import shutil
from PIL import Image

# Define dataset paths
dataset_path = "/kaggle/input/uecfood256/UECFOOD256"
output_path = "/kaggle/working/dataset"

# Define output directories
images_dir = os.path.join(output_path, "images/train")
labels_dir = os.path.join(output_path, "labels/train")

# Create output directories
os.makedirs(images_dir, exist_ok=True)
os.makedirs(labels_dir, exist_ok=True)

# ✅ Step 1: Load Food Category Mapping from category.txt
category_mapping = {}
category_file = os.path.join(dataset_path, "category.txt")

with open(category_file, "r", encoding="utf-8") as file:
    lines = file.readlines()[1:]  # Skip the header

for line in lines:
    parts = line.strip().split("\t")
    if len(parts) == 2:
        category_id, category_name = parts
        try:
            category_mapping[int(category_id)] = category_name
        except ValueError:
            print(f"⚠️ Skipping invalid line: {line}")

print("✅ Category Mapping Loaded Successfully.")

# ✅ Step 2: Process Each Food Category Directory
for category_id in category_mapping.keys():
    category_folder = os.path.join(dataset_path, str(category_id))
    
    if not os.path.exists(category_folder):
        continue

    # Path to the bounding box file
    bb_file = os.path.join(category_folder, "bb_info.txt")
    
    if not os.path.exists(bb_file):
        continue

    with open(bb_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        data = line.strip().split()

        if len(data) != 5:
            continue

        img_name, x1, y1, x2, y2 = data
        try:
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        except ValueError:
            continue

        # New standardized image name (categoryID_imageID.jpg)
        new_img_name = f"{img_name}_{category_id}.jpg"
        old_img_path = os.path.join(category_folder, f"{img_name}.jpg")
        new_img_path = os.path.join(images_dir, new_img_name)

        # Skip if image does not exist
        if not os.path.exists(old_img_path):
            continue

        # Get actual image size
        with Image.open(old_img_path) as img:
            image_width, image_height = img.size  # Dynamically get image size

        # Copy and rename image to output folder
        shutil.copy(old_img_path, new_img_path)

        # Compute YOLO format bounding box
        bbox_width = x2 - x1
        bbox_height = y2 - y1
        x_center = x1 + bbox_width / 2
        y_center = y1 + bbox_height / 2

        # Normalize YOLO format (values between 0 and 1)
        x_center /= image_width
        y_center /= image_height
        bbox_width /= image_width
        bbox_height /= image_height

        # Ensure values are within [0,1] to prevent out-of-bounds errors
        x_center = min(max(x_center, 0), 1)
        y_center = min(max(y_center, 0), 1)
        bbox_width = min(max(bbox_width, 0), 1)
        bbox_height = min(max(bbox_height, 0), 1)

        # Create YOLO label file
        label_file = os.path.join(labels_dir, f"{img_name}_{category_id}.txt")
        with open(label_file, "w") as f:
            f.write(f"{category_id-1} {x_center} {y_center} {bbox_width} {bbox_height}\n")  # YOLO class index starts from 0

print("✅ YOLO Dataset Preparation Completed Successfully! 🚀")
