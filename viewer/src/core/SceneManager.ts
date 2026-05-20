import * as THREE from 'three';

export class SceneManager {
  private scene: THREE.Scene;
  private splatPoints: THREE.Points | null = null;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  async loadSplat(url: string, onProgress?: (progress: number) => void): Promise<void> {
    if (this.splatPoints) {
      this.scene.remove(this.splatPoints);
      this.splatPoints.geometry.dispose();
      if (Array.isArray(this.splatPoints.material)) {
        this.splatPoints.material.forEach(m => m.dispose());
      } else {
        this.splatPoints.material.dispose();
      }
      this.splatPoints = null;
    }

    const response = await fetch(url);
    if (!response.ok) throw new Error(`Failed to fetch splat from ${url}`);

    const reader = response.body?.getReader();
    if (!reader) throw new Error("Body reader not available");

    const contentLength = +(response.headers.get('Content-Length') || '0');
    let receivedLength = 0;
    const chunks: Uint8Array[] = [];

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      if (value) {
        chunks.push(value);
        receivedLength += value.length;
        if (onProgress && contentLength) {
          onProgress(receivedLength / contentLength);
        }
      }
    }

    const splatArray = new Uint8Array(receivedLength);
    let position = 0;
    for (const chunk of chunks) {
      splatArray.set(chunk, position);
      position += chunk.length;
    }

    const buffer = splatArray.buffer;
    const rowSize = 32;
    const count = Math.floor(buffer.byteLength / rowSize);

    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);

    const view = new DataView(buffer);
    for (let i = 0; i < count; i++) {
      const offset = i * rowSize;

      // Position (x, y, z)
      positions[i * 3 + 0] = view.getFloat32(offset + 0, true);
      positions[i * 3 + 1] = view.getFloat32(offset + 4, true);
      positions[i * 3 + 2] = view.getFloat32(offset + 8, true);

      // Color (r, g, b) normalized
      colors[i * 3 + 0] = view.getUint8(offset + 24) / 255;
      colors[i * 3 + 1] = view.getUint8(offset + 25) / 255;
      colors[i * 3 + 2] = view.getUint8(offset + 26) / 255;
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    // Create a particle material that feels premium, clean, and modern
    const material = new THREE.PointsMaterial({
      size: 0.05,
      vertexColors: true,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0.85,
      depthWrite: true
    });

    this.splatPoints = new THREE.Points(geometry, material);
    this.scene.add(this.splatPoints);

    geometry.computeBoundingBox();
    console.log(`[NeoTwin] Loaded ${count} splat points. Bounding box:`, geometry.boundingBox);
  }

  getSplatPoints(): THREE.Points | null {
    return this.splatPoints;
  }

  addLights() {
    const ambient = new THREE.AmbientLight(0xffffff, 0.5);
    this.scene.add(ambient);
    const directional = new THREE.DirectionalLight(0xffffff, 1);
    directional.position.set(5, 10, 7);
    this.scene.add(directional);
  }
}
