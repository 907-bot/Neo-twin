import * as THREE from 'three';

export class RenderLoop {
  private renderer: THREE.WebGLRenderer;
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private clock: THREE.Clock;
  private frameCount = 0;
  private lastTime = 0;

  constructor(renderer: THREE.WebGLRenderer, scene: THREE.Scene, camera: THREE.PerspectiveCamera, clock: THREE.Clock) {
    this.renderer = renderer;
    this.scene = scene;
    this.camera = camera;
    this.clock = clock;
  }

  render() {
    this.renderer.render(this.scene, this.camera);
  }

  updateFPS() {
    this.frameCount++;
    const now = performance.now();
    if (now - this.lastTime >= 1000) {
      const fps = Math.round(this.frameCount * 1000 / (now - this.lastTime));
      document.getElementById('fps-counter')!.textContent = fps.toString();
      this.frameCount = 0;
      this.lastTime = now;
    }
  }
}
