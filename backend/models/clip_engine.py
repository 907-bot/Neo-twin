"""CLIP Engine - Text encoding for visual search"""
import torch
import clip
from PIL import Image
import numpy as np
from core.config import settings

class CLIPEngine:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(settings.CLIP_MODEL, device=self.device)
        self.model.eval()

    def encode_text(self, query: str) -> np.ndarray:
        tokens = clip.tokenize([query]).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(tokens)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        return text_features.cpu().numpy()

    def encode_image(self, image_path: str) -> np.ndarray:
        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        return image_features.cpu().numpy()

    def compute_similarity(self, text: str, image_path: str) -> float:
        text_vec = self.encode_text(text)
        image_vec = self.encode_image(image_path)
        return float(np.dot(text_vec[0], image_vec[0]))

clip_engine = CLIPEngine()
