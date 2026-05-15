# NeoTwin — Developer Documentation

## 1. Project Overview

NeoTwin is a production-ready 3D Digital Twin platform that transforms smartphone photos into interactive, AI-powered 3D scenes. This document provides comprehensive technical guidance for developers working on the project.

---

## 2. Architecture Deep Dive

### 2.1 System Components

**Frontend (Viewer):**
- Three.js r169+ for WebGL rendering
- TypeScript for type safety
- Vite for fast builds and HMR
- @sparkjoy/splat for .splat file rendering
- Custom shaders for Gaussian rendering

**Backend (API):**
- FastAPI for async Python web framework
- Google Gemini 2.0 Flash for AI narration
- CLIP for text/image embeddings
- OWL-ViT for object detection
- SAM 2 for segmentation
- LangSplat for semantic 3D search

**Training Pipeline:**
- Google Colab notebooks (free T4 GPU)
- COLMAP for Structure from Motion
- 3D Gaussian Splatting for scene reconstruction
- LangSplat for semantic embeddings
- gsplat for compression

### 2.2 Data Flow

```
User Photos → COLMAP → Camera Poses → 3DGS Training → LangSplat → .splat File
                                                                              ↓
Viewer ← GitHub Pages ← Compressed .splat (8MB) ← gsplat Compression
                                                                              ↓
Search Query → CLIP Encode → LangSplat Query → Highlight Gaussians → Character Moves
                                                                              ↓
Gemini API → Narration → WebSpeech → User Hears Description
```

---

## 3. Setup Instructions

### 3.1 Prerequisites

- Python 3.11+
- Node.js 20+
- Git
- Google Colab account (free)
- Hugging Face account (free)
- GitHub account (free)

### 3.2 Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Viewer:**
```bash
cd viewer
npm install
npm run dev
```

### 3.3 Environment Variables

Create `.env` in backend folder:
```
GEMINI_API_KEY=your_gemini_api_key
HUGGINGFACE_TOKEN=your_hf_token
REDIS_URL=redis://localhost:6379
SENTRY_DSN=your_sentry_dsn (optional)
```

Get Gemini API key: https://aistudio.google.com/apikey

---

## 4. Code Structure

### 4.1 Backend Structure

```
backend/
├── app.py                    # FastAPI entry point
├── api/                      # API routes
│   ├── routes_search.py      # Visual search endpoints
│   ├── routes_identify.py    # Object detection endpoints
│   ├── routes_narrate.py     # AI narration endpoints
│   ├── routes_pipeline.py    # Training pipeline endpoints
│   └── routes_health.py      # Health check endpoints
├── core/                     # Core utilities
│   ├── config.py             # Settings management
│   ├── security.py           # Rate limiting, auth
│   ├── monitoring.py         # Metrics, logging
│   └── exceptions.py         # Error handlers
├── models/                   # ML models
│   ├── gemini_client.py      # Gemini API wrapper
│   ├── clip_engine.py        # CLIP text/image encoding
│   ├── owl_vit_detector.py   # Object detection
│   ├── sam2_segmenter.py     # Segmentation
│   └── langsplat_query.py    # Semantic 3D search
├── pipeline/                 # Training scripts
│   ├── colmap_runner.py      # COLMAP automation
│   ├── train_3dgs.py         # 3DGS training
│   ├── train_langsplat.py    # LangSplat training
│   ├── export_utils.py       # File export
│   └── compression.py        # Splat compression
└── tests/                    # Test suite
```

### 4.2 Viewer Structure

```
viewer/
├── index.html                # Main HTML
├── src/
│   ├── main.ts               # Entry point
│   ├── App.ts                # Main app class
│   ├── core/                 # Core systems
│   │   ├── SceneManager.ts   # Scene management
│   │   ├── CameraController.ts # Camera controls
│   │   └── RenderLoop.ts     # Animation loop
│   ├── character/            # AI character
│   │   ├── AvatarLoader.ts   # GLTF loading
│   │   ├── PathfindingController.ts # A* navigation
│   │   └── NarrationEngine.ts # WebSpeech + API
│   ├── search/               # Visual search
│   │   ├── SearchEngine.ts   # API client
│   │   └── GaussianHighlighter.ts # Highlight logic
│   └── types/                # TypeScript types
└── public/                   # Static assets
    ├── assets/               # Avatar, navmesh
    └── scenes/               # .splat files
```

---

## 5. API Reference

### 5.1 Search Endpoint

**POST** `/api/v1/search`

Search for objects in 3D scene using natural language.

**Request Body:**
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

### 5.2 Identify Endpoint

**POST** `/api/v1/identify`

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

### 5.3 Narrate Endpoint

**POST** `/api/v1/narrate`

Generate AI narration for scene.

**Request Body:**
```json
{
  "image_path": "/path/to/image.jpg",
  "prompt": "Describe this scene",
  "style": "gta"
}
```

