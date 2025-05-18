from app.prompts.money import get_llm_category_from_message, get_llm_tags_from_message, get_llm_transaction_from_message
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
        "Gasté 3 lucas en almuerzo con amigos en el centro, pagué en efectivo",
    ]
    
    print("\n=== Testing Category and Tag Extraction ===\n")
    
    for message in test_messages:
        print(f"\nTesting message: '{message}'")
        print("-" * 50)
        
        try:
            # Test category extraction
            category = get_llm_category_from_message(message, user.id)
            print(f"Category: {category.name}")
            
            # Test tag extraction
            tags = get_llm_tags_from_message(message, user.id)
            print("\nTags:")
            for tag in tags:
                print(f"- {tag.name}")

            transaction = get_llm_transaction_from_message(message)
            print(f"Transaction: {transaction.amount} {transaction.currency} {transaction.type} {transaction.description} {transaction.payment_method} {transaction.timestamp} {transaction.message_text}")
        
        except Exception as e:
            print(f"Error processing message: {str(e)}")
        
        print("-" * 50)
    User.delete({"telegram_id": "1234567890"})
if __name__ == "__main__":
    test_prompts()