# NeoTwin Architecture

## System Overview

NeoTwin is a three-tier architecture:

1. **Viewer (Frontend)** — Three.js WebGL application
2. **Backend API** — FastAPI + Gradio on Hugging Face Spaces
3. **Training Pipeline** — Google Colab notebooks

## Data Flow

```
User uploads photos → COLMAP (camera poses) → 3DGS training → LangSplat (CLIP) → .splat file
                                                                 ↓
Viewer loads .splat ← GitHub Pages ← Compressed (8MB)
                                                                 ↓
User searches "red chair" → CLIP encode → LangSplat query → Highlight Gaussians
                                                                 ↓
Character walks to result → Gemini narrates → WebSpeech speaks
```

## Technology Decisions

| Decision | Alternative | Why Chosen |
|----------|-------------|------------|
| 3DGS | NeRF | 100x faster rendering |
| Gemini | Claude | Free, no credit card |
| Three.js | Unity | Web-native, no install |
| FastAPI | Flask | Async, type-safe |
| GitHub Pages | Vercel | Free LFS support |

## Security Model

- API keys via environment variables only
- Rate limiting at 15 RPM (Gemini free tier)
- CORS configured for viewer domain only
- No hardcoded secrets in repository
