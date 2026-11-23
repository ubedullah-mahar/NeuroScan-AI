from PIL import Image

from src.classification.inference import (
    load_feature_extractor,
    load_classifier,
    predict_classification,
)


IMAGE_PATH = r"D:\brain tumour\brisc2025\segmentation_task\test\images\brisc2025_test_00001_gl_ax_t1.jpg"


# Load MRI image
image = Image.open(IMAGE_PATH)

# Load EfficientNet feature extractor
feature_extractor, transform = load_feature_extractor()

# Load trained SVM classifier
classifier = load_classifier()

# Predict tumor class
result = predict_classification(
    image,
    feature_extractor,
    transform,
    classifier
)

# Display results
print("Predicted class:", result["predicted_class"])
print("Predicted label:", result["predicted_label"])
print("Feature vector shape:", result["features"].shape)
print("Decision scores:", result["decision_scores"])