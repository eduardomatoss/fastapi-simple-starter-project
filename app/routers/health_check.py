from fastapi import APIRouter


router = APIRouter()


@router.get("/health-check")
def app_check():
    return {"message": "OK"}
