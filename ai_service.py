from fastapi import APIRouter

# 이 줄이 꼭 있어야 합니다!
router = APIRouter()

@router.get("/ai")
async def ai_root():
    return {"message": "AI service is running"}