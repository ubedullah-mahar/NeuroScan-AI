import joblib
import torch
import torch.nn as nn
from PIL import Image
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights


CLASS_NAMES = {
    0: "glioma",
    1: "meningioma",
    2: "no_tumor",
    3: "pituitary",
}


def load_feature_extractor():
    weights = EfficientNet_B0_Weights.DEFAULT

    model = efficientnet_b0(weights=weights)

    model.classifier = nn.Identity()

    model.eval()

    transform = weights.transforms()

    return model, transform


def load_classifier(
    model_path="models/best_svm_full_5000.joblib"
):
    classifier = joblib.load(model_path)

    return classifier


def extract_features(image, model, transform):
    image = image.convert("RGB")

    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        features = model(image_tensor)

    features = features.squeeze(0).cpu().numpy()

    return features.reshape(1, -1)


def predict_classification(
    image,
    feature_extractor,
    transform,
    classifier
):
    features = extract_features(
        image,
        feature_extractor,
        transform
    )

    predicted_class = classifier.predict(features)[0]

    predicted_label = CLASS_NAMES[int(predicted_class)]

    decision_scores = classifier.decision_function(features)

    return {
        "predicted_class": int(predicted_class),
        "predicted_label": predicted_label,
        "decision_scores": decision_scores,
        "features": features,
    }