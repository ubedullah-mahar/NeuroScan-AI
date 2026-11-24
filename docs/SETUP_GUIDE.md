# Setup and supervisor handover guide

This guide covers the current repository state. It does not install dependencies or provide missing datasets/checkpoints; those must be supplied by the project owner.

## Prerequisites

- Python version compatible with the selected PyTorch and Torchvision releases.
- Git and a working copy of the repository.
- A CPU-compatible PyTorch/Torchvision pair, or a matching CUDA-enabled pair and compatible NVIDIA driver if GPU use is intended.
- The required model artifacts listed below.
- Dataset access only if running notebook research; datasets are not included in this repository.

Check the official [PyTorch local installation selector](https://pytorch.org/get-started/locally/) for a compatible install command. Do not choose PyTorch and Torchvision versions independently.

## Create an environment

From the repository root:

```shell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```shell
source .venv/bin/activate
```

Install a compatible PyTorch/Torchvision build first if a specific CUDA or CPU wheel is required, then install the declared packages:

```shell
python -m pip install -r requirements.txt
```

`requirements.txt` groups application/runtime packages separately from optional research and development packages. To avoid optional tools, install only the runtime entries in the first section.

Runtime-only installation:

```shell
python -m pip install streamlit torch torchvision numpy Pillow joblib scikit-learn
```

Optional research and development packages are `pytest`, `pandas`, `matplotlib`, `ImageHash`, `seaborn`, `tqdm`, and `xgboost`. Install those only when the corresponding notebooks or tooling are needed.

## Required model artifacts

| Artifact | Status | Used by |
|---|---|---|
| `models/best_svm_full_5000.joblib` | Present | Default classification inference artifact. |
| `models/best_svm_pipeline.joblib` | Present | Cleaned-training classification experiment. |
| `models/segmentation/best_unet.pth` | **Missing** | Required by `load_segmentation_model()`; must be supplied separately. |
| Torchvision EfficientNet-B0 default weights | Not stored in this repository | `load_feature_extractor()` may need a local cache or network access on first use. |

The expected segmentation checkpoint path is relative to the process working directory and is ignored by `.gitignore`. Confirm that the checkpoint is from the matching U-Net architecture and includes the `model_state_dict` key before starting the segmentation workflow. Do not copy a notebook checkpoint into the expected path without verifying it is the intended model.

## Dataset requirements

No datasets are included in the repository. The classification audit describes BRISC2025 classification data under `classification_task/{train,test}`; segmentation notebooks use `segmentation_task/{train,test}/{images,masks}` and a derived `segmentation_processed_256` directory.

Several notebooks contain machine-specific Windows or Google Colab paths. Update those paths only as part of separate research work; the current Streamlit inference paths do not require the full dataset.

## Expected repository paths

```text
brain-tumor/
├── apps/
│   ├── app.py
│   └── ui_components.py
├── models/
│   ├── best_svm_full_5000.joblib
│   ├── best_svm_pipeline.joblib
│   └── segmentation/
│       └── best_unet.pth          # supply separately; absent from checkout
├── src/
│   ├── classification/inference.py
│   └── segmentation/
│       ├── inference.py
│       └── unet_model.py
├── docs/
└── requirements.txt
```

## Start the application

Run the command from the repository root so the `src` imports and relative model paths resolve:

```shell
streamlit run apps/app.py
```

The classification workflow loads the default full-dataset SVM artifact. The segmentation workflow will fail until the missing checkpoint is supplied. The UI caches loaded model resources for the Streamlit session.

## Common issues

| Symptom | Likely cause and action |
|---|---|
| `FileNotFoundError` for `models/segmentation/best_unet.pth` | The segmentation checkpoint is not in this checkout. Obtain the approved checkpoint and place it at the exact expected path. |
| `FileNotFoundError` for an SVM artifact | Start Streamlit from the repository root and confirm the `.joblib` file is present under `models/`. |
| `ModuleNotFoundError` for Streamlit, Pillow, Torch, or another declared package | Activate the intended virtual environment and install the requirements. Do not mix environments. |
| Torch/Torchvision import or CUDA errors | Reinstall a compatible pair for the selected Python, operating system, driver, and CUDA runtime using the official PyTorch selector. |
| Network/download error while creating EfficientNet-B0 | The torchvision default weights are not cached. Provide network access or pre-populate the approved cache. |
| `KeyError: 'model_state_dict'` while loading U-Net | The checkpoint format does not match the inference loader. Verify the approved checkpoint; do not change inference code as a workaround. |
| `ModuleNotFoundError: src...` or model path errors | Launch from the repository root rather than another working directory. |
| Notebook path not found | Notebook paths are tied to the original local/Colab environment. Obtain the dataset and update notebook configuration in a separate research change. |

The current `tests/test_*.py` files are top-level inference examples with hard-coded external image paths, not isolated assertion-based pytest tests. Pytest discovery may execute those scripts and attempt model inference. Do not treat `pytest` as a safe test suite until the tests are refactored by the maintainers.

## Handover checks

Before a demonstration, the supervisor should:

1. Obtain and validate the missing segmentation checkpoint.
2. Confirm which classification artifact should be used. The runtime default is the original-data artifact; the primary reported 88% result is associated with the cleaned artifact.
3. Confirm whether EfficientNet-B0 weights are cached or accessible.
4. Verify data/model licensing and access permissions independently.
5. Decide how large model artifacts should be distributed. The segmentation checkpoint is ignored by Git.

## Repository consistency notes

- The tracked `package-lock.json` has an empty `packages` object, and there is no `package.json` in the repository. No Node.js application dependency was identified in the inspected Python sources; confirm whether this lockfile is still needed.
- `.gitignore` excludes `.venv/`, `data/features/*.npz`, and the exact segmentation checkpoint path, but it does not provide a general ignore rule for raw MRI datasets. Keep datasets outside the checkout unless the maintainers establish an approved ignore/storage policy.
- `docs/dataset/classification_dataset_audit.md` points to `notebooks/exploratory/01_classification_dataset_audit.ipynb`, which is absent. The available classification audit notebook is `notebooks/classification/classification_dataset.ipynb`; see the [dataset documentation](DATASET_DOCUMENTATION.md).
