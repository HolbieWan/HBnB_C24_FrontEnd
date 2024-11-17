# user.py

from app.extensions import db, bcrypt
from app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError


class User(BaseModel):
    __tablename__ = 'users'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', back_populates='place_owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='user', lazy=True, cascade='all, delete-orphan')

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)