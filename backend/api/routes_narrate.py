"""API Routes: AI Narration via Gemini"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from models.gemini_client import gemini_client
from core.security import check_rate_limit
from PIL import Image
import io

router = APIRouter()

class NarrateRequest(BaseModel):
    image_path: str = ""
    prompt: str = ""
    style: str = "gta"

class NarrateResponse(BaseModel):
    narration: str
    style: str

NARRATION_STYLES = {
    "gta": "You are a GTA-style character exploring a 3D digital twin. Describe what you see in 2-3 short, punchy sentences. Name specific objects, materials, and spatial relationships. Speak in first person. No markdown.",
    "architect": "You are an architect analyzing this space. Describe the design elements, spatial flow, materials, and architectural style in professional terms.",
    "tourist": "You are a tourist seeing this place for the first time. Express wonder and curiosity. Point out interesting details.",
    "detective": "You are a detective examining a scene. Note suspicious details, unusual objects, and anything out of place."
}

@router.post("/narrate", response_model=NarrateResponse)
async def narrate_scene(req: NarrateRequest):
    if not check_rate_limit("client"):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    try:
        prompt = NARRATION_STYLES.get(req.style, NARRATION_STYLES["gta"])
        if req.prompt:
            prompt = req.prompt
        narration = await gemini_client.narrate_scene(req.image_path, prompt)
        return NarrateResponse(narration=narration, style=req.style)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/narrate/upload")
async def narrate_from_upload(file: UploadFile = File(...), style: str = "gta"):
    if not check_rate_limit("client"):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    try:
        image = Image.open(io.BytesIO(await file.read()))
        temp_path = "temp_narrate.jpg"
        image.save(temp_path)
        prompt = NARRATION_STYLES.get(style, NARRATION_STYLES["gta"])
        narration = await gemini_client.narrate_scene(temp_path, prompt)
        return {"narration": narration, "style": style}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask")
async def ask_about_scene(file: UploadFile = File(...), question: str = ""):
    try:
        image = Image.open(io.BytesIO(await file.read()))
        temp_path = "temp_ask.jpg"
        image.save(temp_path)
        answer = await gemini_client.answer_question(temp_path, question)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
