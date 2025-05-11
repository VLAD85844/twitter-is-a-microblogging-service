from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..utils import get_current_user_by_apikey
router = APIRouter()

def get_current_user(api_key: str, db: Session):
    user = db.query(models.User).filter(models.User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid api-key")
    return user

@router.post("/{user_id}/follow", response_model=dict)
def follow_user(
    user_id: int,
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db)
):
    current = get_current_user(api_key, db)
    if current.id == user_id:
        return {"result": True}
    existing = db.query(models.Follow).filter_by(
        follower_id=current.id,
        followed_id=user_id
    ).first()
    if not existing:
        new_f = models.Follow(follower_id=current.id, followed_id=user_id)
        db.add(new_f)
        db.commit()
    return {"result": True}


@router.delete("/{user_id}/follow", response_model=dict)
def unfollow_user(
    user_id: int,
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db)
):
    current = get_current_user(api_key, db)
    follow_rel = db.query(models.Follow).filter_by(
        follower_id=current.id,
        followed_id=user_id
    ).first()
    if follow_rel:
        db.delete(follow_rel)
        db.commit()
    return {"result": True}

@router.get("/me", response_model=dict)
def get_me(api_key: str = Header(..., alias="api-key"), db: Session = Depends(get_db)):
    current = get_current_user_by_apikey(api_key, db)
    followers_q = db.query(models.Follow).filter_by(followed_id=current.id).all()
    following_q = db.query(models.Follow).filter_by(follower_id=current.id).all()
    followers = []
    following = []
    for f in followers_q:
        user = db.query(models.User).get(f.follower_id)
        if user:
            followers.append({"id": user.id, "name": user.name})
    for f in following_q:
        user = db.query(models.User).get(f.followed_id)
        if user:
            following.append({"id": user.id, "name": user.name})
    return {
        "result": True,
        "user": {
            "id": current.id,
            "name": current.name,
            "followers": followers,
            "following": following
        }
    }

@router.get("/{user_id}", response_model=dict)
def get_user_by_id(
    user_id: int,
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db)
):
    current = get_current_user(api_key, db)
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [],
            "following": []
        }
    }