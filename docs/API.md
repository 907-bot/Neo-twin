# NeoTwin API Reference

## Base URL
```
https://huggingface.co/spaces/username/neotwin-api
```

## Endpoints

### POST `/api/v1/search`
Search for objects in 3D scene using natural language.

**Request:**
```json
{
  "query": "red chair",
  "top_k": 500,
  "scene_id": "default"
}
```

**Response:**
```json
{
  "indices": [123, 456, 789],
  "centroid": {"x": 1.2, "y": 0.5, "z": 3.4},
  "count": 500,
  "refined_query": "red wooden chair"
}
```

### POST `/api/v1/identify`
Detect objects in scene image.

**Request:** Multipart form data with image file

**Response:**
```json
{
  "objects": [
    {"label": "chair", "confidence": 0.92, "box": {...}}
  ],
  "narration": "I see a red chair near the window...",
  "total_count": 5
}
```

### POST `/api/v1/narrate`
Generate AI narration for scene.

**Request:**
```json
{
  "image_path": "/path/to/image.jpg",
  "prompt": "Describe this scene",
  "style": "gta"
}
```

**Styles:** `gta`, `architect`, `tourist`, `detective`

### GET `/api/v1/health`
Health check with system metrics.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "gpu_available": true,
  "gpu_memory_mb": 2048,
  "cpu_percent": 15.2,
  "memory_percent": 45.8
}
```
