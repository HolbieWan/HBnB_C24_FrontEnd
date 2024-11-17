from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app('config.DevelopmentConfig')

with app.app_context():
    superuser = User(
        first_name="Super",
        last_name="Admin",
        email="super.admin@gmail.com",
        is_admin=True
    )
    superuser.hash_password("adminpassword")
    db.session.add(superuser)
    db.session.commit()

    print("Superuser created successfully!")


# Creating super_user with CLI, run in app repo: python3 manage.py create_superuser