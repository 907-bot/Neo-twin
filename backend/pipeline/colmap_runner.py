"""COLMAP Runner - Structure from Motion"""
import subprocess
import os
from pathlib import Path
from core.config import settings

def run_colmap(image_dir: str, output_dir: str = None) -> str:
    if output_dir is None:
        output_dir = os.path.join(image_dir, "sparse")
    os.makedirs(output_dir, exist_ok=True)
    database_path = os.path.join(image_dir, "database.db")
    print("Step 1: Feature extraction...")
    subprocess.run([
        settings.COLMAP_PATH, "feature_extractor",
        "--image_path", image_dir,
        "--database_path", database_path,
        "--ImageReader.camera_model", "OPENCV"
    ], check=True)
    print("Step 2: Feature matching...")
    subprocess.run([
        settings.COLMAP_PATH, "exhaustive_matcher",
        "--database_path", database_path
    ], check=True)
    print("Step 3: Sparse reconstruction...")
    subprocess.run([
        settings.COLMAP_PATH, "mapper",
        "--database_path", database_path,
        "--image_path", image_dir,
        "--output_path", output_dir
    ], check=True)
    return os.path.join(output_dir, "0")
