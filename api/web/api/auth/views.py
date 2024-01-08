from fastapi import APIRouter

router = APIRouter()

@router.post("/signin")
async def create_user():
    return

