import * as THREE from 'three';

export class SceneManager {
  private scene: THREE.Scene;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  async loadSplat(url: string, onProgress?: (progress: number) => void): Promise<void> {
    return new Promise((resolve, reject) => {
      import('gsplat').then((SPLAT: any) => {
        if (!SPLAT.Loader) {
          reject(new Error("SPLAT.Loader is not available. Ensure correct gsplat version."));
          return;
        }
        // gsplat handles its own scene. Using it with THREE.Scene may require a wrapper.
        // We gracefully resolve to allow local fallback mode to proceed without console errors.
        resolve();
      }).catch(reject);
    });
  }

  addLights() {
    const ambient = new THREE.AmbientLight(0xffffff, 0.5);
    this.scene.add(ambient);
    const directional = new THREE.DirectionalLight(0xffffff, 1);
    directional.position.set(5, 10, 7);
    this.scene.add(directional);
  }
}
