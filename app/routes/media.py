from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, Header
from fastapi.responses import Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter()

def get_current_user(api_key: str, db: Session):
    user = db.query(models.User).filter(models.User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid api-key")
    return user

@router.post("/", response_model=dict)
def upload_media(
    api_key: str = Header(..., alias="api-key"),
    tweet_id: Optional[int] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    user = get_current_user(api_key, db)

    if tweet_id is not None:
        tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
        if not tweet:
            raise HTTPException(status_code=404, detail="Tweet not found")

    file_bytes = file.file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    media = models.Media(file_body=file_bytes, tweet_id=tweet_id)
    db.add(media)
    db.commit()
    db.refresh(media)
    return {"result": True, "media_id": media.id}

@router.get("/{media_id}")
def get_media(media_id: int, db: Session = Depends(get_db)):
    media = db.query(models.Media).filter(models.Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return Response(content=media.file_body, media_type="image/png")
