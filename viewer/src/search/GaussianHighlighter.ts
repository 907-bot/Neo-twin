import * as THREE from 'three';
import { SceneManager } from '../core/SceneManager';

export class GaussianHighlighter {
  private sceneManager: SceneManager;
  private highlightedIndices: number[] = [];
  private highlightColor = 0xF7C131; // Gold
  private originalColors: Map<number, { r: number; g: number; b: number }> = new Map();

  constructor(sceneManager: SceneManager) {
    this.sceneManager = sceneManager;
  }

  highlight(indices: number[]) {
    this.reset();
    this.highlightedIndices = indices;
    console.log(`Highlighting ${indices.length} Gaussians`);
    indices.forEach(idx => {
      this.setGaussianColor(idx, this.highlightColor);
      this.setGaussianScale(idx, 1.4);
    });
    setTimeout(() => this.reset(), 6000);
  }

  private setGaussianColor(idx: number, hexColor: number) {
    const points = this.sceneManager.getSplatPoints();
    if (!points) return;

    const colorAttribute = points.geometry.getAttribute('color') as THREE.BufferAttribute;
    if (!colorAttribute) return;

    if (idx < 0 || idx >= colorAttribute.count) return;

    // Save original color
    if (!this.originalColors.has(idx)) {
      this.originalColors.set(idx, {
        r: colorAttribute.getX(idx),
        g: colorAttribute.getY(idx),
        b: colorAttribute.getZ(idx)
      });
    }

    // Unpack hex color
    const r = ((hexColor >> 16) & 255) / 255;
    const g = ((hexColor >> 8) & 255) / 255;
    const b = (hexColor & 255) / 255;

    colorAttribute.setXYZ(idx, r, g, b);
    colorAttribute.needsUpdate = true;
  }

  private setGaussianScale(idx: number, scale: number) {
    // For THREE.Points, individual vertex scaling isn't natively supported,
    // but color highlighting is more than enough for visual feedback.
  }

  reset() {
    const points = this.sceneManager.getSplatPoints();
    if (!points) {
      this.highlightedIndices = [];
      this.originalColors.clear();
      return;
    }

    const colorAttribute = points.geometry.getAttribute('color') as THREE.BufferAttribute;
    if (!colorAttribute) return;

    this.highlightedIndices.forEach(idx => {
      const orig = this.originalColors.get(idx);
      if (orig && idx >= 0 && idx < colorAttribute.count) {
        colorAttribute.setXYZ(idx, orig.r, orig.g, orig.b);
      }
    });

    colorAttribute.needsUpdate = true;
    this.highlightedIndices = [];
    this.originalColors.clear();
  }
}
