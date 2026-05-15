export class GaussianHighlighter {
  private highlightedIndices: number[] = [];
  private highlightColor = 0xF7C131;
  private originalColors: Map<number, number> = new Map();

  highlight(indices: number[]) {
    this.highlightedIndices = indices;
    console.log(`Highlighting ${indices.length} Gaussians`);
    indices.forEach(idx => {
      this.setGaussianColor(idx, this.highlightColor);
      this.setGaussianScale(idx, 1.4);
    });
    setTimeout(() => this.reset(), 6000);
  }

  private setGaussianColor(idx: number, color: number) {
    // Placeholder: integrate with splat renderer
  }

  private setGaussianScale(idx: number, scale: number) {
    // Placeholder: integrate with splat renderer
  }

  reset() {
    this.highlightedIndices.forEach(idx => {
      this.resetGaussian(idx);
    });
    this.highlightedIndices = [];
  }

  private resetGaussian(idx: number) {
    // Placeholder: reset to original
  }
}
