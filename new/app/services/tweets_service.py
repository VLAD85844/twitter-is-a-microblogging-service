from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models

def create_tweet(db: Session, user_id: int, content: str, media_ids: Optional[List[int]] = None):
    new_tweet = models.Tweet(author_id=user_id, content=content)
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    return new_tweet


def delete_tweet(db: Session, user_id: int, tweet_id: int):
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    if tweet.author_id != user_id:
        raise HTTPException(status_code=403, detail="Cannot delete someone else's tweet")

    db.delete(tweet)
    db.commit()
    return True


def like_tweet(db: Session, user_id: int, tweet_id: int):
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    like = db.query(models.Like).filter_by(user_id=user_id, tweet_id=tweet_id).first()
    if not like:
        new_like = models.Like(user_id=user_id, tweet_id=tweet_id)
        db.add(new_like)
        db.commit()
    return True


def unlike_tweet(db: Session, user_id: int, tweet_id: int):
    like = db.query(models.Like).filter_by(user_id=user_id, tweet_id=tweet_id).first()
    if like:
        db.delete(like)
        db.commit()
    return True


def get_followed_tweets(db: Session, user_id: int):
    follow_records = db.query(models.Follow).filter(models.Follow.follower_id == user_id).all()
    followed_ids = [f.followed_id for f in follow_records]
    tweets = db.query(models.Tweet).filter(models.Tweet.author_id.in_(followed_ids)).all()

    return tweets
