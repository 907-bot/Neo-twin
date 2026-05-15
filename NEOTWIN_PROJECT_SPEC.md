# NeoTwin — Production-Ready 3D Digital Twin Platform

## 🎯 Project Vision

Build a **GTA-style interactive 3D digital twin** where users upload smartphone photos/video and get a photorealistic, explorable 3D scene with an AI character that walks around, identifies objects, narrates findings, and supports natural language visual search.

**Target:** Portfolio-ready, production-grade application capable of landing a ₹1 Cr (10M INR) role in 3D AI/ML engineering.

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                      │
│   Browser: Three.js Splat Viewer + GTA Character Overlay         │
│   Controls: WASD/Joystick · Text Search Bar · LLM Chat Panel     │
│   UI: Google Stitch-generated components (glass morphism HUD)    │
└─────────────────────────┬────────────────────────────────────────┘
                          │  WebGL / WebXR
┌─────────────────────────▼────────────────────────────────────────┐
│                       3DGS SCENE LAYER                           │
│   .splat / .ply file  ←  LangSplat CLIP 512-d vectors baked in  │
│   Renderer: @sparkjoy/splat  +  Three.js r169+                   │
└──────────┬──────────────────────────────┬────────────────────────┘
           │                              │
    ┌──────▼────────┐             ┌───────▼────────────┐
    │  GTA AGENT    │             │   VISUAL SEARCH    │
    │  GLTF Avatar  │             │   CLIP text query  │
    │  Mixamo anims │             │   OWL-ViT detect   │
    │  A* pathfind  │             │   SAM 2 segment    │
    │  Gemini brain │             │   Gaussian hilite  │
    │  WebSpeech    │             └────────────────────┘
    └──────┬────────┘
           │
┌──────────▼───────────────────────────────────────────────────────┐
│                  HF SPACES BACKEND  (FastAPI + Gradio)           │
│   /reconstruct  →  COLMAP  →  3DGS train  →  export .splat      │
│   /search       →  Gemini + CLIP query   →  Gaussian indices    │
│   /identify     →  OWL-ViT inference      →  object inventory   │
│   /narrate      →  Gemini vision API      →  narration text     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 💰 Zero-Cost Stack (100% Free)

| Resource | Service | Cost | Limits |
|----------|---------|------|--------|
| **AI Model** | Google Gemini 2.0 Flash | **FREE** | 15 RPM, 1M tokens/day |
| **Training GPU** | Google Colab T4 | **FREE** | 12hr sessions |
| **Backend Hosting** | Hugging Face Spaces | **FREE** | T4 GPU, auto-sleep |
| **Viewer Hosting** | GitHub Pages | **FREE** | 1GB storage, 100GB/mo |
| **File Storage** | GitHub LFS | **FREE** | 1GB repo, 1GB/mo bandwidth |
| **UI Generation** | Google Stitch MCP | **FREE** | Unlimited |
| **Planning** | Notion MCP | **FREE** | Personal plan |
| **CI/CD** | GitHub Actions | **FREE** | 2000 min/mo |
| **Avatar** | ReadyPlayerMe | **FREE** | Unlimited |
| **Animations** | Mixamo | **FREE** | Unlimited |
| **TTS** | WebSpeech API | **FREE** | Browser-native |

**Total Monthly Cost: $0**

---

## 📁 Project Structure

