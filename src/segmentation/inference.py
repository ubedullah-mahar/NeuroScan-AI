import numpy as np
import torch
from PIL import Image, ImageOps

from src.segmentation.unet_model import UNet


TARGET_SIZE = (256, 256)


def preprocess_image(image_path):
    image = Image.open(image_path).convert("L")

    resized = ImageOps.contain(
        image,
        TARGET_SIZE,
        method=Image.Resampling.BILINEAR
    )

    canvas = Image.new("L", TARGET_SIZE, 0)

    x_offset = (TARGET_SIZE[0] - resized.width) // 2
    y_offset = (TARGET_SIZE[1] - resized.height) // 2

    canvas.paste(resized, (x_offset, y_offset))

    image_array = np.asarray(
        canvas,
        dtype=np.float32
    ) / 255.0

    image_array = image_array[..., np.newaxis]

    image_tensor = torch.from_numpy(
        image_array
    ).permute(2, 0, 1).unsqueeze(0)

    return image_tensor


def load_segmentation_model(
    checkpoint_path="models/segmentation/best_unet.pth"
):
    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    model = UNet().to(device)

    checkpoint = torch.load(
        checkpoint_path,
        map_location=device,
        weights_only=False
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model.eval()

    return model, device


def predict_segmentation(model, image_tensor, device):
    image_tensor = image_tensor.to(device)

    with torch.no_grad():
        logits = model(image_tensor)

        probabilities = torch.sigmoid(logits)

        predicted_mask = (
            probabilities >= 0.5
        ).float()

    image = image_tensor.squeeze().cpu().numpy()

    probabilities = probabilities.squeeze().cpu().numpy()

    predicted_mask = predicted_mask.squeeze().cpu().numpy()

    return image, probabilities, predicted_mask