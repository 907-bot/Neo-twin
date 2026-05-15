"""API Routes: Visual Search"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.clip_engine import clip_engine
from models.gemini_client import gemini_client
from models.langsplat_query import langsplat_query
from core.security import check_rate_limit

router = APIRouter()

class SearchQuery(BaseModel):
    query: str
    top_k: int = 500
    scene_id: str = "default"

class SearchResult(BaseModel):
    indices: list
    centroid: dict
    count: int
    refined_query: str = ""

@router.post("/search", response_model=SearchResult)
async def search_scene(req: SearchQuery):
    if not check_rate_limit("client"):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    try:
        text_embedding = clip_engine.encode_text(req.query)
        result = langsplat_query.search(text_embedding, req.top_k)
        refined = await gemini_client.generate_search_query(req.query)
        return SearchResult(**result, refined_query=refined)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/similar")
async def find_similar_objects(query: str, threshold: float = 0.7):
    similarity = clip_engine.compute_similarity(query, "data/sample.jpg")
    return {"query": query, "similarity": similarity, "match": similarity > threshold}
