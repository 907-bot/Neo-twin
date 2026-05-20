import * as THREE from 'three';
import { SceneManager } from './core/SceneManager';
import { CameraController } from './core/CameraController';
import { RenderLoop } from './core/RenderLoop';
import { AvatarLoader } from './character/AvatarLoader';
import { PathfindingController } from './character/PathfindingController';
import { NarrationEngine } from './character/NarrationEngine';
import { SearchEngine } from './search/SearchEngine';
import { GaussianHighlighter } from './search/GaussianHighlighter';

export class App {
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private renderer: THREE.WebGLRenderer;
  private clock: THREE.Clock;
  private sceneManager: SceneManager;
  private cameraController: CameraController;
  private renderLoop: RenderLoop;
  private avatar: AvatarLoader | null = null;
  private pathfinding: PathfindingController | null = null;
  private narration: NarrationEngine | null = null;
  private searchEngine: SearchEngine | null = null;
  private highlighter: GaussianHighlighter | null = null;

  constructor(canvas: HTMLCanvasElement) {
    this.clock = new THREE.Clock();
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x08090A);
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.camera.position.set(0, 1.6, 5);
    this.renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.sceneManager = new SceneManager(this.scene);
    this.sceneManager.addLights();
    this.cameraController = new CameraController(this.camera, this.renderer.domElement);
    this.renderLoop = new RenderLoop(this.renderer, this.scene, this.camera, this.clock);
  }

  async init() {
    console.log('🚀 NeoTwin Viewer Initializing...');
    
    // Safety timeout: Ensure loader is hidden after 4s regardless of load state
    setTimeout(() => {
      const loader = document.getElementById('loading');
      if (loader && loader.style.display !== 'none') {
        console.warn('⚠️ Safety preloader timeout reached. Dismissing loading screen.');
        loader.style.opacity = '0';
        setTimeout(() => {
          loader.style.display = 'none';
        }, 500);
      }
    }, 4000);

    try {
      await this.sceneManager.loadSplat('scenes/demo.splat', (progress) => {
        const fill = document.getElementById('load-fill');
        const percent = document.getElementById('load-percent');
        if (fill) fill.style.width = `${progress * 100}%`;
        if (percent) percent.textContent = `${Math.round(progress * 100)}%`;
      });
    } catch (e) {
      console.warn('[NeoTwin] Splat file loading skipped or not found. Operating in local fallback mode:', e);
    }

    // Dismiss loader immediately since load attempt is complete
    const loader = document.getElementById('loading');
    if (loader) {
      loader.style.opacity = '0';
      setTimeout(() => {
        loader.style.display = 'none';
      }, 500);
    }

    try {
      this.avatar = new AvatarLoader(this.scene);
      await this.avatar.load('assets/avatar.glb').catch(err => {
        console.warn('[NeoTwin] Avatar asset not found or failed to load:', err);
      });
    } catch (e) {
      console.warn('[NeoTwin] Avatar loader failed to initialize:', e);
    }

    try {
      this.pathfinding = new PathfindingController(this.scene);
      if (this.avatar) {
        this.pathfinding.setAvatar(this.avatar);
      }
      this.narration = new NarrationEngine();
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:7860/api/v1';
      this.searchEngine = new SearchEngine(apiUrl);
      this.highlighter = new GaussianHighlighter(this.sceneManager);
    } catch (e) {
      console.warn('[NeoTwin] Telemetry engine components skipped:', e);
    }

    this.setupEventListeners();
    console.log('✅ NeoTwin Viewer Ready');
  }

  async loadScene(url: string) {
    console.log(`[NeoTwin] Loading dynamic scene: ${url}`);
    
    // Show preloader
    const loader = document.getElementById('loading');
    const fill = document.getElementById('load-fill');
    const percent = document.getElementById('load-percent');
    if (loader) {
      loader.style.display = 'flex';
      loader.style.opacity = '1';
    }
    if (fill) fill.style.width = '0%';
    if (percent) percent.textContent = '0%';
    
    try {
      await this.sceneManager.loadSplat(url, (progress) => {
        if (fill) fill.style.width = `${progress * 100}%`;
        if (percent) percent.textContent = `${Math.round(progress * 100)}%`;
      });
    } catch (e) {
      console.error('[NeoTwin] Error loading dynamic splat scene:', e);
    }
    
    // Hide preloader
    if (loader) {
      loader.style.opacity = '0';
      setTimeout(() => {
        loader.style.display = 'none';
      }, 500);
    }
  }

  private setupEventListeners() {
    window.addEventListener('resize', () => this.onResize());
    document.getElementById('search-input')!.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.handleSearch((e.target as HTMLInputElement).value);
    });
  }

  private async handleSearch(query: string) {
    if (!this.searchEngine) return;
    const result = await this.searchEngine.search(query);
    if (this.highlighter) this.highlighter.highlight(result.indices);
    if (this.pathfinding && result.centroid) {
      this.pathfinding.moveTo(result.centroid.x, result.centroid.y, result.centroid.z);
    }
    if (this.narration) {
      this.narration.speak(`Found ${query} in the scene.`);
    }
  }

  private onResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    this.renderLoop.render();
    if (this.avatar) this.avatar.update(this.clock.getDelta());
    if (this.pathfinding) this.pathfinding.update();
    this.renderLoop.updateFPS();
    this.updateCoords();
  }

  private updateCoords() {
    const coordEl = document.getElementById('coord-display');
    if (coordEl) {
      const { x, y, z } = this.camera.position;
      coordEl.textContent = `X:${x.toFixed(1)} Y:${y.toFixed(1)} Z:${z.toFixed(1)}`;
    }
  }
}
