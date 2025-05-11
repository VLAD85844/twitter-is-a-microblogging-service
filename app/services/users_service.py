from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models

def follow_user(db: Session, follower_id: int, followed_id: int) -> bool:
    if follower_id == followed_id:
        return True

    existing = db.query(models.Follow).filter_by(
        follower_id=follower_id,
        followed_id=followed_id
    ).first()
    if not existing:
        new_f = models.Follow(follower_id=follower_id, followed_id=followed_id)
        db.add(new_f)
        db.commit()
    return True


def unfollow_user(db: Session, follower_id: int, followed_id: int) -> bool:
    follow_rel = db.query(models.Follow).filter_by(
        follower_id=follower_id,
        followed_id=followed_id
    ).first()
    if follow_rel:
        db.delete(follow_rel)
        db.commit()
    return True


def get_user_by_id(db: Session, user_id: int) -> models.User:
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_profile_info(db: Session, user: models.User):
    followers_records = db.query(models.Follow).filter_by(followed_id=user.id).all()
    followers = []
    for fr in followers_records:
        follower_user = db.query(models.User).get(fr.follower_id)
        if follower_user:
            followers.append({"id": follower_user.id, "name": follower_user.name})

    following_records = db.query(models.Follow).filter_by(follower_id=user.id).all()
    following = []
    for fr in following_records:
        followed_user = db.query(models.User).get(fr.followed_id)
        if followed_user:
            following.append({"id": followed_user.id, "name": followed_user.name})

    return {
        "id": user.id,
        "name": user.name,
        "followers": followers,
        "following": following
    }
