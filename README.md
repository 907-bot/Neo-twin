# NeoTwin — 3D Digital Twin Platform

## 🚀 Overview

NeoTwin transforms **a simple video** of your space into a photorealistic, interactive 3D scene with an AI character that explores, identifies objects, and narrates findings using natural language.

**Live Demo:** [Coming Soon](#)
**Backend API:** [Coming Soon](#)

## ✨ Features

- **📹 Video-to-3D** — Upload a 2-5 minute video, get a complete 3D scene
- **3D Gaussian Splatting** — 100+ FPS photorealistic rendering
- **Semantic Search** — Find objects with natural language ("red chair")
- **AI Character** — GTA-style guide powered by Gemini 2.0 Flash
- **Object Detection** — OWL-ViT + SAM 2 for scene understanding
- **WebXR AR Mode** — Place your digital twin in the real world
- **100% Free** — Zero hosting, GPU, or AI costs

## 🎥 How It Works

```
1. RECORD VIDEO (2-5 min)
   Walk around your space recording
   
2. UPLOAD TO NEOTWIN
   Drag & drop your video file
   
3. EXPLORE IN 3D
   Walk through your digital twin in browser
```

**That's it!** No manual photo selection, no technical knowledge needed.

## 🏗️ Architecture

```
Viewer (Three.js) ←→ Backend API (FastAPI + Gemini) ←→ Training (Colab)
```

## 🚀 Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Viewer
```bash
cd viewer
npm install
npm run dev
```

### Training (Google Colab)
1. Open `notebooks/01_colmap_pose_estimation.ipynb`
2. Run all cells
3. Download `.splat` file
4. Place in `viewer/public/scenes/`

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Performance](docs/PERFORMANCE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 💰 Zero-Cost Stack

| Resource | Service | Cost |
|----------|---------|------|
| AI Model | Gemini 2.0 Flash | FREE |
| Training GPU | Google Colab T4 | FREE |
| Backend | Hugging Face Spaces | FREE |
| Viewer | GitHub Pages | FREE |

## 📅 Roadmap

- [x] Core 3DGS pipeline
- [x] Gemini AI integration
- [x] Three.js viewer
- [x] Visual search
- [ ] Multi-scene support
- [ ] WebXR AR mode
- [ ] Collaborative sessions

## 🤝 Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md)

## 📄 License

MIT — See [LICENSE](LICENSE)
