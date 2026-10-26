import os
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

import engine
from pricing_data import CAR_PARTS_PRICES, CURRENCY_RATES

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = "car-damage-unified-secret-key-2026"
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024  # 32MB max upload
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
SAMPLES_FOLDER = os.path.join(BASE_DIR, "static", "samples")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SAMPLES_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/brands", methods=["GET"])
def get_brands():
    """Returns available vehicle brands and their corresponding models."""
    catalog = {}
    for brand, models in CAR_PARTS_PRICES.items():
        catalog[brand] = list(models.keys())
    return jsonify({
        "brands": catalog,
        "currencies": list(CURRENCY_RATES.keys())
    })

@app.route("/api/samples", methods=["GET"])
def get_samples():
    """Returns preset test images for 1-click evaluation from the downloaded dataset."""
    samples = [
        {
            "id": "front_crash",
            "name": "Front Collision (Severe Bumper & Hood)",
            "filename": "sample_front_collision.jpg",
            "url": "/static/samples/sample_front_collision.jpg",
            "default_brand": "TOYOTA",
            "default_model": "Camry"
        },
        {
            "id": "front_breakage",
            "name": "Front Breakage & Light (Moderate)",
            "filename": "sample_front_breakage.jpg",
            "url": "/static/samples/sample_front_breakage.jpg",
            "default_brand": "HONDA",
            "default_model": "Civic"
        },
        {
            "id": "rear_crush",
            "name": "Rear End Crushed (Dickey & Bumper)",
            "filename": "sample_rear_crush.jpg",
            "url": "/static/samples/sample_rear_crush.jpg",
            "default_brand": "HYUNDAI",
            "default_model": "Creta"
        },
        {
            "id": "rear_breakage",
            "name": "Rear Bumper Breakage (Minor)",
            "filename": "sample_rear_breakage.jpg",
            "url": "/static/samples/sample_rear_breakage.jpg",
            "default_brand": "MARUTI SUZUKI",
            "default_model": "Swift"
        },
        {
            "id": "side_impact",
            "name": "Side Impact (Door & Fender Crush)",
            "filename": "sample_side_impact.jpg",
            "url": "/static/samples/sample_side_impact.jpg",
            "default_brand": "TOYOTA",
            "default_model": "RAV4"
        },
        {
            "id": "clean_undamaged",
            "name": "Undamaged Baseline (Clean Car)",
            "filename": "sample_clean_undamaged.jpg",
            "url": "/static/samples/sample_clean_undamaged.jpg",
            "default_brand": "BMW",
            "default_model": "3 Series"
        }
    ]
    return jsonify({"samples": samples})

@app.route("/api/analyze", methods=["POST"])
def analyze():
    brand = request.form.get("brand", "HONDA")
    car_model = request.form.get("model", "City")
    currency = request.form.get("currency", "USD")
    sample_name = request.form.get("sample_name", "")

    saved_filepath = None
    target_image_url = None

    if sample_name:
        sample_path = os.path.join(SAMPLES_FOLDER, secure_filename(sample_name))
        if os.path.exists(sample_path):
            saved_filepath = sample_path
            target_image_url = f"/static/samples/{secure_filename(sample_name)}"

    if not saved_filepath:
        if "image" not in request.files:
            return jsonify({"error": "No image file provided."}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No selected file."}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Please upload a PNG, JPG, or WEBP image."}), 400

        unique_id = uuid.uuid4().hex[:10]
        filename = f"{unique_id}_{secure_filename(file.filename)}"
        saved_filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(saved_filepath)
        target_image_url = f"/static/uploads/{filename}"

    try:
        results = engine.analyze_car_damage(
            image_path=saved_filepath,
            brand=brand,
            model_name=car_model,
            currency=currency
        )
        results["image_metadata"]["original_url"] = target_image_url
        return jsonify(results)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