```
neotwin/
│
├── 📂 backend/                          # FastAPI + Gradio Backend
│   ├── app.py                           # Main FastAPI application
│   ├── requirements.txt                 # Python dependencies
│   ├── Dockerfile                       # Container for HF Spaces
│   ├── .env.example                     # Environment variables template
│   │
│   ├── 📂 api/                          # API Routes
│   │   ├── __init__.py
│   │   ├── routes_search.py             # /search endpoint (CLIP queries)
│   │   ├── routes_identify.py           # /identify endpoint (OWL-ViT)
│   │   ├── routes_narrate.py            # /narrate endpoint (Gemini vision)
│   │   ├── routes_pipeline.py           # /reconstruct endpoint (COLMAP + 3DGS)
│   │   └── routes_health.py             # /health, /metrics endpoints
│   │
│   ├── 📂 core/                         # Core Logic
│   │   ├── __init__.py
│   │   ├── config.py                    # Settings management
│   │   ├── security.py                  # API key validation, rate limiting
│   │   ├── monitoring.py                # Prometheus metrics, logging
│   │   └── exceptions.py                # Custom error handlers
│   │
│   ├── 📂 models/                       # ML Models
│   │   ├── __init__.py
│   │   ├── clip_engine.py               # CLIP text encoding
│   │   ├── gemini_client.py             # Gemini 2.0 Flash integration
│   │   ├── owl_vit_detector.py          # Object detection
│   │   ├── sam2_segmenter.py            # SAM 2 segmentation
│   │   └── langsplat_query.py           # LangSplat Gaussian search
│   │
│   ├── 📂 pipeline/                     # Training Pipeline
│   │   ├── __init__.py
│   │   ├── capture_utils.py             # Frame extraction, validation
│   │   ├── colmap_runner.py             # COLMAP automation
│   │   ├── train_3dgs.py                # 3DGS training wrapper
│   │   ├── train_langsplat.py           # LangSplat training
│   │   ├── export_utils.py              # .splat, .glb, .ply export
│   │   └── compression.py               # gsplat compression
│   │
│   ├── 📂 services/                     # Business Logic
│   │   ├── __init__.py
│   │   ├── scene_manager.py             # Scene CRUD operations
│   │   ├── cache_service.py             # Redis caching layer
│   │   ├── storage_service.py           # S3/local file storage
│   │   └── notification_service.py      # Email/webhook notifications
│   │
│   └── 📂 tests/                        # Backend Tests
│       ├── __init__.py
│       ├── test_api_search.py
│       ├── test_api_identify.py
│       ├── test_api_narrate.py
│       ├── test_pipeline_colmap.py
│       ├── test_models_clip.py
│       ├── test_models_gemini.py
│       └── conftest.py                  # Pytest fixtures
│
├── 📂 viewer/                           # Three.js Web Viewer
│   ├── index.html                       # Main HTML entry
│   ├── package.json                     # Node dependencies
│   ├── vite.config.js                   # Vite build config
│   ├── tsconfig.json                    # TypeScript config
│   ├── .env.example                     # Environment variables
│   │
│   ├── 📂 src/
│   │   ├── main.ts                      # Entry point
│   │   ├── App.ts                       # Main application class
│   │   │
│   │   ├── 📂 core/                     # Core Systems
│   │   │   ├── SceneManager.ts          # Three.js scene management
│   │   │   ├── CameraController.ts      # Orbit + WASD controls
│   │   │   ├── RenderLoop.ts            # Animation loop, FPS counter
│   │   │   ├── XRManager.ts             # WebXR AR/VR support
│   │   │   └── PerformanceMonitor.ts    # Real-time metrics
│   │   │
│   │   ├── 📂 splat/                    # 3DGS Rendering
│   │   │   ├── SplatRenderer.ts         # .splat file loader + renderer
│   │   │   ├── SplatMaterial.ts         # Custom shader material
│   │   │   ├── GaussianBuffer.ts        # GPU buffer management
│   │   │   └── CompressionDecoder.ts    # Decompress .splat files
│   │   │
│   │   ├── 📂 character/                # GTA AI Character
│   │   │   ├── AvatarLoader.ts          # GLTF avatar loading
│   │   │   ├── AnimationController.ts   # Mixamo animation blending
│   │   │   ├── PathfindingController.ts # A* nav-mesh pathfinding
│   │   │   ├── BehaviorTree.ts          # AI behavior system
│   │   │   ├── NarrationEngine.ts       # WebSpeech + Gemini API
│   │   │   └── CollisionDetector.ts     # Proxy mesh collision
│   │   │
│   │   ├── 📂 search/                   # Visual Search
│   │   │   ├── SearchEngine.ts          # CLIP query handler
│   │   │   ├── GaussianHighlighter.ts   # Highlight matching Gaussians
│   │   │   ├── InventoryPanel.ts        # OWL-ViT results UI
│   │   │   └── SegmentationOverlay.ts   # SAM 2 mask overlay
│   │   │
│   │   ├── 📂 ui/                       # UI Components (Stitch-generated)
│   │   │   ├── HUDOverlay.ts            # Main HUD
│   │   │   ├── SearchBar.ts             # Search input
│   │   │   ├── NarrationPanel.ts        # Narration display
│   │   │   ├── Minimap.ts               # GTA-style minimap
│   │   │   ├── StatsBar.ts              # FPS, GPU stats
│   │   │   ├── NotificationToast.ts     # Toast notifications
│   │   │   └── LoadingScreen.ts         # Progress indicator
│   │   │
│   │   ├── 📂 utils/                    # Utilities
│   │   │   ├── api.ts                   # API client
│   │   │   ├── math.ts                  # Vector/matrix helpers
│   │   │   ├── storage.ts               # LocalStorage cache
│   │   │   └── logger.ts                # Structured logging
│   │   │
│   │   └── 📂 types/                    # TypeScript types
│   │       ├── index.ts
│   │       ├── splat.ts
│   │       ├── character.ts
│   │       └── api.ts
│   │
│   ├── 📂 public/
│   │   ├── assets/
│   │   │   ├── avatar.glb               # Default character
│   │   │   └── navmesh.glb              # Navigation mesh
│   │   └── scenes/                      # Sample .splat files
│   │       └── demo.splat
│   │
│   └── 📂 tests/                        # Viewer Tests
│       ├── SplatRenderer.test.ts
│       ├── PathfindingController.test.ts
│       └── SearchEngine.test.ts
│
├── 📂 notebooks/                        # Google Colab Notebooks
│   ├── 01_colmap_pose_estimation.ipynb  # COLMAP on HF dataset
│   ├── 02_train_3dgs.ipynb              # 3DGS training
│   ├── 03_train_langsplat.ipynb         # LangSplat + CLIP
│   ├── 04_export_compress.ipynb         # Export + compress .splat
│   └── 05_full_pipeline.ipynb           # End-to-end pipeline
│
├── 📂 datasets/                         # Dataset Management
│   ├── download_hf_dataset.py           # Script to download HF datasets
│   ├── validate_dataset.py              # Validate dataset integrity
│   └── README.md                        # Dataset guide
│
├── 📂 docs/                             # Documentation
│   ├── ARCHITECTURE.md                  # System architecture
│   ├── API.md                           # API documentation
│   ├── DEPLOYMENT.md                    # Deployment guide
│   ├── CONTRIBUTING.md                  # Contribution guidelines
│   ├── PERFORMANCE.md                   # Performance optimization
│   └── TROUBLESHOOTING.md               # Common issues + fixes
│
├── 📂 scripts/                          # Automation Scripts
│   ├── setup.sh                         # Local environment setup
│   ├── deploy_viewer.sh                 # Deploy to GitHub Pages
│   ├── deploy_backend.sh                # Deploy to HF Spaces
│   ├── run_tests.sh                     # Run all tests
│   └── benchmark.sh                     # Performance benchmarks
│
├── 📂 .github/                          # GitHub CI/CD
│   └── workflows/
│       ├── ci.yml                       # Run tests on PR
│       ├── deploy_viewer.yml            # Auto-deploy viewer
│       └── deploy_backend.yml           # Auto-deploy backend
│
├── mcp_config.json                      # MCP server configuration
├── .gitignore                           # Git ignore rules
├── LICENSE                              # MIT License
├── README.md                            # Project README
├── AGENTS.md                            # AI agent instructions
└── DESIGN.md                            # Design system
```

