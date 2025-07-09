from fastapi import APIRouter
from fastapi import APIRouter

router = APIRouter()

router = APIRouter(
    prefix="/habit",
    #dependencies=[Depends()],
)

@router.get("/habit/")
async def read_users():
    return {'habit'}