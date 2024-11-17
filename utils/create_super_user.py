from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app('config.DevelopmentConfig')

with app.app_context():
    superuser = User(
        first_name="Super",
        last_name="Admin",
        email="super.admin2@gmail.com",
        is_admin=True
    )
    superuser.hash_password("adminpassword")
    db.session.add(superuser)
    db.session.commit()

    print("Superuser created successfully!")


#To create super_user from this script, run in app repo: python3 -m utils.create_super_user