**Styles:** `gta`, `architect`, `tourist`, `detective`

---

## 6. Training Pipeline

### 6.1 COLMAP (Camera Poses)

```python
from pipeline.colmap_runner import run_colmap
sparse_dir = run_colmap("data/images")
```

**Output:**
- `sparse/0/cameras.bin` — Camera intrinsics
- `sparse/0/images.bin` — Camera extrinsics
- `sparse/0/points3D.bin` — Sparse point cloud

### 6.2 3DGS Training

```python
from pipeline.train_3dgs import train_3dgs
ply_path = train_3dgs("data", sparse_dir, iterations=30000)
```

**Parameters:**
- `iterations`: 30000 (default), 7000 (fast)
- `data`: Directory with images and sparse output
- `sparse_dir`: COLMAP output directory

**Output:** `point_cloud.ply` (~300MB)

### 6.3 LangSplat Training

```python
from pipeline.train_langsplat import train_langsplat
langsplat_path = train_langsplat(ply_path)
```

**Output:** LangSplat checkpoint with CLIP embeddings

### 6.4 Compression

```python
from pipeline.compression import compress_splat
splat_path = compress_splat(ply_path, target_size_mb=8)
```

**Result:** 300MB → 8MB (37x compression)

---

## 7. Testing

### 7.1 Backend Tests

```bash
cd backend
pytest tests/ -v
```

**Test Coverage:**
- API endpoints
- Model inference
- Pipeline steps
- Error handling

### 7.2 Viewer Tests

```bash
cd viewer
npm test
```

**Test Coverage:**
- Component rendering
- Search functionality
- Character animation
- Pathfinding

---

## 8. Deployment

### 8.1 GitHub Pages (Viewer)

```bash
cd viewer
npm run build
git add dist
git commit -m "Build viewer"
git push origin main
```

Auto-deploys via GitHub Actions.

### 8.2 Hugging Face Spaces (Backend)

```bash
huggingface-cli upload username/neotwin-api ./backend .
```

Set secrets in Space Settings:
- `GEMINI_API_KEY`
- `HUGGINGFACE_TOKEN`

### 8.3 Custom Domain

Configure DNS:
```
viewer.yourdomain.com → GitHub Pages
api.yourdomain.com → HF Spaces
```

---

## 9. Performance Optimization

### 9.1 Rendering

- Use Mip-Splatting for anti-aliasing
- Compress .splat to 8MB max
- Limit pixel ratio to 2x
- Use Web Workers for heavy computation

### 9.2 Backend

- Cache CLIP embeddings (Redis)
- Batch Gemini API calls
- Use async endpoints
- Rate limit at 15 RPM

### 9.3 Network

- CDN for Three.js libraries
- Gzip compress API responses
- HTTP/2 for parallel requests
- Lazy load .splat file

---

## 10. Troubleshooting

### 10.1 Common Issues

**COLMAP fails:**
- Ensure 70%+ image overlap
- Check image quality
- Try HLoc for difficult scenes

**3DGS training crashes:**
- Reduce batch size
- Check GPU memory (need 8GB+)
- Use Colab T4 or A100

**Viewer doesn't load:**
- Check .splat file path
- Verify Three.js version
- Check browser console

**Gemini API errors:**
- Verify API key
- Check rate limit (15 RPM)
- Ensure image format supported

### 10.2 Debugging Tools

- **Backend:** FastAPI docs at `/docs`
- **Viewer:** Browser DevTools
- **Training:** TensorBoard logs
- **GPU:** `nvidia-smi`

---

## 11. Contributing

### 11.1 Workflow

1. Fork repository
2. Create feature branch
3. Make changes
4. Run tests
5. Commit with conventional commits
6. Open PR

### 11.2 Code Standards

- Python: PEP 8, type hints
- TypeScript: Strict mode, no `any`
- Commits: `feat(scope): description`
- Tests: Required for new features

---

## 12. Future Enhancements

### 12.1 Planned Features

- Multi-scene support
- WebXR AR mode
- Collaborative sessions
- Custom AI characters
- Video-to-3D pipeline
- Advanced editing tools
- SDK for developers

### 12.2 Research Directions

- Real-time 3DGS training
- Dynamic scene reconstruction
- Multi-modal search (text + image)
- Physics simulation
- Generative scene editing

---

## 13. Resources

### 13.1 Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Performance](docs/PERFORMANCE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [3D Deep Learning Guide](docs/3D_DEEP_LEARNING_GUIDE.md)

### 13.2 External Resources

- 3DGS Paper: https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/
- LangSplat: https://github.com/minghanqin/LangSplat
- Three.js: https://threejs.org/docs/
- FastAPI: https://fastapi.tiangolo.com/
- Gemini: https://ai.google.dev/

---

*Last updated: May 2026*
*Version: 1.0.0*
*Maintainer: NeoTwin Team*
