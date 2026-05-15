# Troubleshooting

## Common Issues

### COLMAP fails
- Ensure images have 70%+ overlap
- Check image quality (not blurry)
- Try HLoc for difficult scenes

### 3DGS training crashes
- Reduce batch size
- Check GPU memory (need 8GB+)
- Use Colab T4 or A100

### Viewer doesn't load
- Check .splat file path
- Verify Three.js version
- Check browser console for errors

### Gemini API errors
- Verify API key is set
- Check rate limit (15 RPM)
- Ensure image format is supported

### Search returns no results
- Verify LangSplat training completed
- Check CLIP model is loaded
- Try simpler search queries

## Getting Help

1. Check this doc
2. Search existing issues
3. Open new issue with:
   - Error message
   - Steps to reproduce
   - System info
