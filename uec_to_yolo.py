import os
from PIL import Image

# Define dataset path
dataset_path = "/kaggle/input/uecfood256/UECFOOD256"  # Kaggle dataset path
labels_root = "/kaggle/working/labels"  # Save labels in Kaggle working directory
os.makedirs(labels_root, exist_ok=True)  # Create labels root if not exists

# Function to convert bounding box to YOLO format
def convert_to_yolo(x1, y1, x2, y2, img_width, img_height):
    center_x = (x1 + x2) / 2 / img_width
    center_y = (y1 + y2) / 2 / img_height
    width = (x2 - x1) / img_width
    height = (y2 - y1) / img_height
    return center_x, center_y, width, height

# Loop through each category folder (1 to 256)
for category_id in range(1, 257):  
    category_folder = os.path.join(dataset_path, str(category_id))
    bb_file = os.path.join(category_folder, "bb_info.txt")

    if not os.path.exists(bb_file):
        continue  # Skip if no bounding box file

    # Create a subfolder in 'labels/' for this food category
    category_labels_folder = os.path.join(labels_root, str(category_id))
    os.makedirs(category_labels_folder, exist_ok=True)

    with open(bb_file, "r") as file:
        lines = file.readlines()[1:]  # ✅ Skip header line

    for line in lines:
        data = line.strip().split()
        if len(data) != 5:
            continue  # Skip invalid lines

        img_name, x1, y1, x2, y2 = data
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

        img_file = os.path.join(category_folder, f"{img_name}.jpg")
        if not os.path.exists(img_file):
            continue  # Skip if image not found

        # Get image dimensions
        img = Image.open(img_file)
        img_width, img_height = img.size

        # Convert to YOLO format
        center_x, center_y, width, height = convert_to_yolo(x1, y1, x2, y2, img_width, img_height)

        # Save YOLO label file in the corresponding category subfolder
        yolo_label_path = os.path.join(category_labels_folder, f"{img_name}.txt")
        with open(yolo_label_path, "w") as yolo_file:
            yolo_file.write(f"{category_id-1} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n")

print("✅ Conversion completed! YOLO labels are saved in /kaggle/working/labels")