---

## 🔥 Advanced Features (1 Cr Job-Level)

### **1. Multi-Scene Management**
- Support multiple scenes simultaneously
- Scene switching with smooth transitions
- Cloud storage integration (S3-compatible)

### **2. Real-Time Performance Monitoring**
- Prometheus metrics exposed via `/metrics`
- Real-time FPS, GPU memory, render time tracking
- Automatic quality degradation on low-end devices

### **3. Advanced AI Narration System**
- **Google Gemini 2.0 Flash** integration with caching
- WebSpeech fallback for $0 cost
- Behavior tree for intelligent character actions
- Context-aware narration (remembers previous POIs)

### **4. WebXR AR/VR Support**
- Place digital twin in real world via phone camera
- VR mode for immersive exploration
- Hit-test for surface detection

### **5. Collaborative Features (Future-Ready)**
- WebSocket support for multi-user sessions
- Shared annotations and bookmarks
- Real-time character position sync

### **6. Production-Grade Error Handling**
- Retry logic with exponential backoff
- Graceful degradation
- Detailed error logging with Sentry integration
- Health check endpoints

### **7. CI/CD Pipeline**
- Automated testing on every PR
- Auto-deployment to GitHub Pages + HF Spaces
- Performance regression detection

### **8. Comprehensive Testing**
- Unit tests for all core modules
- Integration tests for API endpoints
- E2E tests with Playwright
- Performance benchmarks

---

## 🎨 UI Design System (Google Stitch-Generated)

