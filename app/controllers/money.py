from typing import List
from app.prompts.money import get_llm_transaction_from_message, get_llm_category_from_message, get_llm_tags_from_message

from app.schemas.mongo import PythonObjectId
from app.schemas.money import Transaction as TransactionSchema
from app.schemas.money import Category as CategorySchema
from app.schemas.money import Tag as TagSchema

from app.models.mongo.money import Transaction, Category, Tag

from app.controllers.utils import get_last_monday
from datetime import datetime

def get_or_create_tags_from_message(message: str, user_id: PythonObjectId) -> List[TagSchema]:
    llm_tags = get_llm_tags_from_message(message, user_id)
    tags: List[TagSchema] = []
    for llm_tag in llm_tags:
        tag = Tag.find_one({"name": llm_tag.name, "user_id": user_id})
        if tag is not None and tag.is_active:
            tags.append(tag)
        elif tag is not None and not tag.is_active:
            Tag.update({"name": llm_tag.name}, {"is_active": True})
            tag.is_active = True
            tags.append(tag)
        else:
            tag = Tag.create({"name": llm_tag.name, "is_active": True, "user_id": user_id})
            print(f"Tag created: {tag.name}")
            tags.append(tag)
    return tags

def get_category_from_message(message: str, user_id: PythonObjectId) -> CategorySchema:
    llm_category = get_llm_category_from_message(message, user_id)
    category = Category.find_one({"name": llm_category.name, "user_id": user_id})
    return category

def create_transaction_from_message(message: str, user_id: PythonObjectId) -> TransactionSchema:
    llm_transaction = get_llm_transaction_from_message(message)
    category = get_category_from_message(message, user_id)
    tags = get_or_create_tags_from_message(message, user_id)
    
    transaction = Transaction.create({
        **llm_transaction.model_dump(),
        "category_id": category.id,
        "tag_ids": [tag.id for tag in tags],
        "user_id": user_id
    })

    return transaction

def week_summary(user_id: PythonObjectId) -> dict:
    last_monday = get_last_monday()
    transactions_by_category = {"income": {}, "expense": {}}
    categories = Category.find({"user_id": user_id})
    for category in categories:
        transactions = Transaction.find({"user_id": user_id, "timestamp": {"$gte": last_monday}, "category_id": category.id, "type": "expense"})
        total_amount = sum([transaction.amount for transaction in transactions])
        transactions_by_category["expense"][category.name] = total_amount
    for category in categories:
        transactions = Transaction.find({"user_id": user_id, "timestamp": {"$gte": last_monday}, "category_id": category.id, "type": "income"})
        total_amount = sum([transaction.amount for transaction in transactions])
        transactions_by_category["income"][category.name] = total_amount
    return transactions_by_category

def month_summary(user_id: PythonObjectId) -> dict:
    month_first_day = datetime.now().replace(day=1)
    transactions_by_category = {"income": {}, "expense": {}}
    categories = Category.find({"user_id": user_id})
    for category in categories:
        transactions = Transaction.find({"user_id": user_id, "timestamp": {"$gte": month_first_day}, "category_id": category.id, "type": "expense"})
        total_amount = sum([transaction.amount for transaction in transactions])
        transactions_by_category["expense"][category.name] = total_amount
    for category in categories:
        transactions = Transaction.find({"user_id": user_id, "timestamp": {"$gte": month_first_day}, "category_id": category.id, "type": "income"})
        total_amount = sum([transaction.amount for transaction in transactions])
        transactions_by_category["income"][category.name] = total_amount
    return transactions_by_category

def year_summary(user_id: PythonObjectId) -> dict:
    year_first_day = datetime.now().replace(day=1, month=1)
    transactions_by_category = {"income": {}, "expense": {}}
    categories = Category.find({"user_id": user_id})
    for category in categories:
        transactions = Transaction.find({"user_id": user_id, "timestamp": {"$gte": year_first_day}, "category_id": category.id, "type": "expense"})
        total_amount = sum([transaction.amount for transaction in transactions])
        transactions_by_category["expense"][category.name] = total_amount
    for category in categories:
        transactions = Transaction.find({"user_id": user_id, "timestamp": {"$gte": year_first_day}, "category_id": category.id, "type": "income"})
        total_amount = sum([transaction.amount for transaction in transactions])
        transactions_by_category["income"][category.name] = total_amount
    return transactions_by_category