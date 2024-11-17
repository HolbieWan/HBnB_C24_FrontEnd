# review.py

from app.models.base_model import BaseModel
from app.extensions import db

class Review(BaseModel):
    __tablename__ = 'reviews'
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(), db.ForeignKey('places.id', ondelete='CASCADE') , nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    place = db.relationship('Place', back_populates='review_ids', lazy=True)
    user = db.relationship('User', back_populates='reviews', lazy=True)