### **Visual Theme**
Futuristic noir / GTA HUD aesthetic. Dense information overlaid on a dark 3D scene. Glass-panel UI elements. Feels like a AAA game HUD meets a scientific instrument panel.

### **Color Palette**
| Name        | Hex       | Usage                              |
|-------------|-----------|-------------------------------------|
| Void Black  | #0D0D0D   | Scene background, main canvas       |
| Panel Dark  | #111418   | UI panels, sidebars, drawers        |
| GTA Yellow  | #F7C131   | Primary accent, waypoints, active   |
| Cyber Cyan  | #00CFFF   | Secondary accent, data readouts     |
| Kill Red    | #FF3B3B   | Errors, GPU warnings, danger states |
| Neon Green  | #39FF14   | Character health, agent active, OK  |
| Warm Ivory  | #E8E0CC   | Primary body text on dark panels    |
| Muted Slate | #888888   | Secondary labels, disabled          |

### **Typography**
- **Headings**: Rajdhani 700, uppercase, letter-spacing 2px
- **HUD labels**: Rajdhani 600, 10–11px, letter-spacing 3px, ALL CAPS
- **Data / code**: Share Tech Mono, 12–13px
- **Body**: Rajdhani 400, 14–15px, line-height 1.6
- Fallbacks: system-ui, monospace

### **Component Rules**
- Panels: `background: rgba(17,20,24,0.9)` · `border: 0.5px solid rgba(247,193,49,0.35)`
- Buttons: uppercase · letter-spacing 1px · 1px solid border in accent color
  Hover: bg opacity +10% · `box-shadow: 0 0 8px <accent>40`
- Bars (health/progress): 5–8px height · accent fill · `#1a1a1a` track · `border-radius: 2px`
- Minimap: circular 120px · GTA-style triangle waypoints · animated player dot
- Notifications: slide in bottom-right · 220px wide · auto-dismiss 2.8 s
- Scanlines overlay (optional): `repeating-linear-gradient` at 6% opacity

### **Layout Zones**
- **Top-left**: Scene title + star-rating difficulty
- **Top-right**: Circular minimap
- **Bottom bar**: Stats strip — FPS · Engine name · Cost · Scene count
- **Left sidebar**: Mission / pipeline stage selector with progress bars
- **Right panel**: Search bar + inventory list + narration caption
- **Floating**: Notification toasts, bottom-right

---

## 🤖 AI Integration — Google Gemini 2.0 Flash

### **Why Gemini 2.0 Flash:**
- **100% FREE** — 15 requests/min, 1M tokens/day
- **Vision + Text** in one API call (no separate image model)
- **No credit card required** — just Google account
- **Native JSON mode** — perfect for structured outputs
- **Fast** — ~500ms response time

### **API Setup:**
```python
# Get free API key: https://aistudio.google.com/apikey
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Vision + narration in one call
model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content([
    Image.open("screenshot.jpg"),
    "Describe this scene in 2-3 punchy sentences. Name specific objects."
])
```

### **Replaced Claude API → Gemini:**
| Feature | Claude API | Gemini 2.0 Flash |
|---------|------------|------------------|
| Cost | $0.001/msg | **FREE** |
| Vision | Yes | **Yes (native)** |
| Rate Limit | Paid tiers | 15 RPM free |
| Setup | Credit card | **Google account only** |

### **Usage in Project:**
1. **Narration Engine:** Character describes scene at each POI
2. **Visual Search Enhancement:** Gemini refines CLIP search results
3. **Object Context:** Gemini provides rich descriptions of detected objects
4. **Conversation:** Users can ask questions about the scene

---

## 🔧 MCP Configuration

