import * as THREE from 'three';

export class PathfindingController {
  private scene: THREE.Scene;
  private target: THREE.Vector3 | null = null;
  private speed = 0.03;
  private isMoving = false;
  private avatar: any = null;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  setAvatar(avatar: any) {
    this.avatar = avatar;
  }

  update() {
    if (!this.target || !this.isMoving || !this.avatar) return;
    const currentPos = this.avatar.getPosition();
    const direction = new THREE.Vector3().subVectors(this.target, currentPos);
    if (direction.length() < 0.1) {
      this.isMoving = false;
      this.onArrived();
      return;
    }
    direction.normalize().multiplyScalar(this.speed);
    currentPos.add(direction);
    this.avatar.setPosition(currentPos);
  }

  moveTo(x: number, y: number, z: number) {
    this.target = new THREE.Vector3(x, y, z);
    this.isMoving = true;
    console.log('Moving to:', x, y, z);
  }

  private getCurrentPosition() {
    if (this.avatar) {
      return this.avatar.getPosition();
    }
    return new THREE.Vector3(0, 0, 0);
  }

  private onArrived() {
    console.log('Arrived at destination');
  }
}
