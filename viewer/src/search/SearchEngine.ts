export class SearchEngine {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async search(query: string, topK: number = 500) {
    try {
      const response = await fetch(`${this.baseUrl}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, top_k: topK })
      });
      return await response.json();
    } catch (e) {
      console.error('Search failed:', e);
      return { indices: [], centroid: { x: 0, y: 0, z: 0 }, count: 0 };
    }
  }

  async identify(imageFile: File) {
    const formData = new FormData();
    formData.append('file', imageFile);
    try {
      const response = await fetch(`${this.baseUrl}/identify`, {
        method: 'POST',
        body: formData
      });
      return await response.json();
    } catch (e) {
      console.error('Identification failed:', e);
      return { objects: [], narration: '', total_count: 0 };
    }
  }
}
