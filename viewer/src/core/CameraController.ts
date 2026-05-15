import * as THREE from 'three';

export class CameraController {
  private camera: THREE.PerspectiveCamera;
  private domElement: HTMLElement;
  private keys: Record<string, boolean> = {};
  private speed = 0.04;

  constructor(camera: THREE.PerspectiveCamera, domElement: HTMLElement) {
    this.camera = camera;
    this.domElement = domElement;
    this.setupControls();
  }

  private setupControls() {
    document.addEventListener('keydown', (e) => this.keys[e.key] = true);
    document.addEventListener('keyup', (e) => this.keys[e.key] = false);
    this.domElement.addEventListener('click', (e) => this.handleClick(e));
  }

  update() {
    const dir = new THREE.Vector3();
    if (this.keys['w'] || this.keys['ArrowUp']) dir.z -= this.speed;
    if (this.keys['s'] || this.keys['ArrowDown']) dir.z += this.speed;
    if (this.keys['a'] || this.keys['ArrowLeft']) dir.x -= this.speed;
    if (this.keys['d'] || this.keys['ArrowRight']) dir.x += this.speed;
    if (dir.length() > 0) {
      dir.applyQuaternion(this.camera.quaternion);
      this.camera.position.add(dir);
    }
  }

  private handleClick(event: MouseEvent) {
    console.log('Click to move:', event.clientX, event.clientY);
  }
}
