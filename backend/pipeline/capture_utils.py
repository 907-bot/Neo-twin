"""
Capture Utilities - Video Processing & Frame Extraction
Handles video upload, frame extraction, quality filtering
"""

import subprocess
import os
import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, List, Dict

class VideoProcessor:
    """Process video uploads for 3D reconstruction"""
    
    def __init__(self):
        self.supported_formats = ['.mp4', '.mov', '.avi', '.mkv']
        self.max_file_size_mb = 500
        self.min_duration_sec = 30
        self.max_duration_sec = 600
        self.target_fps = 2
        self.max_resolution = 1920
        self.blur_threshold = 100.0
        self.min_frames = 50
        self.max_frames = 500

    def validate_video(self, video_path: str) -> Dict:
        """Validate video file before processing"""
        result = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "info": {}
        }
        
        # Check file exists
        if not os.path.exists(video_path):
            result["valid"] = False
            result["errors"].append("Video file not found")
            return result
        
        # Check file size
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
        if file_size_mb > self.max_file_size_mb:
            result["valid"] = False
            result["errors"].append(f"File too large: {file_size_mb:.1f}MB (max {self.max_file_size_mb}MB)")
            return result
        
        # Get video info
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            result["valid"] = False
            result["errors"].append("Cannot open video file")
            return result
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0
        
        result["info"] = {
            "fps": fps,
            "frame_count": frame_count,
            "width": width,
            "height": height,
            "duration": duration,
            "file_size_mb": round(file_size_mb, 2)
        }
        
        # Validate duration
        if duration < self.min_duration_sec:
            result["valid"] = False
            result["errors"].append(
                f"Video too short: {duration:.0f}s (minimum {self.min_duration_sec}s). "
                f"Walk slowly around the space for better reconstruction."
            )
        
        if duration > self.max_duration_sec:
            result["warnings"].append(
                f"Video very long: {duration:.0f}s. Processing may take longer. "
                f"Consider trimming to 1-5 minutes."
            )
        
        # Check resolution
        if width < 1280 or height < 720:
            result["warnings"].append(
                f"Low resolution: {width}x{height}. "
                f"Recommend 1080p or 4K for best results."
            )
        
        # Check FPS
        if fps < 24:
            result["warnings"].append(
                f"Low frame rate: {fps:.0f}fps. "
                f"Recommend 30fps or 60fps for smooth capture."
            )
        
        # Sample frames for quality check
        quality_score = self._assess_video_quality(cap, frame_count)
        result["info"]["quality_score"] = quality_score
        
        if quality_score < 0.5:
            result["warnings"].append(
                f"Low video quality detected (score: {quality_score:.2f}). "
                f"Ensure good lighting and steady camera movement."
            )
        
        cap.release()
        return result

    def _assess_video_quality(self, cap: cv2.VideoCapture, frame_count: int) -> float:
        """Assess overall video quality by sampling frames"""
        sample_count = min(20, frame_count)
        step = max(1, frame_count // sample_count)
        
        quality_scores = []
        for i in range(0, frame_count, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                continue
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Normalize to 0-1
            normalized = min(1.0, blur_score / 500.0)
            quality_scores.append(normalized)
        
        return np.mean(quality_scores) if quality_scores else 0.0

    def extract_frames(
        self,
        video_path: str,
        output_dir: str,
        fps: int = None,
        max_resolution: int = None
    ) -> Tuple[str, int]:
        """
        Extract frames from video using ffmpeg
        
        Returns:
            Tuple of (output_dir, frame_count)
        """
        if fps is None:
            fps = self.target_fps
        if max_resolution is None:
            max_resolution = self.max_resolution
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Calculate optimal FPS based on video duration
        cap = cv2.VideoCapture(video_path)
        duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        
        # Adjust FPS to target 100-300 frames
        optimal_fps = max(1, min(4, int(200 / duration)))
        fps = min(fps, optimal_fps)
        
        # Extract frames with ffmpeg
        output_pattern = os.path.join(output_dir, "frame_%04d.jpg")
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"fps={fps},scale={max_resolution}:-1",
            "-q:v", "2",
            "-y",
            output_pattern
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ffmpeg failed: {e.stderr.decode()}")
        
        # Filter blurry frames
        filtered_count = self.filter_blurry_frames(output_dir)
        
        # Limit frame count
        self.limit_frames(output_dir, self.max_frames)
        
        final_count = len([f for f in os.listdir(output_dir) if f.endswith('.jpg')])
        
        if final_count < self.min_frames:
            raise ValueError(
                f"Too few frames extracted: {final_count} (minimum {self.min_frames}). "
                f"Please record a longer video or walk more slowly."
            )
        
        return output_dir, final_count

    def filter_blurry_frames(self, frames_dir: str, threshold: float = None) -> int:
        """Remove blurry frames using Laplacian variance"""
        if threshold is None:
            threshold = self.blur_threshold
        
        frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])
        removed = 0
        
        for frame in frames:
            path = os.path.join(frames_dir, frame)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            
            variance = cv2.Laplacian(img, cv2.CV_64F).var()
            
            if variance < threshold:
                os.remove(path)
                removed += 1
        
        print(f"Removed {removed} blurry frames, kept {len(frames) - removed}")
        return len(frames) - removed

    def limit_frames(self, frames_dir: str, max_frames: int):
        """Limit frame count by sampling evenly"""
        frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])
        
        if len(frames) <= max_frames:
            return
        
        # Keep evenly spaced frames
        step = len(frames) / max_frames
        keep_indices = [int(i * step) for i in range(max_frames)]
        
        for i, frame in enumerate(frames):
            if i not in keep_indices:
                os.remove(os.path.join(frames_dir, frame))

    def generate_preview(self, video_path: str, output_dir: str, num_previews: int = 10) -> List[str]:
        """Generate preview images from video"""
        os.makedirs(output_dir, exist_ok=True)
        
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        step = frame_count // num_previews
        
        preview_paths = []
        for i in range(0, frame_count, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                break
            
            preview_path = os.path.join(output_dir, f"preview_{i:04d}.jpg")
            cv2.imwrite(preview_path, frame)
            preview_paths.append(preview_path)
        
        cap.release()
        return preview_paths

    def get_capture_instructions(self) -> Dict:
        """Return video capture instructions for users"""
        return {
            "title": "How to Capture Your Space",
            "duration": "2-5 minutes per room",
            "steps": [
                {
                    "step": 1,
                    "title": "Start at One Corner",
                    "description": "Begin recording at one corner of the room",
                    "tip": "Hold phone steady at eye level"
                },
                {
                    "step": 2,
                    "title": "Walk Slowly in a Circle",
                    "description": "Walk around the perimeter of the room slowly",
                    "tip": "Maintain 70% overlap between views"
                },
                {
                    "step": 3,
                    "title": "Tilt Up and Down",
                    "description": "Capture ceiling, walls, and floor",
                    "tip": "Don't just shoot at eye level"
                },
                {
                    "step": 4,
                    "title": "Get Close to Objects",
                    "description": "Move closer to furniture and details",
                    "tip": "Capture from multiple angles"
                },
                {
                    "step": 5,
                    "title": "Complete the Circle",
                    "description": "Return to starting position",
                    "tip": "Ensure full 360° coverage"
                }
            ],
            "do": [
                "Walk slowly and steadily",
                "Capture from multiple heights",
                "Get close to important objects",
                "Shoot in good lighting",
                "Complete full circles around spaces"
            ],
            "dont": [
                "Run or move too fast",
                "Stand still and rotate",
                "Point only at blank walls",
                "Use digital zoom",
                "Shoot in very dark areas"
            ],
            "ideal_specs": {
                "resolution": "1080p or 4K",
                "frame_rate": "30fps or 60fps",
                "duration": "2-5 minutes per room",
                "format": "MP4 or MOV",
                "max_file_size": "500MB"
            }
        }


# Singleton instance
video_processor = VideoProcessor()
