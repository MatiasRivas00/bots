from app.models.mongo.user import User
from app.models.mongo.money_populate import populate_categories_for_user
from app.schemas.users import User as UserSchema


def get_user_by_telegram_id(telegram_id: int) -> UserSchema:
    user = User.find_one({"telegram_id": telegram_id})
    if user is None:
        user = User.create({"telegram_id": telegram_id})
        populate_categories_for_user(user.id)
        print(f"User created: {user.id}")
    return user
