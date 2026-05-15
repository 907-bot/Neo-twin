# Deployment Guide

## 1. GitHub Pages (Viewer)

```bash
cd viewer
npm run build
git add dist
git commit -m "Build viewer"
git push origin main
```

Auto-deploys via GitHub Actions workflow.

## 2. Hugging Face Spaces (Backend)

1. Create Space at huggingface.co/spaces
2. Select "Docker" SDK
3. Push backend folder:
```bash
huggingface-cli upload username/neotwin-api ./backend .
```

## 3. Set Secrets

### GitHub Secrets:
- `HF_TOKEN` — Hugging Face API token
- `HF_USERNAME` — Your HF username

### HF Space Secrets (Settings → Variables):
- `GEMINI_API_KEY` — Your Gemini API key
- `HUGGINGFACE_TOKEN` — HF token

## 4. Custom Domain (Optional)

```
viewer.yourdomain.com → GitHub Pages
api.yourdomain.com → HF Spaces
```

## 5. Monitoring

- Health endpoint: `/api/v1/health`
- Metrics endpoint: `/api/v1/metrics`
- Logs: HF Spaces → Logs tab
