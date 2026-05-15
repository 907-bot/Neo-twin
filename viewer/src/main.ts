import * as THREE from 'three';
import { App } from './App';

const canvas = document.getElementById('canvas') as HTMLCanvasElement;
const app = new App(canvas);
app.init();
app.animate();
