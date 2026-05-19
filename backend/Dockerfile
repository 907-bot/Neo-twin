FROM python:3.11

# Install system deps for OpenCV, ffmpeg, git (needed for CLIP install)
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    colmap \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV QT_QPA_PLATFORM=offscreen

# Copy and install Python deps first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# HuggingFace Spaces uses port 7860
EXPOSE 7860

# Run with uvicorn — workers=1 keeps memory usage manageable on free tier
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
