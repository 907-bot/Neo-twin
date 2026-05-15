export interface SplatData {
  positions: Float32Array;
  colors: Uint8Array;
  scales: Float32Array;
  rotations: Float32Array;
  opacities: Float32Array;
}

export interface SearchResult {
  indices: number[];
  centroid: { x: number; y: number; z: number };
  count: number;
  refined_query?: string;
}

export interface InventoryItem {
  label: string;
  confidence: number;
  box: { xmin: number; ymin: number; xmax: number; ymax: number };
}

export interface CharacterState {
  position: { x: number; y: number; z: number };
  animation: string;
  isMoving: boolean;
}
