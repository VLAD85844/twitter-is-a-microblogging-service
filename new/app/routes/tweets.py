from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from .. import models, schemas
from sqlalchemy import or_

router = APIRouter()

def get_current_user(api_key: str, db: Session):
    user = db.query(models.User).filter(models.User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid api-key")
    return user

@router.post("/", response_model=dict)
def create_tweet(
    tweet_in: schemas.TweetCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(..., alias="api-key")
):
    user = get_current_user(api_key, db)
    new_tweet = models.Tweet(author_id=user.id, content=tweet_in.tweet_data)
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)

    if tweet_in.tweet_media_ids:
        for media_id in tweet_in.tweet_media_ids:
            media = db.query(models.Media).filter(models.Media.id == media_id).first()
            if media:
                media.tweet_id = new_tweet.id
        db.commit()

    return {"result": True, "tweet_id": new_tweet.id}

@router.delete("/{tweet_id}", response_model=dict)
def delete_tweet(
    tweet_id: int,
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db)
):
    user = get_current_user(api_key, db)
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    if tweet.author_id != user.id:
        raise HTTPException(status_code=403, detail="Cannot delete someone else's tweet")
    db.query(models.Like).filter(models.Like.tweet_id == tweet_id).delete()
    db.delete(tweet)
    db.commit()
    return {"result": True}

@router.post("/{tweet_id}/likes", response_model=dict)
def like_tweet(
    tweet_id: int,
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db)
):
    user = get_current_user(api_key, db)
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    like = db.query(models.Like).filter(models.Like.user_id == user.id, models.Like.tweet_id == tweet_id).first()
    if not like:
        new_like = models.Like(user_id=user.id, tweet_id=tweet_id)
        db.add(new_like)
        db.commit()
    return {"result": True}

@router.delete("/{tweet_id}/likes", response_model=dict)
def unlike_tweet(
    tweet_id: int,
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db)
):
    user = get_current_user(api_key, db)
    like = db.query(models.Like).filter(models.Like.user_id == user.id, models.Like.tweet_id == tweet_id).first()
    if like:
        db.delete(like)
        db.commit()
    return {"result": True}

@router.get("/", response_model=dict)
def get_tweets(
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db)
):
    user = get_current_user(api_key, db)

    tweets = db.query(models.Tweet).all()

    results = []
    for t in tweets:
        likes = db.query(models.Like).filter(models.Like.tweet_id == t.id).all()
        attachments = [f"/api/medias/{m.id}" for m in t.attachments] if hasattr(t, "attachments") else []
        results.append({
            "id": t.id,
            "content": t.content,
            "attachments": attachments,
            "author": {
                "id": t.author.id,
                "name": t.author.name
            },
            "likes": [{"user_id": lk.user_id, "name": ""} for lk in likes],
            "like_count": len(likes),
            "created_at": t.created_at.isoformat()
        })

    results = sorted(results, key=lambda x: x["like_count"], reverse=True)
    return {"result": True, "tweets": results}

