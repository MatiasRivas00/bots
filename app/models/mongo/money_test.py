import pytest
from datetime import datetime, UTC
from app.schemas.mongo import PythonObjectId

from app.models.mongo.money import Category, Tag, Transaction

@pytest.fixture
def user_id():
    """Fixture to provide a consistent user_id for tests"""
    return PythonObjectId()

@pytest.fixture(autouse=True)
def cleanup():
    """Clean up the collections after each test"""
    yield
    Category.delete({})
    Tag.delete({})
    Transaction.delete({})

# Category Tests
def test_category_crud(user_id):
    # Create
    category_data = {
        "user_id": user_id,
        "name": "Test Category",
        "parent_id": None
    }
    category = Category.create(category_data)
    assert category.name == category_data["name"]
    assert category.user_id == user_id
    assert category.parent_id is None
    assert hasattr(category, "id")
    assert hasattr(category, "created_at")

    # Read
    retrieved_category = Category.find_one({"_id": category.id})
    assert retrieved_category.name == category_data["name"]

    # Update
    update_data = {"name": "Updated Category"}
    Category.update({"_id": category.id}, update_data)
    updated_category = Category.find_one({"_id": category.id})
    assert updated_category.name == update_data["name"]

    # Delete
    Category.delete({"_id": category.id})
    deleted_category = Category.find_one({"_id": category.id})
    assert deleted_category is None

def test_category_with_parent(user_id):
    # Create parent category
    parent_category = Category.create({
        "user_id": user_id,
        "name": "Parent Category"
    })

    # Create child category
    child_category = Category.create({
        "user_id": user_id,
        "name": "Child Category",
        "parent_id": parent_category.id
    })

    assert child_category.parent_id == parent_category.id
    
    # Verify child category
    retrieved_child = Category.find_one({"_id": child_category.id})
    assert retrieved_child.parent_id == parent_category.id

def test_category_bulk_operations(user_id):
    # Bulk Create
    categories = [
        {
            "user_id": user_id,
            "name": f"Category {i}",
            "parent_id": None
        }
        for i in range(3)
    ]
    for category in categories:
        Category.create(category)

    # Bulk Read
    found_categories = list(Category.find({"user_id": user_id}))
    assert len(found_categories) == 3

    # Bulk Delete
    Category.delete({"user_id": user_id})
    remaining_categories = list(Category.find({"user_id": user_id}))
    assert len(remaining_categories) == 0

# Tag Tests
def test_tag_crud(user_id):
    # Create
    tag_data = {
        "user_id": user_id,
        "name": "Test Tag",
        "is_active": True
    }
    tag = Tag.create(tag_data)
    assert tag.name == tag_data["name"]
    assert tag.user_id == user_id
    assert tag.is_active is True
    assert hasattr(tag, "id")
    assert hasattr(tag, "created_at")

    # Read
    retrieved_tag = Tag.find_one({"_id": tag.id})
    assert retrieved_tag.name == tag_data["name"]

    # Update
    update_data = {"is_active": False}
    Tag.update({"_id": tag.id}, update_data)
    updated_tag = Tag.find_one({"_id": tag.id})
    assert updated_tag.is_active is False

    # Delete
    Tag.delete({"_id": tag.id})
    deleted_tag = Tag.find_one({"_id": tag.id})
    assert deleted_tag is None

def test_tag_bulk_operations(user_id):
    # Bulk Create
    tags = [
        {
            "user_id": user_id,
            "name": f"Tag {i}",
            "is_active": True
        }
        for i in range(3)
    ]
    for tag in tags:
        Tag.create(tag)

    # Bulk Read
    found_tags = list(Tag.find({"user_id": user_id}))
    assert len(found_tags) == 3

    # Bulk Update
    Tag.update(
        {"user_id": user_id},
        {"is_active": False}
    )
    inactive_tags = list(Tag.find({"user_id": user_id, "is_active": False}))
    assert len(inactive_tags) == 3

    # Bulk Delete
    Tag.delete({"user_id": user_id})
    remaining_tags = list(Tag.find({"user_id": user_id}))
    assert len(remaining_tags) == 0

