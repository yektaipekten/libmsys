from fastapi import APIRouter

router = APIRouter()


@router.get("/availability")
async def check_availability() -> bool:

    available = True
    return available


@router.get("/return_book")
async def return_book() -> bool:
    available = True
    return available
