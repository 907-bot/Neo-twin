---
name: 3dgs-digital-twin-gta-creator
description: >
  Master skill for the "Personal 3D Digital Twin Creator" project — a
  full end-to-end pipeline that turns smartphone photos/video into a
  photorealistic, interactive 3D scene rendered at 100+ FPS in a browser,
  with a GTA-style animated AI character that walks through the scene,
  identifies objects, narrates findings, and supports visual search.

  ALWAYS use this skill when working on any part of this project:
  3D Gaussian Splatting (3DGS), COLMAP / Structure-from-Motion, LangSplat,
  Mip-Splatting, Three.js splat viewer, animated GLTF character (ReadyPlayerMe
  / Mixamo), A* pathfinding, LLM narration via Claude API, OWL-ViT / SAM 2
  visual search, Hugging Face Spaces deployment, Gradio Model3D interface,
  or ANY Antigravity MCP configuration (Stitch, Notion, GitHub, Firebase,
  Playwright, Filesystem). Also trigger on: datasets (DTU, BlendedMVS,
  nerf-gs-datasets), free GPU training (Colab, Kaggle), mcp_config.json
  setup, AGENTS.md, DESIGN.md, or wiring any MCP server in Antigravity.

compatibility:
  tools: [bash, create_file, str_replace, view]
  environment: >
    Google Antigravity v1.20.5+ with Claude Sonnet 4.6 / Opus 4.6.
    Python 3.11, PyTorch 2.4, CUDA 12.1 for training scripts.
    Node 20+ for Three.js viewer and MCP servers.
---

# 3D Digital Twin Creator — Master Project SKILL

## Project North Star

> **Goal:** A user uploads 50–300 smartphone photos or a 4K video.
> The pipeline reconstructs a photorealistic 3D scene rendered at 100+ FPS
> in a web browser. A GTA-style animated character walks through the scene,
> identifies every object using CLIP + OWL-ViT, narrates findings via Claude
> API (spoken with WebSpeech), and lets the user type a query ("red chair")
> to highlight matching Gaussians in 3D space.
> **Total cost: $0. Hosting: Hugging Face Spaces + GitHub Pages.**

---

## Table of Contents

