# place.py

from app.models.base_model import BaseModel
from app.extensions import db
from app.models.association_tables import place_amenity


class Place(BaseModel):
    __tablename__ = 'places'
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner = db.Column(db.String(50), nullable=True)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    reviews = db.Column(db.JSON, default=[])
    amenities = db.Column(db.JSON, default=[])

    place_owner = db.relationship('User', back_populates='places', lazy=True)
    review_ids = db.relationship('Review', back_populates='place', lazy=True, cascade='all, delete-orphan')
    amenities_obj = db.relationship('Amenity', secondary=place_amenity, back_populates='places', lazy=True)
