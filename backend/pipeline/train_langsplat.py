"""LangSplat Training"""
import subprocess
import os

def train_langsplat(ply_path: str) -> str:
    import torch
    cuda_available = torch.cuda.is_available()
    
    langsplat_dir = os.path.join(os.path.dirname(__file__), "../../LangSplat")
    output_path = ply_path.replace("point_cloud.ply", "langsplat.ckpt")
    
    if cuda_available and os.path.exists(os.path.join(langsplat_dir, "train.py")):
        cmd = [
            "python", f"{langsplat_dir}/train.py",
            "--start_checkpoint", ply_path.replace(".ply", ".pth"),
            "--feature_level", "3"
        ]
        print(f"Training LangSplat: {cmd}")
        subprocess.run(cmd, check=True)
    else:
        print("[NeoTwin Fallback] Skipping LangSplat training on CPU/Simulation. Creating dummy checkpoint...")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write("dummy_langsplat_checkpoint")
            
    return output_path
