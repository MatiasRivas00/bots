from app.prompts.money import get_category_from_message, get_tag_from_message
from app.models.mongo.money import Category, Tag
from app.models.mongo.user import User
from app.models.mongo.money_populate import populate_categories_for_user

user = User.find_one({"telegram_id": 1234567890})
categories = Category.find({"user_id": user.id})
if not categories:
    populate_categories_for_user(user.id)

print(user)

def test_prompts():
    # Test messages - add more examples as needed
    test_messages = [
        "Almuerzo con amigos en el centro",
        "Compra de supermercado para la semana",
        "Pago de Netflix mensual",
        "Regalo de cumpleaños para mamá"
    ]
    
    print("\n=== Testing Category and Tag Extraction ===\n")
    
    for message in test_messages:
        print(f"\nTesting message: '{message}'")
        print("-" * 50)
        
        try:
            # Test category extraction
            category = get_category_from_message(message, user.id)
            print(f"Category: {category.name} (ID: {category.id})")
            
            # Test tag extraction
            tags = get_tag_from_message(message, user.id)
            print("\nTags:")
            for tag in tags:
                print(f"- {tag.name} (ID: {tag.id})")
        
        except Exception as e:
            print(f"Error processing message: {str(e)}")
        
        print("-" * 50)
    User.delete({"telegram_id": "1234567890"})
if __name__ == "__main__":
    test_prompts()