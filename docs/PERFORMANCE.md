# Performance Optimization

## Targets

| Metric | Target |
|--------|--------|
| FPS | 100+ |
| Load time | < 3s |
| .splat size | ≤ 8MB |
| API response | < 500ms |

## Optimization Techniques

### 3DGS
- Use Mip-Splatting for anti-aliasing
- Compress with gsplat (target 8MB)
- Reduce iterations to 30k for speed

### Viewer
- Lazy load .splat file
- Use Web Workers for heavy computation
- Limit pixel ratio to 2x

### Backend
- Cache CLIP embeddings
- Batch Gemini API calls
- Use async endpoints

### Network
- CDN for Three.js libraries
- Gzip compress API responses
- HTTP/2 for parallel requests
