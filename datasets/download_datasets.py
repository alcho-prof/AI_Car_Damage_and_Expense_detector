#!/usr/bin/env python3
"""
Car Damage Dataset Downloader
Downloads open-source vehicle damage datasets from Hugging Face Hub:
1. SaiVaibhavS/comprehensive-car-damage (~637 MB, 2,300 images across 6 categories: F_Crushed, F_Breakage, F_Normal, R_Crushed, R_Breakage, R_Normal)
2. yusufnull/car-parts-and-damage-dataset annotations (meta.json) and damage samples
"""

import os
import sys
import shutil
from huggingface_hub import snapshot_download, hf_hub_download

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def download_comprehensive_damage_dataset():
    target_dir = os.path.join(BASE_DIR, "comprehensive_car_damage")
    print(f"\n[1/3] Downloading 'SaiVaibhavS/comprehensive-car-damage' into {target_dir}...")
    
    snapshot_download(
        repo_id="SaiVaibhavS/comprehensive-car-damage",
        repo_type="dataset",
        local_dir=target_dir,
        max_workers=8
    )
    print("Download completed successfully!")

    # Summary of downloaded classes
    categories = ["F_Crushed", "F_Breakage", "F_Normal", "R_Crushed", "R_Breakage", "R_Normal"]
    print("\nDataset Class Counts:")
    for cat in categories:
        cat_path = os.path.join(target_dir, cat)
        if os.path.isdir(cat_path):
            count = len([f for f in os.listdir(cat_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            print(f"  - {cat:12s}: {count} images")

def download_car_parts_dataset_metadata():
    target_dir = os.path.join(BASE_DIR, "car_parts_and_damage_dataset")
    os.makedirs(target_dir, exist_ok=True)
    print(f"\n[2/3] Downloading metadata and samples from 'yusufnull/car-parts-and-damage-dataset'...")

    for fname in ["README.md", "Car parts dataset/meta.json"]:
        try:
            hf_hub_download(
                repo_id="yusufnull/car-parts-and-damage-dataset",
                filename=fname,
                repo_type="dataset",
                local_dir=target_dir
            )
            print(f"  Downloaded: {fname}")
        except Exception as e:
            print(f"  Could not download {fname}: {e}")

def export_samples_to_webapp():
    print("\n[3/3] Exporting diverse test samples to web application static/samples...")
    source_dir = os.path.join(BASE_DIR, "comprehensive_car_damage")
    webapp_samples_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "unified_car_damage_app", "static", "samples"))
    os.makedirs(webapp_samples_dir, exist_ok=True)

    samples_to_copy = [
        ("F_Crushed", "FC_1.jpg", "sample_front_crush.jpg"),
        ("F_Breakage", "FB_1.jpg", "sample_front_breakage.jpg"),
        ("R_Crushed", "RC_1.jpg", "sample_rear_crush.jpg"),
        ("R_Breakage", "RB_1.jpg", "sample_rear_breakage.jpg"),
        ("F_Normal", "FN_1.jpg", "sample_clean_undamaged.jpg"),
    ]

    for cat, src_file, dst_file in samples_to_copy:
        src_path = os.path.join(source_dir, cat, src_file)
        dst_path = os.path.join(webapp_samples_dir, dst_file)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"  Exported sample: {dst_file} (from {cat}/{src_file})")
        else:
            # Fallback to first available file in directory
            cat_dir = os.path.join(source_dir, cat)
            if os.path.isdir(cat_dir):
                files = [f for f in os.listdir(cat_dir) if f.lower().endswith(('.jpg', '.png'))]
                if files:
                    shutil.copy2(os.path.join(cat_dir, files[0]), dst_path)
                    print(f"  Exported sample: {dst_file} (from {cat}/{files[0]})")

if __name__ == "__main__":
    print("==================================================")
    print(" AutoDamage AI — Dataset Downloader")
    print("==================================================")
    download_comprehensive_damage_dataset()
    download_car_parts_dataset_metadata()
    export_samples_to_webapp()
    print("\nAll dataset downloads and exports completed successfully!")
