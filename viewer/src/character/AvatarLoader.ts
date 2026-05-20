import * as THREE from 'three';

export class AvatarLoader {
  private scene: THREE.Scene;
  private mixer: THREE.AnimationMixer | null = null;
  private character: THREE.Object3D | null = null;
  private actions: Record<string, THREE.AnimationAction> = {};
  private currentAction: THREE.AnimationAction | null = null;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
  }

  async load(url: string) {
    // Create a mock avatar using a group and basic meshes to prevent 404 errors
    return new Promise<void>((resolve) => {
      this.character = new THREE.Group();
      const body = new THREE.Mesh(
        new THREE.CylinderGeometry(0.3, 0.3, 1.6, 16),
        new THREE.MeshStandardMaterial({ color: 0x888888 })
      );
      body.position.y = 0.8;
      
      const head = new THREE.Mesh(
        new THREE.SphereGeometry(0.25, 16, 16),
        new THREE.MeshStandardMaterial({ color: 0xcccccc })
      );
      head.position.y = 1.85;
      
      this.character.add(body, head);
      this.scene.add(this.character);
      
      // Dummy mixer so we don't throw errors
      this.mixer = new THREE.AnimationMixer(this.character);
      resolve();
    });
  }

  update(delta: number) {
    if (this.mixer) this.mixer.update(delta);
  }

  playAnimation(name: string) {
    if (this.actions[name]) {
      if (this.currentAction) this.currentAction.fadeOut(0.3);
      this.actions[name].reset().fadeIn(0.3).play();
      this.currentAction = this.actions[name];
    }
  }

  getPosition() {
    return this.character?.position.clone() || new THREE.Vector3();
  }

  setPosition(pos: THREE.Vector3) {
    if (this.character) this.character.position.copy(pos);
  }
}
