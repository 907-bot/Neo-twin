# 🚀 NeoTwin — Complete Starting Guide

## 📖 TABLE OF CONTENTS

1. [What is This Project?](#1-what-is-this-project)
2. [3D Deep Learning Explained](#2-3d-deep-learning-explained)
3. [Complete Tech Stack](#3-complete-tech-stack)
4. [How Everything Connects](#4-how-everything-connects)
5. [Step-by-Step Starting Guide](#5-step-by-step-starting-guide)
6. [Order of Operations](#6-order-of-operations)
7. [Common Questions](#7-common-questions)

---

## 1. WHAT IS THIS PROJECT?

### The Simple Explanation:

You take 50-300 photos of a room with your phone → NeoTwin turns them into a **3D video game environment** → You walk through it in your browser → An AI character explores with you and tells you what it sees.

### Real-World Example:

1. You photograph your living room
2. NeoTwin creates a 3D model
3. You open a website and see your room in 3D
4. An AI character walks around saying: "I see a red sofa, a coffee table with a laptop, and a plant near the window"
5. You type "find the laptop" → It highlights the laptop in yellow
6. The character walks to it and describes it

### Why This is Impressive:

- **Traditional 3D scanning** costs $3000+ and needs special equipment
- **NeRF** (previous tech) renders at 1 FPS (slideshow speed)
- **NeoTwin** renders at 100+ FPS (smooth as a video game)
- **AI character** understands the scene and talks about it
- **100% FREE** — no hosting, GPU, or AI costs

---

## 2. 3D DEEP LEARNING EXPLAINED

### What is 3D Deep Learning?

**2D Deep Learning:** AI that understands flat images
- Input: Photo (height × width × 3 colors)
- Output: "This is a cat" (classification)

**3D Deep Learning:** AI that understands 3D space
- Input: Multiple photos or 3D data
- Output: "This is a 3D room with a chair at position (1.2, 0.5, 3.4)"

### The Evolution of 3D AI:

```
2017: PointNet — Classify 3D point clouds
       ↓
2020: NeRF — Create 3D from photos (but slow: 1 FPS)
       ↓
2023: 3D Gaussian Splatting — Create 3D from photos (fast: 100+ FPS) ← WE USE THIS
       ↓
2024: LangSplat — Add text understanding to 3D ← WE USE THIS
```

### Key 3D Concepts:

#### **Point Cloud:**
- What: Collection of (x, y, z) points
- Like: A cloud of dots in 3D space
- Used by: LiDAR scanners, 3D sensors

#### **Mesh:**
- What: Triangles connected to form surfaces
- Like: Video game models
- Used by: Unity, Unreal Engine

#### **NeRF (Neural Radiance Fields):**
- What: Neural network that "memorizes" a scene
- Pros: Photorealistic
- Cons: Very slow (1 FPS), can't edit

#### **3D Gaussian Splatting (3DGS):**
- What: Thousands of 3D "blobs" (Gaussians) with color
- Each Gaussian has:
  - Position (where it is)
  - Shape (how big and oriented)
  - Color (RGB)
  - Opacity (how transparent)
- Pros: Fast (100+ FPS), editable, searchable
- Cons: Large file size (we compress it)

### Why 3DGS is Revolutionary:

| Feature | NeRF | 3DGS |
|---------|------|------|
| Training Time | 6-12 hours | 10-20 minutes |
| Rendering Speed | 1 FPS | 100+ FPS |
| Editable | No | Yes |
| Searchable | No | Yes (with LangSplat) |
| File Size | 100 MB | 300 MB (compressed to 8 MB) |

---

## 3. COMPLETE TECH STACK

### LAYER 1: 3D Reconstruction (Creating the Scene)

```
Your Photos → COLMAP → 3DGS Training → LangSplat → .splat File
```

| Tool | Purpose | How It Works |
|------|---------|--------------|
| **COLMAP** | Finds camera positions | Matches features across photos, calculates where each photo was taken |
| **3DGS** | Creates 3D scene | Optimizes thousands of Gaussians to match your photos |
| **LangSplat** | Adds semantic meaning | Embeds CLIP vectors into each Gaussian so they "know" what they are |
| **gsplat** | Compresses file | Reduces 300MB → 8MB for web delivery |

### LAYER 2: AI Models (Understanding the Scene)

```
Text Query → CLIP → Find Matching Gaussians → Gemini Describes → WebSpeech Speaks
```

| Model | Purpose | Cost |
|-------|---------|------|
| **Google Gemini 2.0 Flash** | AI that sees images and talks | FREE (15 RPM) |
| **CLIP (OpenAI)** | Converts text to vectors | FREE (open-source) |
| **OWL-ViT** | Detects objects in images | FREE (open-source) |
| **SAM 2 (Meta)** | Segments objects at click | FREE (open-source) |

### LAYER 3: Frontend (What Users See)

```
Browser → Three.js → Loads .splat → Renders at 100+ FPS → User Interacts
```

| Technology | Purpose | Why |
|------------|---------|-----|
| **Three.js** | 3D rendering in browser | Most popular WebGL library |
| **TypeScript** | JavaScript with types | Catches errors before runtime |
| **@sparkjoy/splat** | Renders .splat files | Optimized for 3DGS |
| **Vite** | Build tool | Fast dev server, instant HMR |

### LAYER 4: Backend (API Server)

```
User Request → FastAPI → Gemini/CLIP/OWL-ViT → Response → User
```

| Technology | Purpose | Why |
|------------|---------|-----|
| **FastAPI** | Python web framework | Fast, async, auto-generates docs |
| **PyTorch** | Deep learning | Industry standard, GPU support |
| **Gradio** | Demo UI | Easy ML model interface |

### LAYER 5: Deployment (Where It Lives)

```
Colab (Training) → GitHub LFS (Storage) → GitHub Pages (Viewer) + HF Spaces (API)
```

| Service | Hosts | Cost |
|---------|-------|------|
| **Google Colab** | Training notebooks | FREE (T4 GPU) |
| **Hugging Face Spaces** | Backend API | FREE (T4 GPU) |
| **GitHub Pages** | Viewer website | FREE |
| **GitHub LFS** | .splat files | FREE (1GB) |

---

## 4. HOW EVERYTHING CONNECTS

### Complete Data Flow:

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: USER UPLOADS PHOTOS                                  │
│ 100-300 smartphone photos                                    │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: COLMAP (Google Colab)                                │
│ • Finds camera positions for each photo                      │
│ • Creates sparse point cloud                                 │
│ Output: sparse/ folder with camera poses                     │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: 3DGS TRAINING (Google Colab)                         │
│ • Creates 3D Gaussians from photos + camera poses            │
│ • Optimizes for 30,000 iterations (~10 min on T4)            │
│ Output: point_cloud.ply (~300MB)                             │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: LANGSPLAT TRAINING (Google Colab)                    │
│ • Embeds CLIP vectors into each Gaussian                     │
│ • Now each Gaussian "knows" what it represents               │
│ Output: langsplat.ckpt with CLIP features                    │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: COMPRESSION (Google Colab)                           │
│ • Compresses 300MB → 8MB using gsplat                        │
│ Output: scene_compressed.splat (8MB)                         │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 6: DEPLOY TO GITHUB PAGES                               │
│ • Upload .splat to GitHub LFS                                │
│ • Viewer loads it in browser                                 │
│ Output: username.github.io/neotwin-viewer                    │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 7: USER INTERACTS                                       │
│ • Opens website, sees 3D scene                               │
│ • Types "find red chair"                                     │
│ • Backend receives query                                     │
│ • CLIP encodes "red chair" to vector                         │
│ • LangSplat finds matching Gaussians                         │
│ • Viewer highlights them in yellow                           │
│ • Character walks to result                                  │
│ • Gemini describes what it sees                              │
│ • WebSpeech speaks the description                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. STEP-BY-STEP STARTING GUIDE

### ORDER OF OPERATIONS (Follow This Exactly):

```
PHASE 1: Setup (Day 1)
  ↓
PHASE 2: Train First Scene (Day 2-3)
  ↓
PHASE 3: Run Viewer Locally (Day 4)
  ↓
PHASE 4: Connect Backend (Day 5)
  ↓
PHASE 5: Deploy (Day 6-7)
  ↓
PHASE 6: Refine UI + Polish (Day 8-12)
```

---

### PHASE 1: SETUP (Day 1)

**Step 1.1: Get Free API Keys**

1. **Gemini API Key:**
   - Go to: https://aistudio.google.com/apikey
   - Click "Create API Key"
   - Copy the key (starts with `AIza...`)

2. **GitHub Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select: `repo`, `workflow`, `write:packages`
   - Copy the token (starts with `ghp_...`)

3. **Hugging Face Token:**
   - Go to: https://huggingface.co/settings/tokens
   - Click "New token"
   - Select: `Read` and `Write`
   - Copy the token (starts with `hf_...`)

**Step 1.2: Setup Backend Environment**

```bash
cd D:\3D-Deeplearning\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file in `backend/`:
```
GEMINI_API_KEY=your_gemini_key_here
HUGGINGFACE_TOKEN=your_hf_token_here
```

**Step 1.3: Setup Viewer Environment**

```bash
cd D:\3D-Deeplearning\viewer
npm install
```

---

### PHASE 2: TRAIN FIRST SCENE (Day 2-3)

**Step 2.1: Open Google Colab**

1. Go to: https://colab.research.google.com
2. Upload `notebooks/01_colmap_pose_estimation.ipynb`
3. Change runtime to GPU: Runtime → Change runtime type → T4 GPU

**Step 2.2: Run Notebooks in Order**

1. **Notebook 01:** COLMAP pose estimation
   - Downloads dataset from Hugging Face
   - Runs COLMAP to find camera positions
   - Downloads `sparse_output.zip`

2. **Notebook 02:** 3DGS training
   - Clones gaussian-splatting repo
   - Trains for 30,000 iterations (~10 min)
   - Downloads `point_cloud.ply` (~300MB)

3. **Notebook 03:** LangSplat training
   - Clones LangSplat repo
   - Trains with CLIP features (~5 min)
   - Downloads `langsplat.ckpt`

4. **Notebook 04:** Export + compress
   - Compresses to `.splat` format
   - Downloads `scene_compressed.splat` (~8MB)

**Step 2.3: Place Files in Viewer**

```
Copy scene_compressed.splat → viewer/public/scenes/demo.splat
```

---

### PHASE 3: RUN VIEWER LOCALLY (Day 4)

**Step 3.1: Start Viewer**

```bash
cd D:\3D-Deeplearning\viewer
npm run dev
```

This opens: http://localhost:3000

**Step 3.2: Test Basic Features**

- [ ] Scene loads (you should see 3D environment)
- [ ] WASD keys move camera
- [ ] FPS counter shows 100+
- [ ] Search bar appears in top-right

---

### PHASE 4: CONNECT BACKEND (Day 5)

**Step 4.1: Start Backend**

```bash
cd D:\3D-Deeplearning\backend
venv\Scripts\activate
python app.py
```

This starts at: http://localhost:7860

**Step 4.2: Test API**

Open: http://localhost:7860/docs

You should see FastAPI auto-generated documentation.

Test endpoints:
- GET `/api/v1/health` — Should return system info
- POST `/api/v1/search` — Test with `{"query": "chair"}`

**Step 4.3: Test Search in Viewer**

1. Open viewer: http://localhost:3000
2. Type "chair" in search bar
3. Press Enter
4. Should highlight matching Gaussians

---

### PHASE 5: DEPLOY (Day 6-7)

**Step 5.1: Push to GitHub**

```bash
cd D:\3D-Deeplearning
git init
git remote add origin https://github.com/YOUR_USERNAME/neotwin.git
git add .
git commit -m "feat: initial NeoTwin project"
git push -u origin main
```

**Step 5.2: Deploy Viewer to GitHub Pages**

1. Go to GitHub repo → Settings → Pages
2. Source: `gh-pages` branch
3. URL: `https://YOUR_USERNAME.github.io/neotwin`

**Step 5.3: Deploy Backend to Hugging Face**

1. Create Space at: https://huggingface.co/new-space
2. Name: `neotwin-api`
3. SDK: Docker
4. Push backend:
```bash
huggingface-cli upload YOUR_USERNAME/neotwin-api ./backend .
```

**Step 5.4: Set Secrets in HF Spaces**

Go to Space Settings → Variables and secrets:
- `GEMINI_API_KEY`: Your Gemini key
- `HUGGINGFACE_TOKEN`: Your HF token

---

### PHASE 6: REFINE UI + POLISH (Day 8-12)

**Step 6.1: Generate UI with Stitch MCP**

1. Load Stitch MCP in Antigravity
2. Generate HUD components
3. Replace placeholder UI in `viewer/index.html`

**Step 6.2: Add Character**

1. Download avatar from ReadyPlayerMe
2. Download animations from Mixamo
3. Place in `viewer/public/assets/`

**Step 6.3: Test Everything**

- [ ] Scene loads in < 3 seconds
- [ ] 100+ FPS rendering
- [ ] Search works
- [ ] Character walks
- [ ] Narration speaks
- [ ] Works on mobile

---

## 6. ORDER OF OPERATIONS

### DO THIS FIRST (Priority Order):

1. ✅ Get API keys (15 minutes)
2. ✅ Setup backend + viewer locally (30 minutes)
3. ✅ Run Colab notebooks to get .splat file (2-3 hours)
4. ✅ Test viewer locally (30 minutes)
5. ✅ Test backend API (30 minutes)
6. ✅ Deploy to GitHub + HF Spaces (1 hour)
7. ✅ Refine UI with Stitch (2-3 hours)
8. ✅ Add character + animations (2 hours)
9. ✅ Test end-to-end (1 hour)
10. ✅ Create demo video (1 hour)

---

## 7. COMMON QUESTIONS

### Q: Do I need a GPU?
**A:** No! All training runs on Google Colab (free T4 GPU). Your local machine only runs the viewer (uses your GPU for rendering, but any modern GPU works).

### Q: How much does this cost?
**A:** $0. Everything is free: Colab, HF Spaces, GitHub Pages, Gemini API.

### Q: How long to build?
**A:** 12 days if you follow the guide. First working version in 4 days.

### Q: Can I use my own photos?
**A:** Yes! Start with HF datasets for learning, then use your own photos.

### Q: What if Colab disconnects?
**A:** Training checkpoints are saved. Just resume from last checkpoint.

### Q: How do I make the UI beautiful?
**A:** Use Stitch MCP to generate components. The current UI is functional but basic.

### Q: Can I deploy this commercially?
**A:** Yes, MIT license. For production, add authentication, rate limiting, and paid GPU.

### Q: What jobs can this get me?
**A:** 3D ML Engineer, Computer Vision Engineer, Graphics Engineer, AI Research Engineer. Salary range: ₹30L - ₹1Cr+ depending on company.

---

## 📚 LEARNING RESOURCES

### For 3D Deep Learning Mastery:

1. **Read:** `docs/3D_DEEP_LEARNING_GUIDE.md` (12-week curriculum)
2. **Watch:** Two Minute Papers YouTube channel
3. **Practice:** Run all Colab notebooks
4. **Build:** This NeoTwin project end-to-end
5. **Read Papers:**
   - 3D Gaussian Splatting (SIGGRAPH 2023)
   - LangSplat (CVPR 2024)
   - NeRF (ECCV 2020)

---

## 🎯 YOUR IMMEDIATE NEXT STEPS

### RIGHT NOW (Next 2 Hours):

1. **Get Gemini API Key** → https://aistudio.google.com/apikey
2. **Setup Backend** → `cd backend && pip install -r requirements.txt`
3. **Setup Viewer** → `cd viewer && npm install`
4. **Open Colab** → Upload `notebooks/01_colmap_pose_estimation.ipynb`

### TODAY:

- Run Notebook 01 (COLMAP)
- Run Notebook 02 (3DGS training)
- Download `.splat` file
- Place in `viewer/public/scenes/`

### TOMORROW:

- Run viewer locally
- Test search functionality
- Start backend
- Connect viewer to backend

---

**You have everything you need. Start with Phase 1 and follow the steps in order.**
