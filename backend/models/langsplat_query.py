"""LangSplat Query Engine - Semantic 3D search"""
import torch
import numpy as np
from pathlib import Path
from core.config import settings

class LangSplatQuery:
    def __init__(self):
        self.clip_features = None
        self.gaussian_positions = None
        self.loaded = False

    def load_scene(self, scene_path: str):
        scene_file = Path(scene_path)
        if not scene_file.exists():
            raise FileNotFoundError(f"Scene file not found: {scene_path}")
        data = torch.load(scene_file, map_location="cpu")
        self.clip_features = data.get("clip_features")
        self.gaussian_positions = data.get("positions")
        self.loaded = True

    def search(self, text_embedding: np.ndarray, top_k: int = 500):
        if not self.loaded:
            raise RuntimeError("Scene not loaded. Call load_scene() first.")
        text_tensor = torch.from_numpy(text_embedding).float()
        similarities = torch.matmul(self.clip_features, text_tensor.T).squeeze()
        top_indices = similarities.topk(top_k).indices.tolist()
        centroid = self.gaussian_positions[top_indices].mean(dim=0).tolist()
        return {
            "indices": top_indices,
            "centroid": {"x": centroid[0], "y": centroid[1], "z": centroid[2]},
            "count": len(top_indices)
        }

langsplat_query = LangSplatQuery()
