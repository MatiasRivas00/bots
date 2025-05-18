from app.schemas.money import Transaction as TransactionSchema
from app.models.mongo.money import Category, Tag
import pytz

def parse_transaction_to_reply(transaction: TransactionSchema) -> str:
    transaction_category = Category.find_one({"_id": transaction.category_id})
    parsed_category = f"{transaction_category.name}"
    transaction_tags = [Tag.find_one({"_id": tag_id}).name for tag_id  in transaction.tag_ids]
    parsed_tags = ', '.join([f"#{tag}" for tag in transaction_tags])
    chile_tz = pytz.timezone('America/Santiago')
    chile_time = transaction.timestamp.astimezone(chile_tz)

    parsed_transaction = f"""
💭 {transaction.description} ({parsed_category}) {parsed_tags}
💲 {transaction.amount} {transaction.currency} ({transaction.payment_method}) ({transaction.type})
⏰ {chile_time.strftime('%Y-%m-%d %H:%M')}
⚙#{transaction.id}"""

    return parsed_transaction
