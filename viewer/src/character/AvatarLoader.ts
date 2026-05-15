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
    const { GLTFLoader } = await import('three/examples/jsm/loaders/GLTFLoader.js');
    const loader = new GLTFLoader();
    return new Promise<void>((resolve, reject) => {
      loader.load(url, (gltf) => {
        this.character = gltf.scene;
        this.scene.add(this.character);
        this.mixer = new THREE.AnimationMixer(this.character);
        gltf.animations.forEach((clip) => {
          const action = this.mixer!.clipAction(clip);
          this.actions[clip.name] = action;
        });
        if (this.actions['Idle']) this.actions['Idle'].play();
        resolve();
      }, undefined, reject);
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