1. [Project Architecture](#1-project-architecture)
2. [Pipeline at a Glance](#2-pipeline-at-a-glance)
3. [Mission 01 — Data Capture](#3-mission-01--data-capture)
4. [Mission 02 — SfM + Camera Poses](#4-mission-02--sfm--camera-poses)
5. [Mission 03 — 3DGS Training](#5-mission-03--3dgs-training)
6. [Mission 04 — GTA AI Character Engine](#6-mission-04--gta-ai-character-engine)
7. [Mission 05 — Visual Search](#7-mission-05--visual-search)
8. [Mission 06 — Web Deployment](#8-mission-06--web-deployment)
9. [Free Datasets](#9-free-datasets)
10. [Antigravity MCP Configuration](#10-antigravity-mcp-configuration)
11. [AGENTS.md Template](#11-agentsmd-template)
12. [DESIGN.md Template](#12-designmd-template)
13. [Full Technology Stack](#13-full-technology-stack)
14. [Security & Cost Rules](#14-security--cost-rules)
15. [Reference File Map](#15-reference-file-map)

---

## 1. Project Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                      │
│   Browser: Three.js Splat Viewer + GTA Character Overlay         │
│   Controls: WASD/Joystick · Text Search Bar · LLM Chat Panel     │
└─────────────────────────┬────────────────────────────────────────┘
                          │  WebGL / WebXR
┌─────────────────────────▼────────────────────────────────────────┐
│                       3DGS SCENE LAYER                           │
│   .splat / .ply file  ←  LangSplat CLIP 512-d vectors baked in  │
│   Renderer: antimatter15/splat  +  Three.js r169+                │
└──────────┬──────────────────────────────┬────────────────────────┘
           │                              │
    ┌──────▼────────┐             ┌───────▼────────────┐
    │  GTA AGENT    │             │   VISUAL SEARCH    │
    │  GLTF Avatar  │             │   CLIP text query  │
    │  Mixamo anims │             │   OWL-ViT detect   │
    │  A* pathfind  │             │   SAM 2 segment    │
    │  Claude brain │             │   Gaussian hilite  │
    │  WebSpeech    │             └────────────────────┘
    └──────┬────────┘
           │
┌──────────▼───────────────────────────────────────────────────────┐
│                  HF SPACES BACKEND  (Gradio + FastAPI)           │
│   /reconstruct  →  COLMAP  →  3DGS train  →  export .splat      │
│   /search       →  LangSplat CLIP query   →  Gaussian indices    │
│   /identify     →  OWL-ViT inference      →  object inventory   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Pipeline at a Glance

| # | Mission | Core Tool | Free Compute | Output |
|---|---|---|---|---|
| 01 | Capture | Smartphone / ffmpeg | — | 100–300 JPEG frames |
| 02 | SfM + Camera Poses | COLMAP / HLoc | Colab T4 | sparse/ point cloud |
| 03 | 3DGS + LangSplat | gaussian-splatting | Colab T4 / A100 | .ply + .splat + CLIP vecs |
| 04 | GTA Character | Three.js + Claude API | Browser | animated AI guide |
| 05 | Visual Search | CLIP + OWL-ViT + SAM 2 | HF Spaces | 3D object highlights |
| 06 | Deploy | HF Spaces + GitHub Pages | Free tier | live URL, shareable |

---

## 3. Mission 01 — Data Capture

### Capture Rules
- Shoot **4K 60fps** — any modern smartphone (iPhone 12+, Pixel 6+)
- **≥70% frame overlap** — walk slowly, constant speed
- Complete **3 passes** over the scene:
  1. Perimeter at eye level (full circle around object/room)
  2. 45° tilted-down pass (captures top surfaces — commonly missed)
  3. Close-up detail pass for key objects
- Target **100–300 usable frames** after extraction

### Frame Extraction (ffmpeg — Free)
```bash
# 2 fps  — good for slow walkthroughs
ffmpeg -i video.mp4 -vf fps=2 frames/%04d.jpg

# 4 fps  — for faster-moving captures
ffmpeg -i video.mp4 -vf fps=4 frames/%04d.jpg

# Resize to 1920×1080 if Colab runs out of VRAM
ffmpeg -i video.mp4 -vf "fps=2,scale=1920:1080" frames/%04d.jpg
```

### Quick-Start Mobile Option
**KIRI Engine** (iOS / Android, free) handles capture + built-in COLMAP +
basic 3D export. Use for rapid prototyping before the full pipeline.

### Dataset Alternatives — See [Section 9](#9-free-datasets)

---

## 4. Mission 02 — SfM + Camera Poses

### What SfM Produces
- `sparse/0/cameras.bin` — intrinsics for each camera
- `sparse/0/images.bin`  — extrinsics (position + rotation) per frame
- `sparse/0/points3D.bin` — initial sparse point cloud (input seed for 3DGS)

### Option A: COLMAP (Standard — Best Accuracy)
```bash
pip install pycolmap --break-system-packages

# 1. Feature extraction
colmap feature_extractor \
  --image_path data/images \
  --database_path data/database.db \
  --ImageReader.camera_model OPENCV

# 2. Matching (exhaustive for ≤200 images)
colmap exhaustive_matcher --database_path data/database.db

# 3. Sparse reconstruction
colmap mapper \
  --database_path data/database.db \
  --image_path data/images \
  --output_path data/sparse
```

### Option B: HLoc (Harder Scenes — Dark / Repetitive Textures)
```bash
pip install hloc --break-system-packages
# SuperPoint (deep keypoints) + SuperGlue (graph neural matching)
# github.com/cvg/Hierarchical-Localization
# Produces same sparse/ folder format as COLMAP
```

### Colab Notebook Generation Prompt
```
"Write a complete Google Colab notebook that:
 1. Installs pycolmap on a T4 runtime
 2. Accepts a .zip of images uploaded via google.colab.files.upload()
 3. Runs COLMAP feature_extractor, exhaustive_matcher, and mapper
 4. Zips the sparse/ output and triggers a download
 Optimised for the gaussian-splatting repo input format."
```

---

## 5. Mission 03 — 3DGS Training

### Base: 3D Gaussian Splatting
```bash
git clone https://github.com/graphdeco-inria/gaussian-splatting --recursive
cd gaussian-splatting
pip install -e . --break-system-packages

# Train — 30k iterations ≈ 10–20 min on T4
python train.py -s data/scene --iterations 30000

# Output: output/<scene>/point_cloud/iteration_30000/point_cloud.ply
```

### Upgrade 1: Mip-Splatting (Always Use for Final Builds)
- Repo: `github.com/autonomousvision/mip-splatting`
- Anti-aliased Gaussians — eliminates dilation artifacts at any zoom
- Drop-in replacement; same CLI interface as base 3DGS

### Upgrade 2: LangSplat (Required for Mission 05 Visual Search)
Embeds a **512-dim CLIP vector** into every Gaussian during training.
```bash
git clone https://github.com/minghanqin/LangSplat
# Run after 3DGS converges — adds ~5 min on T4
python train.py \
  -s data/scene \
  --start_checkpoint output/scene/ckpt30000.pth \
  --feature_level 3
```

### Mesh Export (for Gradio Model3D .glb display)
```bash
# SuGaR — clean textured .glb from Gaussians
pip install sugar-scene --break-system-packages
python train_full_pipeline.py -s data/scene -c output/scene

# GOF — better watertight geometry (complex interiors)
# github.com/autonomousvision/gaussian-opacity-fields
```

### Compress for Web Delivery
```bash
pip install gsplat --break-system-packages
python -c "
from gsplat import compress
compress(
  'output/scene/point_cloud.ply',
  'output/scene/scene_compressed.splat',
  target_size_mb=8
)
"
# Typical result: 300 MB → 6–10 MB
```

---

## 6. Mission 04 — GTA AI Character Engine

### Character Setup (Three.js + ReadyPlayerMe)
```javascript
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
let mixer, walkAction, idleAction;

loader.load('avatar.glb', (gltf) => {
  const character = gltf.scene;
  scene.add(character);

  mixer = new THREE.AnimationMixer(character);
  // Mixamo animation clips baked into avatar.glb
  idleAction = mixer.clipAction(gltf.animations.find(a => a.name === 'Idle'));
  walkAction = mixer.clipAction(gltf.animations.find(a => a.name === 'Walk'));
  idleAction.play();
});

// Update mixer in animation loop
function animate() {
  requestAnimationFrame(animate);
  const delta = clock.getDelta();
  if (mixer) mixer.update(delta);
  renderer.render(scene, camera);
}
```

### Free Avatar + Animation Sources
| Resource | URL | Cost | Format |
|---|---|---|---|
| ReadyPlayerMe | readyplayer.me | Free | GLTF/GLB with skeleton |
| Mixamo | mixamo.com | Free | FBX → convert to GLTF |
| Sketchfab CC0 | sketchfab.com/tags/cc0 | Free | GLTF |

### Navigation: A* Pathfinding on Nav-Mesh
```javascript
import { Pathfinding } from 'three-pathfinding';

const pathfinding = new Pathfinding();
const ZONE = 'scene';

// Build nav-mesh from scene floor geometry (bake in Blender or use recast-wasm)
pathfinding.setZoneData(ZONE, Pathfinding.createZone(navMeshGeometry));

function moveCharacterTo(targetPosition) {
  const groupID = pathfinding.getGroup(ZONE, character.position);
  const path = pathfinding.findPath(character.position, targetPosition, ZONE, groupID);
  if (path && path.length > 0) followPath(path);
}

function followPath(waypoints) {
  let i = 0;
  walkAction.play(); idleAction.stop();
  const interval = setInterval(() => {
    if (i >= waypoints.length) {
      clearInterval(interval);
      idleAction.play(); walkAction.stop();
      onArrived(character.position); // triggers narration
      return;
    }
    character.position.lerp(waypoints[i], 0.08);
    character.lookAt(waypoints[i]);
    i++;
  }, 16);
}
```

### LLM Brain: Claude API Vision + WebSpeech Narration
```javascript
// Called when character arrives at each Point of Interest
async function narrateCurrentView() {
  // Capture character's current viewpoint as JPEG base64
  const screenshotBase64 = captureViewportBase64(renderer, camera);

  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 300,
      messages: [{
        role: "user",
        content: [
          {
            type: "image",
            source: { type: "base64", media_type: "image/jpeg", data: screenshotBase64 }
          },
          {
            type: "text",
            text: `You are a GTA-style character exploring a 3D digital twin.
Describe what you see in 2–3 short, punchy sentences. Name specific objects,
materials, and spatial relationships. Speak in first person. No markdown.`
          }
        ]
      }]
    })
  });

  const data = await response.json();
  const narration = data.content[0].text;

  // Speak aloud
  const utterance = new SpeechSynthesisUtterance(narration);
  utterance.rate = 0.95;
  speechSynthesis.speak(utterance);

  return narration;
}
```

### Character Behavior Tree
```
IDLE
  │ player triggers move / auto-tour starts
  ▼
WALK → A* path to next POI centroid
  │ arrived within 0.8 units
  ▼
LOOK_AROUND → play look_around Mixamo clip
  │ capture 360° screenshots (4 angles)
  ▼
IDENTIFY → send best screenshot to Claude API
  │ receive narration text
  ▼
NARRATE → WebSpeech API speaks, caption shown in HUD
  │ next POI queued
  ▼
WALK → ...
```

### WASD + Click-to-Move Controls
```javascript
// Keyboard
const keys = {};
document.addEventListener('keydown', e => keys[e.key] = true);
document.addEventListener('keyup',   e => keys[e.key] = false);

function processInput() {
  const speed = 0.04;
  const dir = new THREE.Vector3();
  if (keys['w'] || keys['ArrowUp'])    dir.z -= speed;
  if (keys['s'] || keys['ArrowDown'])  dir.z += speed;
  if (keys['a'] || keys['ArrowLeft'])  dir.x -= speed;
  if (keys['d'] || keys['ArrowRight']) dir.x += speed;
  character.position.add(dir.applyQuaternion(camera.quaternion));
}

// Click-to-move via raycasting
renderer.domElement.addEventListener('click', (e) => {
  const raycaster = new THREE.Raycaster();
  raycaster.setFromCamera(getNDC(e, renderer), camera);
  const hits = raycaster.intersectObjects(floorObjects);
  if (hits.length > 0) moveCharacterTo(hits[0].point);
});
```

---

## 7. Mission 05 — Visual Search

### LangSplat CLIP Query (Text → Top-K Gaussians)
```python
import torch, clip
from langsplat import LangSplatScene

model, _ = clip.load("ViT-L/14", device="cuda")
scene    = LangSplatScene.load("output/scene/langsplat.ckpt")

def search_scene(query: str, top_k: int = 500) -> list[int]:
    tokens = clip.tokenize([query]).to("cuda")
    with torch.no_grad():
        text_vec = model.encode_text(tokens)
        text_vec /= text_vec.norm(dim=-1, keepdim=True)
    sims = (scene.clip_features @ text_vec.T).squeeze()
    return sims.topk(top_k).indices.cpu().tolist()
```

### Highlight Gaussians in Three.js Viewer
```javascript
// POST /search returns { indices: [i0, i1, ...], centroid: {x,y,z} }
async function visualSearch(query) {
  const res  = await fetch('/search', {
    method: 'POST',
    body: JSON.stringify({ query }),
    headers: { 'Content-Type': 'application/json' }
  });
  const { indices, centroid } = await res.json();

  // Glow effect on matching Gaussians
  indices.forEach(idx => {
    splatRenderer.setGaussianColor(idx, 0xF7C131);  // GTA yellow
    splatRenderer.setGaussianScale(idx, 1.4);
  });

  // Character walks to result
  moveCharacterTo(new THREE.Vector3(centroid.x, centroid.y, centroid.z));

  // Reset after 6 s
  setTimeout(() => indices.forEach(idx => splatRenderer.resetGaussian(idx)), 6000);
}
```

### OWL-ViT — Scene Inventory Builder
```python
from transformers import pipeline as hf_pipeline

detector = hf_pipeline(
  "zero-shot-object-detection",
  model="google/owlvit-large-patch14",
  device=0
)

DEFAULT_LABELS = [
  "chair","table","lamp","sofa","window","door",
  "plant","monitor","keyboard","shelf","painting","rug","bed"
]

def build_inventory(pil_image, labels=DEFAULT_LABELS) -> list[dict]:
  results = detector(pil_image, candidate_labels=labels)
  return [
    {"label": r["label"], "confidence": round(r["score"], 3), "box": r["box"]}
    for r in results if r["score"] > 0.20
  ]
```

### SAM 2 — Click-to-Segment + Export as .glb
```python
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

predictor = SAM2ImagePredictor(build_sam2("sam2_hiera_large.pt"))

def segment_at_click(pil_image, click_x: int, click_y: int):
  predictor.set_image(pil_image)
  masks, scores, _ = predictor.predict(
    point_coords=[[click_x, click_y]],
    point_labels=[1],
    multimask_output=False
  )
  return masks[0]  # Binary mask → extract Gaussian subset → export .glb
```

---

## 8. Mission 06 — Web Deployment

### GitHub Pages — Static Splat Viewer (Free)
```html
<!-- index.html  — deploy to gh-pages branch -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>3D Digital Twin</title>
  <style>body{margin:0;overflow:hidden;background:#000}</style>
</head>
<body>
  <canvas id="canvas"></canvas>
  <div id="progress" style="position:fixed;top:50%;left:50%;
    transform:translate(-50%,-50%);color:#F7C131;font-family:monospace;
    font-size:20px">Loading 0%</div>

  <script type="module">
    import * as SPLAT from "https://cdn.jsdelivr.net/npm/@sparkjoy/splat@0.3/dist/splat.module.js";

    const renderer = new SPLAT.Renderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('canvas').replaceWith(renderer.canvas);

    await SPLAT.Loader.LoadAsync("scene_compressed.splat", renderer.scene, (p) => {
      document.getElementById('progress').textContent = `Loading ${Math.round(p*100)}%`;
    });

    document.getElementById('progress').remove();
    renderer.render();
  </script>
</body>
</html>
```

Store large `.splat` files in **GitHub LFS** (free, 1 GB storage, 1 GB/month bandwidth).

### Hugging Face Spaces — Gradio Backend (Free GPU)
```python
# app.py
import gradio as gr
from pipeline import run_colmap, run_3dgs, run_langsplat, export_splat, export_glb

def process_scene(files):
    sparse  = run_colmap(files)
    ply     = run_3dgs(sparse, iterations=30000)
    _       = run_langsplat(ply)          # bakes CLIP into Gaussians
    splat   = export_splat(ply)           # compressed for web viewer
    glb     = export_glb(ply)            # mesh for Gradio Model3D
    return glb, splat

with gr.Blocks(title="3D Digital Twin Creator") as demo:
    gr.Markdown("# 🏙️ 3D Digital Twin Creator")
    with gr.Row():
        upload   = gr.File(label="Upload Photos or Video", file_count="multiple")
        model_3d = gr.Model3D(label="Your 3D Twin (.glb)")
    splat_dl = gr.File(label="Download .splat for Web Viewer")
    btn = gr.Button("Create 3D Twin ⚡", variant="primary")
    btn.click(process_scene, inputs=upload, outputs=[model_3d, splat_dl])

demo.launch()
```

### requirements.txt
```
torch==2.4.0
torchvision==0.19.0
gradio==4.44.0
pycolmap==3.10.0
gsplat==1.3.1
open3d==0.18.0
transformers==4.44.0
segment-anything-2
anthropic==0.34.0
clip @ git+https://github.com/openai/CLIP.git
```

### WebXR AR Mode (Bonus — Zero Extra Cost)
```javascript
// Let users place their digital twin in the real world via phone camera
if (navigator.xr) {
  const btn = document.createElement('button');
  btn.textContent = 'View in AR 📱';
  btn.onclick = async () => {
    const session = await navigator.xr.requestSession('immersive-ar', {
      requiredFeatures: ['hit-test']
    });
    renderer.xr.enabled = true;
    renderer.xr.setSession(session);
  };
  document.body.appendChild(btn);
}
```

---

## 9. Free Datasets

| Dataset | Scenes | Best For | URL |
|---|---|---|---|
| **DTU** | ~80 | Benchmark reconstruction quality | roboimagedata.compute.dtu.dk |
| **BlendedMVS** | 113 | Generalisation to diverse environments | github.com/YoYo000/BlendedMVS |
| **nerf-gs-datasets** | Curated | Pre-formatted for NeRF + 3DGS | HF: `jxuhf/nerf-gs-datasets` |
| **Tanks & Temples** | 21 | Large-scale indoor + outdoor | tanksandtemples.org |
| **DIY capture** | ∞ | Real-world robustness | Your smartphone |

```python
# Load HF dataset directly in Colab
from datasets import load_dataset
ds = load_dataset("jxuhf/nerf-gs-datasets", split="train")
```

---

## 10. Antigravity MCP Configuration

### Model Selection in Antigravity
1. Open **Settings → AI Model → Select Model**
2. Choose **Claude Sonnet 4.6** for day-to-day coding
3. Switch to **Claude Opus 4.6** for architecture decisions and
   complex multi-file refactors

### Complete mcp_config.json
Place at project root or `~/.antigravity/mcp_config.json` for global use.

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
    "firebase": {
      "command": "npx",
      "args": ["-y", "firebase-tools", "experimental:mcp"],
      "env": {
        "FIREBASE_PROJECT_ID": "${FIREBASE_PROJECT_ID}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${HOME}/projects/3dgs-output"
      ]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

### .env.local  (gitignored — never commit)
```bash
STITCH_API_KEY=your_stitch_key_here
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
FIREBASE_PROJECT_ID=your-firebase-project-id
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
# Notion uses OAuth — no token needed with serverUrl method
```

### Stitch Agent Skills to Install
```bash
npx skills add google-labs-code/stitch-skills --skill stitch-design --global
npx skills add google-labs-code/stitch-skills --skill design-md --global
npx skills add google-labs-code/stitch-skills --skill react-components --global
npx skills add google-labs-code/stitch-skills --skill shadcn-ui --global
```

### Notion MCP — Critical Warning
> ❌ Do NOT use the gallery "Notion" connector in Antigravity.
> It installs the deprecated `notion-mcp-server` npm package.
> ✅ Always use `"serverUrl": "https://mcp.notion.com/mcp"` as above.

### MCP Role Map for This Project

| Server | Used For |
|---|---|
| **stitch** | Generate Gradio UI screens, Three.js HUD overlays, DESIGN.md extraction |
| **notion** | Read architecture spec + coding standards before any task; update sprint board |
| **github** | Create PRs for completed features, read issues, search codebase |
| **firebase** | Read Firestore schema for scene metadata; deploy Cloud Functions |
| **filesystem** | Read COLMAP sparse output, .ply files, .splat compressed files locally |
| **playwright** | Browser-test the Three.js splat viewer and character engine |

---

## 11. AGENTS.md Template

```markdown
# AGENTS.md — 3D Digital Twin Creator

## Model
Use Claude Sonnet 4.6 for all tasks by default.
Switch to Claude Opus 4.6 for:
- Designing the GTA character behavior tree architecture
- Complex LangSplat + CLIP pipeline debugging
- Large multi-file Three.js refactors (>5 files changed)

## MCP Instructions
- **stitch**: Always read DESIGN.md before generating any UI component.
  Use react-components skill to convert Stitch output to clean React.
- **notion**: Fetch Architecture Spec (Page ID: YOUR_ID) before any
  backend task. Update sprint board task to "Done" on completion.
- **github**: Use conventional commits — feat/fix/chore(scope): message.
  Open a PR for every completed feature branch.
- **firebase**: Read Firestore schema before writing any data model code.
  Run `firebase login` locally before using this MCP server.
- **filesystem**: Use to read COLMAP sparse/ output and .ply / .splat
  files from ~/projects/3dgs-output/ without copying to clipboard.
- **playwright**: Run viewer tests after every Three.js change.
  Test on Chrome (primary), Firefox, and Safari (WebXR check).

## Pipeline Order — Never Skip Steps
1. Capture → ffmpeg frame extraction
2. COLMAP or HLoc → sparse/ point cloud
3. 3DGS training (Mip-Splatting) → point_cloud.ply
4. LangSplat training → CLIP features baked into Gaussians
5. SuGaR / GOF mesh export → scene.glb for Gradio Model3D
6. gsplat compression → scene_compressed.splat for web viewer
7. Three.js viewer + GTA character + A* navigation
8. Claude API narration + WebSpeech
9. OWL-ViT inventory + LangSplat search + SAM 2 segmentation
10. HF Spaces backend (Gradio) + GitHub Pages static viewer

## Coding Standards
- Python 3.11 / PyTorch 2.4 / CUDA 12.1 for all training code
- TypeScript strict mode for all Three.js / character / search code
- React 19 + shadcn/ui for control panels and Gradio-adjacent UI
- Three.js r169+ — never use deprecated APIs (no THREE.Geometry)
- All API keys via environment variables — never hardcoded
- Max Claude API call: max_tokens=300 per narration; batch where possible

## Project File Structure
src/
├── viewer/          # Three.js + splat renderer
│   ├── SplatRenderer.ts
│   ├── CameraController.ts
│   └── XRManager.ts
├── character/       # GTA agent
│   ├── AvatarLoader.ts
│   ├── PathfindingController.ts
│   ├── BehaviorTree.ts
│   └── NarrationEngine.ts      # Claude API + WebSpeech
├── search/          # Visual search
│   ├── LangSplatQuery.ts        # calls /search endpoint
│   ├── GaussianHighlighter.ts
│   ├── InventoryPanel.ts        # OWL-ViT results UI
│   └── SegmentationOverlay.ts   # SAM 2 mask overlay
├── pipeline/        # Training scripts (Python)
│   ├── capture_utils.py
│   ├── run_colmap.py
│   ├── train_3dgs.py
│   ├── train_langsplat.py
│   └── export_utils.py
├── api/             # HF Spaces backend
│   ├── app.py
│   └── requirements.txt
├── AGENTS.md
└── DESIGN.md
```

---

## 12. DESIGN.md Template

```markdown
# DESIGN.md — 3D Digital Twin Creator

## Visual Theme
Futuristic noir / GTA HUD aesthetic. Dense information overlaid on a dark
3D scene. Glass-panel UI elements. Feels like a AAA game HUD meets a
scientific instrument panel.

## Color Palette
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

## Typography
- **Headings**: Rajdhani 700, uppercase, letter-spacing 2px
- **HUD labels**: Rajdhani 600, 10–11px, letter-spacing 3px, ALL CAPS
- **Data / code**: Share Tech Mono, 12–13px
- **Body**: Rajdhani 400, 14–15px, line-height 1.6
- Fallbacks: system-ui, monospace

## Component Rules
- Panels: `background: rgba(17,20,24,0.9)` · `border: 0.5px solid rgba(247,193,49,0.35)`
- Buttons: uppercase · letter-spacing 1px · 1px solid border in accent color
  Hover: bg opacity +10% · `box-shadow: 0 0 8px <accent>40`
- Bars (health/progress): 5–8px height · accent fill · `#1a1a1a` track · `border-radius: 2px`
- Minimap: circular 120px · GTA-style triangle waypoints · animated player dot
- Notifications: slide in bottom-right · 220px wide · auto-dismiss 2.8 s
- Scanlines overlay (optional): `repeating-linear-gradient` at 6% opacity

## Layout Zones
- **Top-left**: Scene title + star-rating difficulty
- **Top-right**: Circular minimap
- **Bottom bar**: Stats strip — FPS · Engine name · Cost · Scene count
- **Left sidebar**: Mission / pipeline stage selector with progress bars
- **Right panel**: Search bar + inventory list + narration caption
- **Floating**: Notification toasts, bottom-right
```

---

## 13. Full Technology Stack

| Layer | Technology | Version | Notes |
|---|---|---|---|
| 3DGS Core | gaussian-splatting | latest | graphdeco-inria/gaussian-splatting |
| Anti-alias | Mip-Splatting | latest | Use for all final builds |
| Semantic 3D | LangSplat | latest | CLIP baked into each Gaussian |
| Mesh export | SuGaR / GOF | latest | Textured .glb from Gaussians |
| Compression | gsplat | 1.3.1+ | 300 MB → 8 MB |
| SfM Poses | pycolmap / HLoc | 3.10.0 | Camera pose estimation |
| 3D Viewer | Three.js | r169+ | WebGL splat renderer |
| Splat Loader | @sparkjoy/splat | 0.3+ | antimatter15 algorithm |
| Avatar | ReadyPlayerMe | GLTF 2.0 | Free custom avatars |
| Animations | Mixamo | — | Free motion capture library |
| Pathfinding | three-pathfinding | 0.8+ | A* on baked nav-mesh |
| Object Detect | OWL-ViT 2 | — | google/owlvit-large-patch14 |
| Segmentation | SAM 2 | — | facebook/sam2-hiera-large |
| CLIP | OpenAI CLIP | ViT-L/14 | Text → 512-d vector |
| LLM | Claude Sonnet 4.6 | claude-sonnet-4-20250514 | Character brain |
| Speech | WebSpeech API | native | Browser TTS, $0 |
| Physics | Rapier WASM | 0.14+ | Optional collision |
| Frontend UI | React 19 + shadcn/ui | latest | Control panel |
| Backend | Gradio | 4.44+ | HF Spaces app |
| Training GPU | Google Colab T4 | — | Free tier |
| Backend Host | Hugging Face Spaces | — | Free GPU runtime |
| Viewer Host | GitHub Pages + LFS | — | Free static CDN |
| IDE | Google Antigravity | 1.20.5+ | Claude Sonnet/Opus |
| UI Design | Google Stitch | — | MCP-connected |
| Knowledge | Notion | — | MCP-connected |

---

## 14. Security & Cost Rules

### Total Project Cost: $0

| Resource | Service | Cost |
|---|---|---|
| Training GPU | Google Colab / Kaggle | Free |
| Backend hosting | Hugging Face Spaces | Free |
| Viewer hosting | GitHub Pages | Free |
| Datasets | DTU, BlendedMVS, HF | Free |
| Avatar + animations | ReadyPlayerMe + Mixamo | Free |
| IDE | Antigravity | Free |
| UI design tool | Google Stitch | Free |

### Claude API — Keep Costs Minimal
- Only call Claude API **on POI arrival** — never every frame
- Batch inventory + narration into **one API call** per stop
- Use `max_tokens: 300` — narration needs 2–3 sentences max
- Cache narration per location hash — skip repeat visits
- Use `claude-sonnet-4-20250514` — do NOT default to Opus for narration

### Security Checklist
```
[ ] .env.local added to .gitignore before first commit
[ ] No API keys hardcoded anywhere — all use ${ENV_VAR}
[ ] GitHub PAT is fine-grained, scoped to this repo only
[ ] Notion integration token scoped to required pages only
[ ] HF Spaces secrets set in Space Settings, not in app.py
[ ] Stitch API key rotated quarterly
[ ] .splat files stored in GitHub LFS, not as regular blobs
```

### .gitignore Entries
```
.env.local
*.splat
output/
data/images/
data/database.db
__pycache__/
*.pyc
node_modules/
.DS_Store
```

---

## 15. Reference File Map

When a topic exceeds this SKILL.md, create these reference files:

```
references/
├── colmap-colab-notebook.md      # Full Colab notebook with all cells
├── langsplat-training-guide.md   # Step-by-step LangSplat training
├── three-character-full-code.md  # Complete Three.js character engine
├── hf-spaces-setup.md            # Step-by-step HF Spaces deployment
├── mcp-troubleshooting.md        # Common MCP errors and fixes
└── webxr-ar-integration.md       # Full WebXR hit-test AR mode guide
```

Load a reference file only when the user's task specifically requires it.

---

*Last updated: May 2026 · Claude Sonnet 4.6 · Antigravity v1.20.5+*
*Stack: 3DGS · LangSplat · Three.js · ReadyPlayerMe · Mixamo · OWL-ViT · SAM 2 · HF Spaces*
