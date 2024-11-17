# amenity.py

from app.extensions import db
from app.models.base_model import BaseModel
from app.models.association_tables import place_amenity

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    name = db.Column(db.String(50), nullable=False)

    places = db.relationship('Place', secondary=place_amenity, back_populates='amenities_obj', lazy=True)