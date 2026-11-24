# Dataset documentation

The datasets are not included in this repository. The documented inventory and audit findings below come from the committed audit report and notebook outputs; they describe the investigated BRISC2025 copies, not a guarantee about other dataset versions.

## Classification dataset

The classification audit identifies the following local organization:

```text
<BRISC2025 root>/
└── classification_task/
    ├── train/
    │   ├── glioma/
    │   ├── meningioma/
    │   ├── no_tumor/
    │   └── pituitary/
    └── test/
        ├── glioma/
        ├── meningioma/
        ├── no_tumor/
        └── pituitary/
```

The reported audit inventory is 5,000 training images and 1,000 test images:

| Class | Training | Testing |
|---|---:|---:|
| Glioma | 1,147 | 254 |
| Meningioma | 1,329 | 306 |
| No tumor | 1,067 | 140 |
| Pituitary | 1,457 | 300 |
| **Total** | **5,000** | **1,000** |

The audit reports JPEG files, with 3,134 RGB-mode and 2,866 grayscale-mode images. It found RGB images to be grayscale-equivalent by channel comparison. Image dimensions varied; the audit reports 183 distinct dimension combinations. These observations apply to the inspected dataset copy.

The classification notebooks create an internal stratified 80/20 training/validation split with `random_state=42` and keep the named test directory separate. The experiment metadata separately records 3,891 training samples for the cleaned experiment and 5,000 for the original-data experiment; do not infer a different held-out test split from these notebook validation steps.

## Classification cleaning and duplicate audit

The audit report at [`dataset/classification_dataset_audit.md`](dataset/classification_dataset_audit.md) records:

- 6,000 total files and 5,856 unique grayscale-content hashes.
- 134 exact-duplicate groups, covering 278 files.
- 98 exact-duplicate groups spanning training and test splits.
- 101 affected test images in those cross-split groups.
- No duplicate groups with conflicting class labels.
- 312 additional perceptual-hash candidates; these were not confirmed duplicates.

The 101 cross-split duplicate test images create a potential data leakage concern for evaluation on the original split. The audit reports that the cleaned classification experiment used 3,891 training samples and the same 1,000-sample test count; its metadata records 88% test accuracy. The supplementary experiment used 5,000 training samples and records 97%. See the experiment metadata for the reported results and [Model documentation](MODEL_DOCUMENTATION.md) for artifact/runtime caveats.

The audit report says its associated notebook is `notebooks/exploratory/01_classification_dataset_audit.ipynb`, but that path is not present in the current repository. The available classification dataset notebook is `notebooks/classification/classification_dataset.ipynb`.

## Segmentation dataset workflow

The segmentation audit notebook expects the following BRISC2025 layout:

```text
<BRISC2025 root>/
└── segmentation_task/
    ├── train/
    │   ├── images/
    │   └── masks/
    └── test/
        ├── images/
        └── masks/
```

A saved output in `notebooks/segmentation/segmentation_dataset_audit.ipynb` reports 3,933 training images and masks, and 860 test images and masks. The notebook checks matching image/mask stems. Those counts refer to the dataset copy examined in that notebook.

`notebooks/segmentation/segmentation_preprocessing.ipynb` describes a processed output directory named `segmentation_processed_256`, converts images and masks to grayscale, resizes and pads them to 256 × 256, and binarizes masks with a threshold of 128. The training notebook uses the processed data, creates a seeded 80/20 training/validation split from the training portion, and retains the separate test portion.

These are notebook workflows, not a repository-provided dataset loader. The inference module separately preprocesses a single uploaded image and does not require the original dataset directory.

## Data access and limitations

- No image dataset or data download script is tracked in this repository.
- The notebooks use environment-specific paths, including `D:\brain tumour\brisc2025` and Google Colab Drive paths. They must be configured for the authorized local dataset copy before use.
- Dataset provenance, redistribution rights, patient-level independence, and clinical suitability are not established by this repository.
- Exact image de-duplication does not establish patient-level disjointness.
- Do not infer missing dataset attributes, demographics, patient grouping, or external validation from filenames or notebook examples.
