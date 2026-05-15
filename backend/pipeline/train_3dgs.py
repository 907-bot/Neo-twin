"""3DGS Training Wrapper"""
import subprocess
import os
from core.config import settings

def train_3dgs(data_dir: str, sparse_dir: str, iterations: int = 30000) -> str:
    gs_path = os.path.join(os.path.dirname(__file__), "../../gaussian-splatting")
    output_dir = os.path.join(data_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "python", f"{gs_path}/train.py",
        "-s", data_dir,
        "--iterations", str(iterations),
        "--eval",
        "--output_path", output_dir
    ]
    print(f"Training 3DGS: {cmd}")
    subprocess.run(cmd, check=True)
    ply_path = os.path.join(output_dir, "point_cloud", "iteration_30000", "point_cloud.ply")
    return ply_path
