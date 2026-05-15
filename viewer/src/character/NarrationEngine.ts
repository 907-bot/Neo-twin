export class NarrationEngine {
  private synth = window.speechSynthesis;

  speak(text: string) {
    const textEl = document.getElementById('narration-text');
    if (textEl) {
      textEl.innerHTML = `${text}<span class="narration-cursor"></span>`;
    }
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95;
    this.synth.speak(utterance);
  }

  async narrateFromAPI(imagePath: string, style: string = 'gta'): Promise<string> {
    try {
      const response = await fetch('http://localhost:7860/api/v1/narrate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_path: imagePath, style })
      });
      const data = await response.json();
      this.speak(data.narration);
      return data.narration;
    } catch (e) {
      console.error('Narration API failed:', e);
      return '';
    }
  }
}
