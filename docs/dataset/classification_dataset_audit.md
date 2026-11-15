# BRISC2025 Classification Dataset — Audit Report

**Project:** NeuroScan-AI  
**Task:** Brain MRI Classification  
**Dataset:** BRISC2025  
**Audit status:** Preliminary investigation  
**Notebook:** `notebooks/exploratory/01_classification_dataset_audit.ipynb`

---

## 1. Objective

This report documents the exploratory data analysis and initial quality investigation performed on the BRISC2025 classification dataset.

The objectives are to:

- Understand the dataset structure and class distribution.
- Examine image dimensions, formats and pixel characteristics.
- Investigate RGB and grayscale image representation.
- Identify exact duplicate images.
- Investigate potential cross-split duplication.
- Identify near-duplicate candidates using perceptual hashing.
- Establish a foundation for a reproducible preprocessing and evaluation pipeline.

## 2. Dataset Overview

The classification dataset contains four categories:

1. Glioma
2. Meningioma
3. No tumor
4. Pituitary

The initial inventory identified 6,000 images.

| Split | Image count |
|---|---:|
| Training | 5,000 |
| Testing | 1,000 |
| **Total** | **6,000** |

### 2.1 Class distribution

| Class | Training | Testing |
|---|---:|---:|
| Glioma | 1,147 | 254 |
| Meningioma | 1,329 | 306 |
| No tumor | 1,067 | 140 |
| Pituitary | 1,457 | 300 |
| **Total** | **5,000** | **1,000** |

The class distribution is not uniform, particularly in the official testing split.

Consequently, future model evaluation should include macro-averaged metrics and per-class performance rather than relying exclusively on accuracy.

## 3. Image Properties

### 3.1 Image dimensions

The audit identified 183 distinct image dimension combinations.

The most frequent dimensions were:

| Dimensions | Image count |
|---|---:|
| 512 × 512 | 4,881 |
| 369 × 369 | 363 |
| 216 × 369 | 354 |
| 256 × 256 | 32 |

The variation in image dimensions indicates that a consistent input-resolution strategy will be required for model training.

### 3.2 Image formats and modes

All 6,000 inspected images were JPEG files.

The image modes were:

| Mode | Image count |
|---|---:|
| RGB | 3,134 |
| Grayscale (L) | 2,866 |

No corrupted images were detected during the initial image inspection.

### 3.3 RGB channel investigation

All 3,134 RGB images were examined by comparing their red, green and blue channel values.

The mean absolute differences between the channels were zero for all four classes.

This indicates that the inspected RGB images contain identical channel values and are grayscale-equivalent images stored in RGB format.

This finding supports evaluating a standardized grayscale input representation during preprocessing.

## 4. Pixel Intensity Investigation

A sample of 50 training images per class was used for preliminary intensity analysis.

| Class | Mean intensity | Mean standard deviation |
|---|---:|---:|
| Glioma | 31.92 | 37.02 |
| Meningioma | 41.65 | 44.84 |
| No tumor | 53.41 | 55.31 |
| Pituitary | 50.78 | 41.68 |

These statistics describe the sampled images rather than the entire dataset.

The observed intensity distributions overlap, so pixel intensity alone should not be assumed to provide reliable class discrimination.

## 5. Exact Duplicate Investigation

Exact duplicate detection was performed using SHA-256 hashes calculated from grayscale image content, including image dimensions.

The audit identified:

| Finding | Count |
|---|---:|
| Total image files | 6,000 |
| Unique image hashes | 5,856 |
| Exact duplicate groups | 134 |
| Files belonging to duplicate groups | 278 |
| Cross-split duplicate groups | 98 |
| Test images affected by cross-split duplication | 101 |
| Duplicate groups with conflicting class labels | 0 |

The 98 cross-split groups indicate that identical image content appears in both the official training and testing directories.

This creates a potential image-level data leakage concern.

The affected test images represent 10.1% of the official testing set.

The effect of this duplication on model performance has not yet been measured because classification models have not been trained.

## 6. Near-Duplicate Investigation

Perceptual hashing (pHash) was used to identify visually similar image pairs across the official training and testing splits.

The initial candidate threshold was a Hamming distance of four or less, excluding zero-distance matches already covered by the exact-hash investigation.

| Hamming distance | Candidate pairs |
|---|---:|
| 2 | 85 |
| 4 | 227 |
| **Total** | **312** |

The candidate pairs were distributed across several class combinations, with most occurring within the same class.

Five candidate pairs with a Hamming distance of two were visually inspected.

These observations were not sufficient to confirm that the images originated from the same MRI scans.

Therefore, the 312 pairs are classified as near-duplicate candidates, not confirmed near-duplicates.

Further verification is required.

## 7. Preliminary Findings and Implications

The initial audit identifies several considerations for future experiments:

1. Class distributions differ between training and testing splits.
2. Image dimensions are heterogeneous.
3. RGB images are grayscale-equivalent.
4. Exact image duplication occurs across the official train/test boundary.
5. Perceptual hashing identifies additional candidate pairs requiring verification.
6. Patient-level independence cannot be established from the current investigation.

These findings should inform preprocessing, dataset validation and evaluation design.

## 8. Limitations

This audit has several limitations:

- Intensity statistics were calculated from a sample of 200 training images.
- Perceptual hashing is a candidate-generation method and does not establish duplicate identity.
- Only five near-duplicate candidate pairs were visually inspected.
- Exact image duplication does not establish patient-level overlap.
- No model training or performance evaluation has been conducted.
- No conclusions about clinical diagnostic performance can be drawn.

## 9. Next Steps

The planned work includes:

1. Further verification of near-duplicate candidates.
2. Investigation of MRI view distributions and dataset consistency.
3. Segmentation dataset audit.
4. Design of classification and segmentation preprocessing strategies.
5. Development of reusable data-loading and validation modules.
6. Construction of documented evaluation protocols.

---

**Report status:** Preliminary — subject to revision as additional investigations are completed.

**Associated experimental notebook:** `notebooks/exploratory/01_classification_dataset_audit.ipynb`