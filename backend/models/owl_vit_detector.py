import torch
from transformers import pipeline
from core.config import settings

class OWLViTDetector:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.detector = pipeline(
            "zero-shot-object-detection",
            model=settings.OWL_VIT_MODEL,
            device=self.device
        )
        self.default_labels = [
            "chair", "table", "lamp", "sofa", "window", "door",
            "plant", "monitor", "keyboard", "shelf", "painting", "rug", "bed",
            "cup", "bottle", "book", "vase", "clock", "mirror", "cabinet"
        ]

    def detect_objects(self, image, labels=None, threshold=0.15):
        if labels is None:
            labels = self.default_labels
        results = self.detector(image, candidate_labels=labels)
        return [
            {
                "label": r["label"],
                "confidence": round(r["score"], 3),
                "box": r["box"]
            }
            for r in results if r["score"] > threshold
        ]

owl_vit_detector = OWLViTDetector()
