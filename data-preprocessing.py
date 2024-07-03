import os
import cv2
import json
import numpy as np
import matplotlib.pyplot as plt

def plot_mask_and_bboxes(image, mask, bbox3d):
    num_slices = mask.shape[0]
    cols = 5 if num_slices > 5 else num_slices
    rows = (num_slices + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(15, rows * 3))
    axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

    for slice_idx in range(num_slices):
        ax = axes[slice_idx]

        # Plot the image
        ax.imshow(image)

        # Overlay the mask
        mask_slice = mask[slice_idx]
        mask_resized = cv2.resize(mask_slice.astype(np.uint8), (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
        mask_overlay = np.zeros_like(image)
        mask_overlay[mask_resized == 1] = [255, 0, 0]  # Red mask
        ax.imshow(mask_overlay, alpha=0.5)

        for bbox in bbox3d:
            x_min, y_min, z_min = bbox[0]
            x_max, y_max, z_max = bbox[1]
            rect = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, linewidth=2, edgecolor='g', facecolor='none')
            ax.add_patch(rect)

        ax.set_title(f'Slice {slice_idx}')
        ax.axis('off')

    for idx in range(num_slices, len(axes)):
        axes[idx].axis('off')

    plt.subplots_adjust(wspace=0.1, hspace=0.1)
    plt.show()

main_path = os.listdir('dataset')

for sub in main_path:
    image = cv2.imread(os.path.join('dataset', sub, 'rgb.jpg'))
    mask = np.load(os.path.join('dataset', sub, 'mask.npy'))
    bbox3d = np.load(os.path.join('dataset', sub, 'bbox3d.npy'))

    plot_mask_and_bboxes(image, mask, bbox3d)
    
    
    
dataset_path = 'dataset'
output_json_path = 'coco/annotations/instances.json'
output_images_path = os.path.join('coco', 'images')

os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
os.makedirs(output_images_path, exist_ok=True)

coco_format = {
    "images": [],
    "annotations": [],
    "categories": [{"id": 1, "name": "object"}]
}

annotation_id = 1
image_id = 1

def convert_to_json_serializable(obj):
    if isinstance(obj, (np.integer, np.int64, np.uint64)):
        return int(obj)
    if isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

for subdir in os.listdir(dataset_path):
    subdir_path = os.path.join(dataset_path, subdir)
    if os.path.isdir(subdir_path):

        image_file = os.path.join(subdir_path, 'rgb.jpg')
        mask_file = os.path.join(subdir_path, 'mask.npy')

        image = cv2.imread(image_file)
        if image is None:
            print(f"Warning: Image {image_file} not found or cannot be loaded.")
            continue
        
        height, width, _ = image.shape

        output_image_file = os.path.join(output_images_path, f"{subdir}.jpg")
        cv2.imwrite(output_image_file, image)

        coco_format["images"].append({
            "id": image_id,
            "file_name": f"{subdir}.jpg",
            "height": height,
            "width": width
        })

        if not os.path.exists(mask_file):
            print(f"Warning: Mask file {mask_file} not found.")
            continue
        mask = np.load(mask_file)

        for slice_idx in range(mask.shape[0]):
            mask_slice = mask[slice_idx]
            mask_resized = cv2.resize(mask_slice.astype(np.uint8), (width, height), interpolation=cv2.INTER_NEAREST)

            contours, _ = cv2.findContours(mask_resized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            segmentation = []
            for contour in contours:
                if len(contour) > 4:  
                    contour = contour.flatten().tolist()
                    trimmed_contour = []
                    for i in range(0, len(contour), 2):
                        x = max(0, min(contour[i], width - 1))
                        y = max(0, min(contour[i + 1], height - 1))
                        trimmed_contour.extend([x, y])
                    if len(trimmed_contour) > 4:
                        segmentation.append(trimmed_contour)

            if len(segmentation) > 0:
                x_min = min(trimmed_contour[0::2])
                y_min = min(trimmed_contour[1::2])
                x_max = max(trimmed_contour[0::2])
                y_max = max(trimmed_contour[1::2])

                bbox = [x_min, y_min, x_max - x_min, y_max - y_min]
                area = int(np.sum(mask_resized))

                coco_format["annotations"].append({
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": 1,
                    "bbox": bbox,
                    "area": area,
                    "segmentation": segmentation,
                    "iscrowd": 0
                })
                annotation_id += 1

        image_id += 1

coco_format = json.loads(json.dumps(coco_format, default=convert_to_json_serializable))

with open(output_json_path, 'w') as json_file:
    json.dump(coco_format, json_file)

print("Dataset converted to COCO format successfully.")