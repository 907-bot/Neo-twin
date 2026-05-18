import * as THREE from 'three';

export class SceneManager {
  private scene: THREE.Scene;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  async loadSplat(url: string, onProgress?: (progress: number) => void): Promise<void> {
    return new Promise((resolve, reject) => {
      import('gsplat').then((SPLAT) => {
        const renderer = new SPLAT.Renderer();
        SPLAT.Loader.LoadAsync(url, this.scene, (p) => {
          if (onProgress) onProgress(p);
        }).then(() => resolve()).catch(reject);
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