### **mcp_config.json**
```json
{
  "mcpServers": {
    "stitch": {
      "serverUrl": "https://mcp.stitch.withgoogle.com/v1",
      "headers": {
        "Authorization": "Bearer ${STITCH_API_KEY}"
      }
    },
    "notion": {
      "serverUrl": "https://mcp.notion.com/mcp"
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

### **MCP Role Map:**
| Server | Used For |
|--------|----------|
| **stitch** | Generate UI components, HUD overlays, DESIGN.md extraction |
| **notion** | Architecture spec, sprint board, documentation |
| **github** | PRs, issues, codebase search, CI/CD |
| **playwright** | E2E testing of Three.js viewer and character engine |

---

## 📚 Free Datasets

### **Primary Dataset: Hugging Face `nerf-gs-datasets`**
- Pre-formatted for 3DGS
- Load in Colab: `from datasets import load_dataset; load_dataset("jxuhf/nerf-gs-datasets")`
- Multiple scenes: indoor, outdoor, object-centric
- No preprocessing needed

### **Alternative Datasets:**
| Dataset | Scenes | Best For | URL |
|---------|--------|----------|-----|
| **DTU** | ~80 | Benchmark reconstruction quality | roboimagedata.compute.dtu.dk |
| **BlendedMVS** | 113 | Generalisation to diverse environments | github.com/YoYo000/BlendedMVS |
| **Tanks & Temples** | 21 | Large-scale indoor + outdoor | tanksandtemples.org |
| **Replica / ScanNet** | Curated | Semantic annotations | github.com/facebookresearch/Replica-Dataset |

---

## 🚀 Deployment Strategy

### **Three-Tier Deployment:**

```
┌─────────────────────────────────────────────────────┐
│  TIER 1: Viewer (GitHub Pages)                      │
│  • Static Three.js app                              │
│  • CDN via jsDelivr/CDNJS                           │
│  • GitHub LFS for .splat files                      │
│  • URL: username.github.io/neotwin-viewer           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  TIER 2: Backend API (Hugging Face Spaces)          │
│  • FastAPI + Gradio                                 │
│  • Free GPU (T4) for inference                      │
│  • Auto-scaling                                     │
│  • URL: huggingface.co/spaces/username/neotwin-api  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  TIER 3: Training (Google Colab)                    │
│  • On-demand training notebooks                     │
│  • Free T4 GPU, 12-hour sessions                    │
│  • Export .splat files to GitHub LFS                │
│  • No persistent server needed                      │
└─────────────────────────────────────────────────────┘
```

### **CI/CD Pipeline (GitHub Actions):**

```yaml
# .github/workflows/deploy.yml
name: Deploy NeoTwin

on:
  push:
    branches: [main]

jobs:
  deploy-viewer:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
        working-directory: viewer
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./viewer/dist

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: huggingface/setup-cli@v2
      - run: |
          huggingface-cli upload \
            username/neotwin-api \
            ./backend .
