"""COLMAP Runner - Structure from Motion"""
import subprocess
import os
import shutil
from pathlib import Path
from core.config import settings

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

    database_path = os.path.join(image_dir, "database.db")

    # ── Step 1: Feature extraction ──────────────────────────────────────────
    print("Step 1: Feature extraction (Optimized)...")
    subprocess.run([
        settings.COLMAP_PATH, "feature_extractor",
        "--image_path",                          image_dir,
        "--database_path",                       database_path,
        "--ImageReader.camera_model",            "OPENCV",
        "--SiftExtraction.use_gpu",              "0",
        "--SiftExtraction.max_num_features",     "4096",
        "--SiftExtraction.estimate_affine_shape","0",
    ], check=True)

    # ── Step 2: Feature matching ─────────────────────────────────────────────
    # CRITICAL: loop_detection=1 requires a vocabulary tree binary.
    # Without it COLMAP opens a file that doesn't exist and raises SIGABRT
    # (triggers visual_index.h assertion failure). We only enable it when the
    # vocab tree is actually present on this machine.
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
        "--database_path",                    database_path,
        "--SiftMatching.use_gpu",             "0",
        "--SequentialMatching.overlap",       "10",
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
