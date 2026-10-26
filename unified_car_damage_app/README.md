# AutoDamage AI — Unified Vehicle Damage Assessment System

A unified application integrating the best features from three vehicle damage detection repositories:
- **Repo 1 (`sahilkhan-7/accident-damage-detection`)**: Vehicle parts repair & replacement pricing catalog by brand and model.
- **Repo 2 (`thehrsr/CAR-DAMAGE-DETECTION`)**: YOLOv8 deep learning damage detection, part bounding box localization, and visual annotations.
- **Repo 3 (`TilakD/Car-Damage-Analysis-App`)**: Multi-gate damage severity grading, structural integrity assessment, impact zone mapping, and drivability diagnostics.

---

## Key Features

1. **No Authentication / Direct Upload**:
   - Clean, frictionless interface with no login or credentials required.
   - Drag-and-drop or file browser upload for damaged vehicle images (PNG, JPG, WEBP).
   - Pre-loaded one-click demo crashes (*Front Collision*, *Side Impact*) for rapid testing.

2. **Customizable Output Display (User-Controlled Filtering)**:
   - **Crash Bounding Box**: Damaged car components highlighted with interactive bounding boxes and confidence scores.
   - **Damage Severity**: 3-tier severity classification (*Minor*, *Moderate*, *Severe*) with severity score gauge, primary impact zone, structural risk, and tow/drivability status.
   - **Cost Detection**: Vehicle make/model-specific OEM part pricing, severity-scaled repair costs, labor rates, paint materials, tax estimates, and insurance deductible calculations.
   - **Display Toggles**: Easily view only selected outputs (*"Only Bounding Box"*, *"Only Severity"*, *"Only Cost Detection"*, or any custom combination).

3. **Multi-Currency & Multi-Brand Catalog**:
   - Supports Toyota, Honda, Hyundai, Maruti Suzuki, Ford, BMW, and Generic Vehicles.
   - Live currency conversion (USD, INR, EUR, GBP).

---

## Directory Structure

```
unified_car_damage_app/
├── app.py                  # Flask web backend and REST API endpoints
├── engine.py               # AI damage detection & multi-gate synthesis engine
├── pricing_data.py         # Vehicle brand parts pricing matrix & labor rates
├── models/
│   └── best.pt             # Trained YOLOv8 vehicle damage detection weights
├── data/
│   └── car_parts_prices.json
├── static/
│   ├── css/style.css       # Modern dark-mode styling with glassmorphism
│   ├── js/app.js           # Interactive UI, canvas bounding boxes & filters
│   ├── samples/            # Sample crash test images
│   └── uploads/            # Uploaded & annotated result images
├── templates/
│   └── index.html          # Main application interface
├── venv/                   # Python 3.10 virtual environment
├── start.sh                # Convenience launch script
└── README.md
```

---

## Quick Start

### 1. Launch the Server
From the project root:
```bash
cd /Users/sndyy/PoC/unified_car_damage_app
./start.sh
```
Or run directly using the virtual environment:
```bash
./venv/bin/python app.py
```

### 2. Access the Application
Open your web browser and navigate to:
```
http://localhost:5001
```

---

## API Endpoints

- `GET /api/brands`: Returns list of available automotive brands, models, and supported currencies.
- `GET /api/samples`: Returns pre-configured demo crash images.
- `POST /api/analyze`: Multipart form upload accepting `image` (file) or `sample_name` (string), `brand`, `model`, and `currency`. Returns full JSON report containing detections, severity metrics, and itemized cost quote.
