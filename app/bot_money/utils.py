from app.schemas.money import Transaction as TransactionSchema
from app.models.mongo.money import Category, Tag
import pytz
from wcwidth import wcswidth

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

def ljust_visual(s: str, width: int) -> str:
    current_width = wcswidth(s)
    if current_width < width:
        return s + " " * (width - current_width)
    return s

def parse_summary_to_reply(summary: dict) -> str:
    parsed_summary = ""
    parsed_summary += "💰 Resumen de gastos por categoría\n\n"
    
    # Get all categories from either section since they're the same
    categories = list(summary["expense"].keys())
    max_length = max([wcswidth(category) for category in categories])
    
    # Format expenses
    for category in categories:
        amount = summary["expense"][category]
        parsed_summary += f"{ljust_visual(category, max_length)}: ${amount}\n"
    
    total_expense = sum(summary["expense"].values())
    parsed_summary += f"{ljust_visual('Total', max_length)}: ${total_expense}"

    parsed_summary += "\n\n💰 Resumen de ingresos por categoría\n\n"
    
    # Format income using the same categories
    for category in categories:
        amount = summary["income"][category]
        parsed_summary += f"{ljust_visual(category, max_length)}: ${amount}\n"
    total_income = sum(summary["income"].values())
    parsed_summary += f"{ljust_visual('Total', max_length)}: ${total_income}\n\n"

    parsed_summary += f"balance total: ${total_income - total_expense}"
    return parsed_summary
