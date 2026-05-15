"""LangSplat Training"""
import subprocess
import os

def train_langsplat(ply_path: str) -> str:
    langsplat_dir = os.path.join(os.path.dirname(__file__), "../../LangSplat")
    output_path = ply_path.replace("point_cloud.ply", "langsplat.ckpt")
    cmd = [
        "python", f"{langsplat_dir}/train.py",
        "--start_checkpoint", ply_path.replace(".ply", ".pth"),
        "--feature_level", "3"
    ]
    print(f"Training LangSplat: {cmd}")
    subprocess.run(cmd, check=True)
    return output_path
