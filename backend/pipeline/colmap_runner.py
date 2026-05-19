"""COLMAP Runner - Structure from Motion"""
import subprocess
import os
from pathlib import Path
from core.config import settings

def run_colmap(image_dir: str, output_dir: str = None) -> str:
    # Force Qt to run in headless (offscreen) mode to prevent X11 display connection errors
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    if output_dir is None:
        output_dir = os.path.join(image_dir, "sparse")
    os.makedirs(output_dir, exist_ok=True)
    database_path = os.path.join(image_dir, "database.db")
    print("Step 1: Feature extraction (Optimized)...")
    subprocess.run([
        settings.COLMAP_PATH, "feature_extractor",
        "--image_path", image_dir,
        "--database_path", database_path,
        "--ImageReader.camera_model", "OPENCV",
        "--SiftExtraction.use_gpu", "0",
        "--SiftExtraction.max_num_features", "10240",
        "--SiftExtraction.estimate_affine_shape", "1"
    ], check=True)
    print("Step 2: Feature matching (Permissive)...")
    subprocess.run([
        settings.COLMAP_PATH, "exhaustive_matcher",
        "--database_path", database_path,
        "--SiftMatching.use_gpu", "0",
        "--SiftMatching.max_ratio", "0.85"
    ], check=True)
    print("Step 3: Sparse reconstruction (High Resiliency)...")
    subprocess.run([
        settings.COLMAP_PATH, "mapper",
        "--database_path", database_path,
        "--image_path", image_dir,
        "--output_path", output_dir,
        "--Mapper.init_min_tri_angle", "4.0",          # Essential: Handles low parallax camera moves
        "--Mapper.init_min_num_inliers", "30",          # Essential: Initializes with fewer features
        "--Mapper.init_max_reg_trials", "300",          # Essential: Searches harder for starting pairs
        "--Mapper.abs_pose_min_num_inliers", "15",      # Essential: Registers hard-to-match frames
        "--Mapper.filter_max_reproj_error", "6.0"       # Tolerate minor lens distortion & noise
    ], check=True)
    return os.path.join(output_dir, "0")
