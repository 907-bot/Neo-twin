import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

export class CameraController {
  private camera: THREE.PerspectiveCamera;
  private domElement: HTMLElement;
  private controls: OrbitControls;

  constructor(camera: THREE.PerspectiveCamera, domElement: HTMLElement) {
    this.camera = camera;
    this.domElement = domElement;
    this.controls = new OrbitControls(this.camera, this.domElement);
    this.setupControls();
  }

  private setupControls() {
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.screenSpacePanning = true;
    this.controls.minDistance = 0.5;
    this.controls.maxDistance = 100;
    
    // Position controls target near the default avatar position
    this.controls.target.set(0, 1.6, 0);
    this.controls.update();

    this.domElement.addEventListener('click', (e) => this.handleClick(e));
  }

  update() {
    this.controls.update();
  }

  fitToBox(box: THREE.Box3) {
    const center = new THREE.Vector3();
    box.getCenter(center);
    
    const size = new THREE.Vector3();
    box.getSize(size);
    
    const maxDim = Math.max(size.x, size.y, size.z);
    const fov = this.camera.fov * (Math.PI / 180);
    
    // Safely calculate camera distance with a fallback for flat/empty boxes
    let cameraZ = maxDim > 0.01 ? Math.abs(maxDim / 2 / Math.tan(fov / 2)) : 5;
    cameraZ = Math.max(1, Math.min(cameraZ * 1.5, 30));
    
    this.controls.target.copy(center);
    this.camera.position.set(center.x, center.y + (maxDim * 0.2), center.z + cameraZ);
    this.controls.update();
  }

  private handleClick(event: MouseEvent) {
    console.log('Click to move:', event.clientX, event.clientY);
  }
}
