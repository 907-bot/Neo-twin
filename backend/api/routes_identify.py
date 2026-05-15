"""API Routes: Object Identification"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from models.owl_vit_detector import owl_vit_detector
from models.gemini_client import gemini_client
from core.security import check_rate_limit
from PIL import Image
import io

router = APIRouter()

class InventoryItem(BaseModel):
    label: str
    confidence: float
    box: dict

class InventoryResponse(BaseModel):
    objects: list[InventoryItem]
    narration: str = ""
    total_count: int

@router.post("/identify", response_model=InventoryResponse)
async def identify_objects(file: UploadFile = File(...)):
    if not check_rate_limit("client"):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    try:
        image = Image.open(io.BytesIO(await file.read()))
        objects = owl_vit_detector.detect_objects(image)
        inventory = [InventoryItem(**obj) for obj in objects]
        narration = await gemini_client.narrate_scene(
            io.BytesIO(await file.read()),
            "List all objects you see in this scene briefly."
        )
        return InventoryResponse(objects=inventory, narration=narration, total_count=len(inventory))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/describe-object")
async def describe_specific_object(file: UploadFile = File(...), object_name: str = "chair"):
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        description = await gemini_client.describe_object(image, object_name)
        return {"object": object_name, "description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
