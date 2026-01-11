from fastapi import APIRouter, Depends
from app.core.security import verify_api_key

router = APIRouter(
    prefix="/protected",
    tags=["protected"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("")
def protected_endpoint():
    return {"message": "authorized"}