# Transaction Tests
def test_transaction_crud(user_id):
    # Create required category and tag first
    category = Category.create({
        "user_id": user_id,
        "name": "Test Category"
    })
    tag = Tag.create({
        "user_id": user_id,
        "name": "Test Tag"
    })

    # Create
    transaction_data = {
        "user_id": user_id,
        "amount": 100.50,
        "currency": "CLP",
        "type": "expense",
        "description": "Test Transaction",
        "category_id": category.id,
        "payment_method": "debit_card",
        "tag_ids": [tag.id],
        "timestamp": datetime.now(UTC),
        "message_text": "Test message"
    }
    transaction = Transaction.create(transaction_data)
    assert transaction.amount == transaction_data["amount"]
    assert transaction.description == transaction_data["description"]
    assert transaction.category_id == category.id
    assert transaction.tag_ids == [tag.id]
    assert transaction.currency == "CLP"
    assert transaction.payment_method == "debit_card"
    assert hasattr(transaction, "id")
    assert hasattr(transaction, "created_at")

    # Read
    retrieved_transaction = Transaction.find_one({"_id": transaction.id})
    assert retrieved_transaction.amount == transaction_data["amount"]

    # Update
    update_data = {"amount": 200.75}
    Transaction.update({"_id": transaction.id}, update_data)
    updated_transaction = Transaction.find_one({"_id": transaction.id})
    assert updated_transaction.amount == update_data["amount"]

    # Delete
    Transaction.delete({"_id": transaction.id})
    deleted_transaction = Transaction.find_one({"_id": transaction.id})
    assert deleted_transaction is None

def test_transaction_validation(user_id):
    category = Category.create({
        "user_id": user_id,
        "name": "Test Category"
    })
    
    # Create tags
    tags = [Tag.create({
        "user_id": user_id,
        "name": f"Tag {i}"
    }) for i in range(6)]  # Creating 6 tags to test validation

    # Test validation of max 5 tags
    with pytest.raises(ValueError):
        transaction_data = {
            "user_id": user_id,
            "amount": 100.0,
            "currency": "CLP",
            "type": "expense",
            "description": "Test Transaction",
            "category_id": category.id,
            "payment_method": "debit_card",
            "tag_ids": [tag.id for tag in tags],  # Adding 6 tags
            "timestamp": datetime.now(UTC),
            "message_text": "Test message"
        }
        Transaction.create(transaction_data)

def test_transaction_filters(user_id):
    # Create test data
    category1 = Category.create({
        "user_id": user_id,
        "name": "Category 1"
    })
    category2 = Category.create({
        "user_id": user_id,
        "name": "Category 2"
    })
    tag1 = Tag.create({
        "user_id": user_id,
        "name": "Tag 1"
    })
    tag2 = Tag.create({
        "user_id": user_id,
        "name": "Tag 2"
    })

    now = datetime.now(UTC)
    transactions = [
        {
            "user_id": user_id,
            "amount": 100.0,
            "currency": "CLP",
            "type": "expense",
            "description": "Transaction 1",
            "category_id": category1.id,
            "payment_method": "cash",
            "tag_ids": [tag1.id],
            "timestamp": now,
            "message_text": "Message 1"
        },
        {
            "user_id": user_id,
            "amount": 200.0,
            "currency": "CLP",
            "type": "income",
            "description": "Transaction 2",
            "category_id": category2.id,
            "payment_method": "credit_card",
            "tag_ids": [tag2.id],
            "timestamp": now,
            "message_text": "Message 2"
        }
    ]
    for transaction in transactions:
        Transaction.create(transaction)

    # Test filtering by category
    category1_transactions = list(Transaction.find({
        "user_id": user_id,
        "category_id": category1.id
    }))
    assert len(category1_transactions) == 1
    assert category1_transactions[0].amount == 100.0

    # Test filtering by tag
    tag2_transactions = list(Transaction.find({
        "user_id": user_id,
        "tag_ids": tag2.id
    }))
    assert len(tag2_transactions) == 1
    assert tag2_transactions[0].amount == 200.0

    # Test filtering by type
    income_transactions = list(Transaction.find({
        "user_id": user_id,
        "type": "income"
    }))
    assert len(income_transactions) == 1
    assert income_transactions[0].amount == 200.0

    # Test filtering by payment method
    cash_transactions = list(Transaction.find({
        "user_id": user_id,
        "payment_method": "cash"
    }))
    assert len(cash_transactions) == 1
    assert cash_transactions[0].amount == 100.0
