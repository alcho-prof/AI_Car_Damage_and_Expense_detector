# AutoDamage AI — Vehicle Damage Assessment Platform

An end-to-end computer vision platform that unifies vehicle damage localization, severity grading, and repair cost estimation into a single interactive web application.

---

## 🏗️ Architecture Overview

This project synthesizes and extends three foundational automotive computer vision repositories:

1. **`repo1_sahilkhan` (Accident Damage Detection & Cost Estimation)**:
   - Parts catalog and baseline replacement/repair costs across major automobile manufacturers and models.
2. **`repo2_thehrsr` (Damage Type & Component Localization)**:
   - Deep learning damage detection (YOLOv8) with bounding boxes and defect morphology (dent, scratch, shatter, dislocation).
3. **`repo3_tilakd` (Damage Severity & Classification)**:
   - Multi-gate assessment system for vehicle drivability, impact zone diagnostics, and structural risk.

---

## 📁 Repository Structure

```
PoC/
├── unified_car_damage_app/           # Standalone production web application
│   ├── app.py                        # Flask backend & REST API endpoints
│   ├── engine.py                     # AI damage detection & multi-gate synthesis
│   ├── pricing_data.py               # Vehicle brand parts matrix & currency rates
│   ├── models/
│   │   └── best.pt                   # Trained YOLOv8 vehicle damage weights
│   ├── static/
│   │   ├── css/style.css             # Modern dark-mode styling with glassmorphism
│   │   ├── js/app.js                 # Interactive UI, bounding boxes & filters
│   │   └── samples/                  # Preloaded 1-click test crash samples
│   ├── templates/
│   │   └── index.html                # Main application interface
│   ├── start.sh                      # Quick launch script
│   └── README.md
│
├── datasets/                         # Vehicle damage datasets & download scripts
│   ├── download_datasets.py          # Automated Hugging Face dataset downloader
│   ├── car_parts_and_damage_dataset/ # Component & defect annotations (meta.json)
│   └── README.md                     # Dataset documentation & class schemas
│
└── car_damage_analysis/              # Reference benchmark repositories
    ├── repo1_sahilkhan/              # Parts pricing & database schema
    ├── repo2_thehrsr/                # Damage segmentation & localization
    └── repo3_tilakd/                 # Multi-gate severity classification
```

---

## 🚀 Getting Started

### 1. Launch the Web Application
```bash
cd unified_car_damage_app
./start.sh
```
Or run with Python:
```bash
./venv/bin/python app.py
```
Then visit **`http://localhost:5001`** in your browser.

### 2. Download Training / Testing Datasets
To fetch the 2,300+ image vehicle damage dataset (`SaiVaibhavS/comprehensive-car-damage`):
```bash
cd datasets
python3 download_datasets.py
```

---

## 🎯 Features

- **No-Login Frictionless Workflow**: Upload any car photo via drag-and-drop or select one of the built-in crash demo presets.
- **Selective Output Display Filters**:
  - **Crash Bounding Box**: Interactive bounding boxes with confidence scores.
  - **Damage Severity**: 3-level severity grading (*Minor*, *Moderate*, *Severe*), animated severity index gauge, impact location, and tow/drivability status.
  - **Cost Detection**: Manufacturer-specific parts pricing, severity multipliers, labor, paint, taxes, and insurance deductible calculation.
  - **Filter Controls**: Dedicated toggle cards and quick-view buttons (*"All Outputs"*, *"Only Bounding Box"*, *"Only Severity"*, *"Only Cost Detection"*).
- **Multi-Brand & Multi-Currency**: Dynamic support for Toyota, Honda, Hyundai, Maruti Suzuki, Ford, BMW, and live currency conversion (USD, INR, EUR, GBP).