```

---

## 📅 Execution Plan (12 Days)

### **Week 1: Core Pipeline**

| Day | Task | MCP Used | Output |
|-----|------|----------|--------|
| **1** | Setup GitHub repo + Notion workspace | Notion MCP | Project board, architecture doc |
| **2** | Generate UI with Stitch | Stitch MCP | React/TS UI components |
| **3** | Colab notebook: COLMAP + 3DGS | — | Trained .ply file |
| **4** | Colab notebook: LangSplat + CLIP | — | .splat + CLIP embeddings |
| **5** | Backend: FastAPI + Gemini API | — | /search, /narrate, /identify |
| **6** | Viewer: Three.js + SplatRenderer | — | Working 3D viewer |
| **7** | Character engine + pathfinding | — | GTA character walking |

### **Week 2: Polish + Deploy**

| Day | Task | MCP Used | Output |
|-----|------|----------|--------|
| **8** | Visual search + highlighting | — | Search bar + 3D highlights |
| **9** | Narration + WebSpeech | — | AI character speaks |
| **10** | Testing + optimization | Playwright MCP | 100+ FPS, <3s load |
| **11** | Deploy to GitHub Pages + HF Spaces | GitHub MCP | Live URLs |
| **12** | Documentation + demo video | Notion MCP | Portfolio-ready |

---

## 🔐 Security & Best Practices

### **Security Checklist:**
- [ ] `.env` files added to `.gitignore` before first commit
- [ ] No API keys hardcoded anywhere — all use `${ENV_VAR}`
- [ ] GitHub PAT is fine-grained, scoped to this repo only
- [ ] HF Spaces secrets set in Space Settings, not in app.py
- [ ] `.splat` files stored in GitHub LFS, not as regular blobs

### **Coding Standards:**
- Python 3.11 / PyTorch 2.4 / CUDA 12.1 for all training code
- TypeScript strict mode for all Three.js / character / search code
- Three.js r169+ — never use deprecated APIs
- All API keys via environment variables — never hardcoded
- Max Gemini API call: 300 tokens per narration; batch where possible

### **Rate Limiting Strategy:**
- Cache Gemini responses per location hash
- Skip repeat visits to same POI
- Batch inventory + narration into one API call per stop
- Use `max_tokens: 300` — narration needs 2–3 sentences max

---

## 📊 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Rendering FPS** | 100+ FPS | Browser DevTools |
| **Scene Load Time** | < 3 seconds | Network tab |
| **CLIP Query Response** | < 500 ms | API latency |
| **Character Animation** | 60 FPS | Animation mixer |
| **Memory Usage** | < 512 MB | Browser task manager |
| **`.splat` File Size** | ≤ 8 MB | File size after compression |
| **Gemini API Cost** | $0 | Free tier usage |

---

## 📝 Technology Stack Summary

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| 3DGS Core | gaussian-splatting | latest | graphdeco-inria/gaussian-splatting |
| Semantic 3D | LangSplat | latest | CLIP baked into each Gaussian |
| Mesh export | SuGaR / GOF | latest | Textured .glb from Gaussians |
| Compression | gsplat | 1.3.1+ | 300 MB → 8 MB |
| SfM Poses | pycolmap / HLoc | 3.10.0 | Camera pose estimation |
| 3D viewer | Three.js | r169+ | WebGL splat renderer |
| Splat Loader | @sparkjoy/splat | 0.3+ | antimatter15 algorithm |
| Avatar | ReadyPlayerMe | GLTF 2.0 | Free custom avatars |
| Animations | Mixamo | — | Free motion capture library |
| Pathfinding | three-pathfinding | 0.8+ | A* on baked nav-mesh |
| Object Detect | OWL-ViT 2 | — | google/owlvit-large-patch14 |
| Segmentation | SAM 2 | — | facebook/sam2-hiera-large |
| CLIP | OpenAI CLIP | ViT-L/14 | Text → 512-d vector |
| LLM | **Gemini 2.0 Flash** | latest | Character brain (FREE) |
| Speech | WebSpeech API | native | Browser TTS, $0 |
| Physics | Rapier WASM | 0.14+ | Optional collision |
| Frontend UI | Stitch-generated + shadcn/ui | latest | Control panel |
| Backend | FastAPI + Gradio | 4.44+ | HF Spaces app |
| Training GPU | Google Colab T4 | — | Free tier |
| Backend Host | Hugging Face Spaces | — | Free GPU runtime |
| Viewer Host | GitHub Pages + LFS | — | Free static CDN |
| IDE | Google Antigravity | 1.20.5+ | Claude Sonnet/Opus |
| UI Design | Google Stitch | — | MCP-connected |
| Knowledge | Notion | — | MCP-connected |

---

## 🎯 Success Metrics

### **Technical:**
- [ ] 100+ FPS rendering on modern browsers
- [ ] Scene loads in < 3 seconds on 4G
- [ ] Visual search accuracy > 85% on test queries
- [ ] Character pathfinding works on all scene types
- [ ] Zero API costs for AI narration

### **Portfolio:**
- [ ] Live demo URL (GitHub Pages + HF Spaces)
- [ ] Complete source code on GitHub
- [ ] Architecture documentation
- [ ] Performance benchmarks
- [ ] Demo video (2-3 min walkthrough)

### **Interview-Ready:**
- [ ] Can explain 3DGS math intuitively
- [ ] Can discuss LangSplat CLIP integration
- [ ] Can walk through deployment architecture
- [ ] Can discuss tradeoffs (NeRF vs 3DGS, etc.)
- [ ] Can demonstrate real-time performance

---

## 📞 Quick Reference Links

| Resource | URL |
|----------|-----|
| **Gemini API Key** | https://aistudio.google.com/apikey |
| **GitHub Token** | https://github.com/settings/tokens |
| **Hugging Face Token** | https://huggingface.co/settings/tokens |
| **Stitch MCP** | https://stitch.withgoogle.com |
| **Notion MCP** | https://mcp.notion.com/mcp |
| **Google Colab** | https://colab.research.google.com |
| **Hugging Face Datasets** | https://huggingface.co/datasets/jxuhf/nerf-gs-datasets |
| **ReadyPlayerMe** | https://readyplayer.me |
| **Mixamo** | https://mixamo.com |
| **3DGS Paper** | https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/ |
| **LangSplat** | https://github.com/minghanqin/LangSplat |
| **gsplat** | https://github.com/nerfstudio-project/gsplat |

---

*Last updated: May 2026*
*Stack: 3DGS · LangSplat · Three.js · ReadyPlayerMe · Mixamo · OWL-ViT · SAM 2 · Gemini 2.0 Flash · HF Spaces · Google Stitch*
*Target: Production-ready, ₹1 Cr job-level portfolio project*
