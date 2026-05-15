"""SAM 2 Segmentation"""
from core.config import settings
import numpy as np

class SAM2Segmenter:
    def __init__(self):
        self.predictor = None
        self.current_image = None

    def load_model(self):
        try:
            from sam2.build_sam import build_sam2
            from sam2.sam2_image_predictor import SAM2ImagePredictor
            model = build_sam2("sam2_hiera_large.pt")
            self.predictor = SAM2ImagePredictor(model)
        except ImportError:
            print("SAM 2 not installed. Segmentation disabled.")

    def set_image(self, image):
        self.current_image = image
        if self.predictor:
            self.predictor.set_image(image)

    def segment_at_point(self, x: int, y: int) -> np.ndarray:
        if not self.predictor:
            return np.zeros((1, 1))
        masks, scores, _ = self.predictor.predict(
            point_coords=[[x, y]],
            point_labels=[1],
            multimask_output=False
        )
        return masks[0]

sam2_segmenter = SAM2Segmenter()
