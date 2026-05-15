"""Gemini 2.0 Flash Integration - FREE AI Provider"""
import google.generativeai as genai
from PIL import Image
import os
from core.config import settings
import json

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    async def narrate_scene(self, image_path: str, prompt: str = None) -> str:
        if prompt is None:
            prompt = """You are a GTA-style character exploring a 3D digital twin.
Describe what you see in 2-3 short, punchy sentences. Name specific objects,
materials, and spatial relationships. Speak in first person. No markdown."""

        image = Image.open(image_path)
        response = self.model.generate_content([image, prompt])
        return response.text

    async def answer_question(self, image_path: str, question: str) -> str:
        image = Image.open(image_path)
        prompt = f"Based on this scene, answer: {question}"
        response = self.model.generate_content([image, prompt])
        return response.text

    async def describe_object(self, image_path: str, object_name: str) -> str:
        image = Image.open(image_path)
        prompt = f"Describe the {object_name} in this scene. Include its position, color, and relationship to nearby objects."
        response = self.model.generate_content([image, prompt])
        return response.text

    async def generate_search_query(self, user_input: str) -> str:
        prompt = f"Convert this natural language query into a concise search term for finding objects in a 3D scene: '{user_input}'. Return only the search term, nothing else."
        response = self.model.generate_content(prompt)
        return response.text.strip()

gemini_client = GeminiClient()
