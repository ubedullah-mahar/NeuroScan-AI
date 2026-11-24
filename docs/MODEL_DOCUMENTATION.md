# Model documentation

This document describes the committed inference code, model metadata, and relevant notebook experiments. Classification and segmentation are separate pipelines with different inputs, artifacts, and outputs.

## Classification pipeline

### Feature extraction

`src/classification/inference.py` loads `efficientnet_b0` using `EfficientNet_B0_Weights.DEFAULT`. It replaces the final classifier with `torch.nn.Identity`, switches the network to evaluation mode, and returns the weight-provided image transform.

For each image, the inference code:

1. Converts the PIL image to RGB.
2. Applies the torchvision transform and adds a batch dimension.
3. Runs EfficientNet-B0 with gradients disabled.
4. Removes the batch dimension and reshapes features to `(1, -1)`.

The classification experiment metadata records a **1,280-dimensional** feature vector. The pretrained torchvision weights may need to be available in the local cache or fetched by torchvision when the extractor is initialized.

### Scaler and SVM

The experiment metadata describes an RBF-kernel SVM preceded by `StandardScaler`, with `C=10` and `gamma="scale"`. The cleaned experiment's serialized artifact is `models/best_svm_pipeline.joblib`. Its metadata identifies the scaler and classifier pipeline.

The original-data experiment is represented by `models/best_svm_full_5000.joblib`. The inference function defaults to this path. The UI currently invokes that default, so it uses the original-data artifact rather than automatically using the primary cleaned-data artifact.

### Classes and outputs

`CLASS_NAMES` maps the classifier's integer output as follows:

| Index | Label |
|---:|---|
| 0 | `glioma` |
| 1 | `meningioma` |
| 2 | `no_tumor` |
| 3 | `pituitary` |

`predict_classification()` returns:

- `predicted_class`: integer class index.
- `predicted_label`: mapped class name.
- `decision_scores`: the classifier's raw `decision_function` output.
- `features`: the extracted feature array.

The inference function does not return calibrated confidence or class probabilities. Do not convert or label raw decision scores as confidence without a separately validated calibration method.

### Classification metadata and performance

| Metadata file | Experiment | Training samples | Test samples | Test accuracy | Artifact |
|---|---|---:|---:|---:|---|
| `models/metadata/cleaned_experiment.json` | Cleaned training data; primary reported experiment | 3,891 | 1,000 | 0.88 | `best_svm_pipeline.joblib` |
| `models/metadata/full_dataset_experiment.json` | Original training data; supplementary experiment | 5,000 | 1,000 | 0.97 | `best_svm_full_5000.joblib` |

The dataset audit found 101 exact duplicate images in the original test split that also occur in the training split, across 98 cross-split duplicate groups. The 97% result is potentially affected by leakage. The 88% cleaned-training result is the primary reported classification result, not a clinical-performance claim.

## Segmentation pipeline

### U-Net architecture

`src/segmentation/unet_model.py` defines `UNet(in_channels=1, out_channels=1, base_channels=64)`.

- Encoder stages use two 3 × 3 convolution, batch-normalization, and ReLU sequences, with max-pooling between stages. Channel widths are 64, 128, 256, and 512.
- The bottleneck uses 1,024 channels.
- The decoder uses transposed convolutions for upsampling, concatenates matching encoder features as skip connections, and applies double-convolution blocks.
- A final 1 × 1 convolution emits one output channel.

These are details of the current source architecture, not a claim about segmentation accuracy.

### Input preprocessing

`preprocess_image()` accepts a path or a file-like object supported by Pillow. It:

1. Opens the image and converts it to grayscale (`L`).
2. Uses `ImageOps.contain` with bilinear resampling to fit within 256 × 256 while preserving aspect ratio.
3. Centers the resized image on a 256 × 256 black canvas.
4. Converts pixels to `float32`, divides by 255, adds the channel dimension, and returns a batched PyTorch tensor.

The resulting tensor has one grayscale input channel. The inference preprocessing is implemented in the source module; dataset-level preprocessing scripts in the notebooks are experimental and may write separate processed datasets.

### Model loading and prediction

`load_segmentation_model()` defaults to `models/segmentation/best_unet.pth`, chooses CUDA when available and CPU otherwise, creates a `UNet`, loads `checkpoint["model_state_dict"]`, and sets evaluation mode. The expected checkpoint file is not present in the repository.

`predict_segmentation(model, image_tensor, device)` moves the input tensor to the selected device and performs inference without gradients:

1. Run the U-Net to produce logits.
2. Apply sigmoid to produce a per-pixel probability map.
3. Threshold at `0.5` to produce a float-valued binary mask.
4. Return the preprocessed grayscale image, probabilities, and mask as NumPy arrays.

The inference API does not accept a ground-truth mask and does not compute Dice, IoU, precision, or recall.

### Notebook-only segmentation experiment

The training notebook contains a separate experimental training workflow: it uses an 80/20 random split of the training portion for training and validation, with a seeded generator, and keeps a separate test dataset. The test-evaluation notebook contains saved output reporting test loss `0.0889`, Dice `0.8478`, IoU `0.7762`, precision `0.8925`, and recall `0.8666`.

These are historical notebook outputs, not metrics returned by the inference API or a committed model-metadata file. The required checkpoint is absent, so these results cannot be reproduced from the repository alone. Treat them as notebook-reported experimental values, not independently verified or clinical evidence.

## Experimental notebook work versus implemented inference

The notebooks include additional dataset cleaning, feature extraction, model comparison, training, and evaluation experiments. In particular, notebook comparisons include alternatives such as ResNet50, Random Forest, and XGBoost. Those experimental approaches are not the deployed classification inference path, which uses EfficientNet-B0 features and a serialized SVM. U-Net training is in a notebook; the reusable runtime path is the architecture and inference code under `src/segmentation/`.
