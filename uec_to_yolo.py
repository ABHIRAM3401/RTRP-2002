import os

# Define paths
dataset_path = "path/to/uec_food_256"  # Change this to your dataset path
output_labels_path = "path/to/uec_food_256/labels"  # Where YOLO labels will be saved

# Create labels directory if it doesn't exist
os.makedirs(output_labels_path, exist_ok=True)

# Function to convert bounding box to YOLO format
def convert_to_yolo(x1, y1, x2, y2, img_width, img_height):
    center_x = (x1 + x2) / 2 / img_width
    center_y = (y1 + y2) / 2 / img_height
    width = (x2 - x1) / img_width
    height = (y2 - y1) / img_height
    return center_x, center_y, width, height

# Loop through each category folder
for category_id in range(1, 257):  # Assuming 256 categories (1 to 256)
    category_folder = os.path.join(dataset_path, str(category_id))
    bb_file = os.path.join(category_folder, "bb_info.txt")

    if not os.path.exists(bb_file):
        continue  # Skip if no bounding box file found

    with open(bb_file, "r") as file:
        lines = file.readlines()

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
        from PIL import Image
        img = Image.open(img_file)
        img_width, img_height = img.size

        # Convert to YOLO format
        center_x, center_y, width, height = convert_to_yolo(x1, y1, x2, y2, img_width, img_height)

        # Save YOLO label file
        yolo_label_path = os.path.join(output_labels_path, f"{img_name}.txt")
        with open(yolo_label_path, "w") as yolo_file:
            yolo_file.write(f"{category_id-1} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n")

print("Conversion completed! YOLO labels saved in:", output_labels_path)
