# Vehicle Damage Detection & Classification Datasets

This directory contains benchmark vehicle damage datasets downloaded for model training, validation, and evaluation in the AutoDamage AI platform.

---

## 1. Comprehensive Car Damage Dataset (`comprehensive_car_damage/`)

- **Source**: [`SaiVaibhavS/comprehensive-car-damage`](https://huggingface.co/datasets/SaiVaibhavS/comprehensive-car-damage)
- **License**: MIT
- **Total Images**: **2,300 high-resolution images**
- **Size**: ~669 MB
- **Format**: JPG / JPEG organized by severity & crash zone

### Class Breakdown:

| Category | Description | Image Count | Typical Severity |
| :--- | :--- | :--- | :--- |
| **`F_Crushed`** | Front view, heavy crushing & frame impact | 400 images | Severe |
| **`F_Breakage`** | Front view, broken headlights, grilles, bumpers | 500 images | Moderate |
| **`F_Normal`** | Front view, clean undamaged baseline vehicles | 500 images | None / Minor |
| **`R_Crushed`** | Rear view, crushed trunk, dickey & rear fender | 300 images | Severe |
| **`R_Breakage`** | Rear view, cracked tail lamps & bumper scuffs | 300 images | Moderate |
| **`R_Normal`** | Rear view, clean undamaged baseline vehicles | 300 images | None / Minor |

---

## 2. Car Parts and Damages Annotations (`car_parts_and_damage_dataset/`)

- **Source**: [`yusufnull/car-parts-and-damage-dataset`](https://huggingface.co/datasets/yusufnull/car-parts-and-damage-dataset)
- **License**: MIT
- **Contents**:
  - `meta.json`: Full polygon and mask metadata mapping car components and localized defects (dents, scratches, cracks).
  - `README.md`: Annotation specifications and taxonomy.

---

## 3. Dataset Downloader & Utility Scripts

- [`download_datasets.py`](file:///Users/sndyy/PoC/datasets/download_datasets.py):
  Python script using `huggingface_hub` to download datasets and export sample test images into `unified_car_damage_app/static/samples/`.

To re-run or update the dataset:
```bash
cd /Users/sndyy/PoC/datasets
/Users/sndyy/PoC/unified_car_damage_app/venv/bin/python download_datasets.py
```
