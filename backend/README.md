---
title: NeoTwin API
emoji: 🤖
colorFrom: yellow
colorTo: gray
sdk: docker
pinned: false
app_port: 7860
---

# NeoTwin API — 3D Digital Twin Backend

FastAPI backend powering the NeoTwin 3D Digital Twin platform.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/api/v1/health` | Detailed health status |
| POST | `/api/v1/reconstruct` | Upload video/photos → 3DGS job |
| GET | `/api/v1/reconstruct/{job_id}` | Poll job status |
| POST | `/api/v1/search` | Semantic scene search |
| POST | `/api/v1/identify` | Object identification |
| POST | `/api/v1/narrate` | AI narration generation |

## Environment Variables

Set these in the HuggingFace Space secrets:

```
GEMINI_API_KEY=your_gemini_api_key
HUGGINGFACE_TOKEN=your_hf_token
```

## API Docs

Visit `/docs` for the interactive Swagger UI.
