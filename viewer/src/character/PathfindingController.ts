import * as THREE from 'three';

export class PathfindingController {
  private scene: THREE.Scene;
  private target: THREE.Vector3 | null = null;
  private speed = 0.03;
  private isMoving = false;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  update() {
    if (!this.target || !this.isMoving) return;
    const direction = new THREE.Vector3().subVectors(this.target, this.getCurrentPosition());
    if (direction.length() < 0.1) {
      this.isMoving = false;
      this.onArrived();
      return;
    }
    direction.normalize().multiplyScalar(this.speed);
    this.getCurrentPosition().add(direction);
  }

  moveTo(x: number, y: number, z: number) {
    this.target = new THREE.Vector3(x, y, z);
    this.isMoving = true;
    console.log('Moving to:', x, y, z);
  }

  private getCurrentPosition() {
    return new THREE.Vector3(0, 0, 0);
  }

  private onArrived() {
    console.log('Arrived at destination');
  }
}
