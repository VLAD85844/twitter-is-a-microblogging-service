from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models

def get_current_user_by_apikey(api_key: str, db: Session):
    user = db.query(models.User).filter(models.User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or missing api-key")
    return user

def some_string_cleaner(text: str) -> str:

    return text.strip().lower()

