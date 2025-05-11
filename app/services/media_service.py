import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app import models

def read_media_file(file: UploadFile) -> bytes:
    file_bytes = file.file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file")
    return file_bytes

def create_media_record(db: Session, file_bytes: bytes) -> models.Media:
    media = models.Media(file_body=file_bytes)
    db.add(media)
    db.commit()
    db.refresh(media)
    return media
