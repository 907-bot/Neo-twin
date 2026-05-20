"""COLMAP Runner - Structure from Motion"""
import subprocess
import os
import shutil
from pathlib import Path
from core.config import settings

# Try to detect GPU using torch to speed up SIFT extraction and matching if available
try:
    import torch
    GPU_AVAILABLE = torch.cuda.is_available()
except ImportError:
    GPU_AVAILABLE = False

# Well-known vocabulary tree paths used by COLMAP for loop detection.
# Loop detection (--SequentialMatching.loop_detection 1) REQUIRES this file.
# Without it, COLMAP hard-aborts (SIGABRT) with a visual_index.h assertion error.
_VOCAB_TREE_SEARCH_PATHS = [
    "/usr/local/share/colmap/vocab_tree_flickr100K_words32K.bin",
    "/usr/share/colmap/vocab_tree_flickr100K_words32K.bin",
    "/opt/colmap/vocab_tree_flickr100K_words32K.bin",
    os.path.expanduser("~/vocab_tree_flickr100K_words32K.bin"),
    os.path.join(os.path.dirname(__file__), "../../data/vocab_tree_flickr100K_words32K.bin"),
]

def _find_vocab_tree() -> str | None:
    """Return path to COLMAP vocabulary tree, or None if not found."""
    for path in _VOCAB_TREE_SEARCH_PATHS:
        if os.path.isfile(path):
            return path
    return None

def run_colmap(image_dir: str, output_dir: str = None) -> str:
    """
    Run COLMAP Structure-from-Motion pipeline.

    Steps:
      1. feature_extractor   – detects SIFT keypoints in each frame
      2. sequential_matcher  – matches features between adjacent frames
      3. mapper              – reconstructs sparse 3D point cloud

    Raises subprocess.CalledProcessError on failure so the caller's
    pipeline fallback is triggered correctly.
    """
    # Force Qt headless mode — prevents X11 display connection errors on servers
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

    if output_dir is None:
        output_dir = os.path.join(image_dir, "sparse")
    os.makedirs(output_dir, exist_ok=True)

    # Put database file one level above image_dir to prevent COLMAP from
    # scanning database files (.db, .db-shm, .db-wal) as image files.
    database_path = os.path.join(os.path.dirname(image_dir), f"{os.path.basename(image_dir)}_database.db")
    gpu_param = "1" if GPU_AVAILABLE else "0"

    print(f"COLMAP execution config: GPU_ENABLED={GPU_AVAILABLE} (Detected via torch)")

    # ── Step 1: Feature extraction (SPEED-OPTIMIZED) ──────────────────────
    # Optimization notes:
    # 1. `--SiftExtraction.first_octave 0` disables image upscaling (defaults to -1).
    #    Upscaling takes 4x-10x longer. Disabling it speeds up extraction by 3-5x.
    # 2. `--SiftExtraction.max_num_features 2048` limits the number of keypoints,
    #    which speeds up the extraction and quadratic matching steps.
    # 3. `--ImageReader.single_camera 1` shares the same camera parameters across
    #    all video frames (since they come from the same physical camera/sensor).
    #    This prevents independent camera calibration drift and solves registration errors.
    # 4. `--ImageReader.camera_model SIMPLE_RADIAL` is highly stable for consumer cameras
    #    and prevents parameter estimation failures compared to the 8-parameter OPENCV model.
    print("Step 1: Feature extraction (Optimized)...")
    subprocess.run([
        settings.COLMAP_PATH, "feature_extractor",
        "--image_path",                          image_dir,
        "--database_path",                       database_path,
        "--ImageReader.camera_model",            "SIMPLE_RADIAL",
        "--ImageReader.single_camera",           "1",
        "--SiftExtraction.use_gpu",              gpu_param,
        "--SiftExtraction.first_octave",         "0",     # Disable upscaling for 3-5x speedup
        "--SiftExtraction.max_num_features",     "2048",  # Limit features to keep matching fast
        "--SiftExtraction.estimate_affine_shape","0",
    ], check=True)

    # ── Step 2: Feature matching (SPEED-OPTIMIZED) ─────────────────────────
    # Optimization notes:
    # 1. `--SequentialMatching.overlap 5` matches each frame with 5 adjacent frames
    #    instead of 10. For video datasets with high overlap, this is more than
    #    enough and cuts matching time in half.
    # 2. loop_detection is disabled unless the vocabulary tree is actually present.
    print("Step 2: Feature matching (Sequential)...")
    vocab_tree_path = _find_vocab_tree()
    loop_detection_enabled = "1" if vocab_tree_path else "0"

    if vocab_tree_path:
        print(f"  [loop_detection] Vocab tree found: {vocab_tree_path}")
    else:
        print("  [loop_detection] Vocab tree NOT found — loop detection disabled to prevent SIGABRT.")
        print("  [loop_detection] To enable: download vocab_tree_flickr100K_words32K.bin and place in data/")

    matcher_cmd = [
        settings.COLMAP_PATH, "sequential_matcher",
        "--database_path",                     database_path,
        "--SiftMatching.use_gpu",              gpu_param,
        "--SequentialMatching.overlap",        "5",     # Reduced from 10 to cut matching time in half
        "--SequentialMatching.loop_detection", loop_detection_enabled,
    ]
    if vocab_tree_path:
        matcher_cmd += ["--SequentialMatching.vocab_tree_path", vocab_tree_path]

    subprocess.run(matcher_cmd, check=True)

    # ── Step 3: Sparse reconstruction ───────────────────────────────────────
    print("Step 3: Sparse reconstruction (High Resiliency)...")
    subprocess.run([
        settings.COLMAP_PATH, "mapper",
        "--database_path",                    database_path,
        "--image_path",                       image_dir,
        "--output_path",                      output_dir,
        "--Mapper.init_min_tri_angle",        "4.0",   # Handles low-parallax camera moves
        "--Mapper.init_min_num_inliers",      "30",    # Initializes with fewer features
        "--Mapper.init_max_reg_trials",       "300",   # Searches harder for starting pairs
        "--Mapper.abs_pose_min_num_inliers",  "15",    # Registers hard-to-match frames
        "--Mapper.filter_max_reproj_error",   "6.0",   # Tolerates minor lens distortion & noise
    ], check=True)

    return os.path.join(output_dir, "0")
