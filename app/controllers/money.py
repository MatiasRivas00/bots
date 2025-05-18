from typing import List
from app.prompts.money import get_llm_transaction_from_message, get_llm_category_from_message, get_llm_tags_from_message

from app.schemas.mongo import PythonObjectId
from app.schemas.money import Transaction as TransactionSchema
from app.schemas.money import Category as CategorySchema
from app.schemas.money import Tag as TagSchema

from app.models.mongo.money import Transaction, Category, Tag

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


