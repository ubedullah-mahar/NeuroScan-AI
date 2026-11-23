import matplotlib.pyplot as plt
import numpy as np

from src.segmentation.inference import (
    preprocess_image,
    load_segmentation_model,
    predict_segmentation
)


IMAGE_PATH = r"D:\brain tumour\brisc2025\segmentation_task\test\images\brisc2025_test_00001_gl_ax_t1.jpg"


# Load image and preprocess it
image_tensor = preprocess_image(IMAGE_PATH)

# Load trained U-Net model
model, device = load_segmentation_model()

# Generate prediction
image, probabilities, predicted_mask = predict_segmentation(
    model,
    image_tensor,
    device
)

# Display prediction information
print("Device:", device)
print("Image shape:", image.shape)
print("Mask shape:", predicted_mask.shape)
print("Predicted tumor pixels:", int(predicted_mask.sum()))
print("Tumor percentage:", round(predicted_mask.mean() * 100, 2), "%")

# Create visualization
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(image, cmap="gray")
axes[0].set_title("Original MRI")
axes[0].axis("off")

axes[1].imshow(predicted_mask, cmap="gray")
axes[1].set_title("Predicted Tumor Mask")
axes[1].axis("off")

axes[2].imshow(image, cmap="gray")
axes[2].imshow(
    predicted_mask,
    cmap="Reds",
    alpha=0.4
)
axes[2].set_title("MRI + Tumor Overlay")
axes[2].axis("off")

plt.tight_layout()
plt.show()