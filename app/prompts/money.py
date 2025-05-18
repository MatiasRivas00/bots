from google import genai
from typing import List

from app.schemas.mongo import PythonObjectId

from app.models.mongo.money import Category, Tag, Transaction
from app.schemas.money import LLMCategory, LLMTag, LLMTransaction

from app.schemas.money import BaseSchema

from app.core.constants import GEMINI_TOKEN

client = genai.Client(api_key=GEMINI_TOKEN)

def get_category_from_message(message: str, user_id: PythonObjectId) -> BaseSchema:
    """
    Get the category from the message
    """

    categories = Category.find({"user_id": user_id})
    formatted_categories = "\n".join([
        f"- {category.name}"
        for category in categories
    ])

    prompt = f"""
    Obtenen la categoría que describe de mejor manera la transacción del siguiente mensaje: {message}
    
    Las categorías existentes son:
    {formatted_categories}

    Devuelve una sola categoría o una lista de categorías según corresponda.
    El name de la categoría debe ser alguno de los que se muestra en las categorías existentes.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": LLMCategory
        }
    )

    category_data = response.parsed
    return Category.find_one({"name": category_data.name}) or Category.find_one({"name": "Otro"})

def get_tag_from_message(message: str, user_id: PythonObjectId) -> List[BaseSchema]:
    existing_tags = Tag.find({"is_active": True, "user_id": user_id})
    existing_tags_length = len(existing_tags)

    categories = Category.find({"user_id": user_id})

    formatted_categories = "\n".join([
        f"- {category.name}"
        for category in categories
    ])

    formatted_tags = "\n".join([
        f"- {tag.name}"
        for tag in existing_tags
    ])

    prompt = f"""
    Obtén la etiqueta o las etiquetas que describen de mejor manera la transacción del siguiente mensaje: {message}

    Reglas para las etiquetas:  
    1. Las etiquetas deben ser en minúsculas (lowercase)
    2. No usar tildes o caracteres especiales
    3. Si la etiqueta tiene más de una palabra, separarla con guion bajo (_)
    4. Puedes crear un máximo de 5 etiquetas por transacción
    5. Solo crear etiquetas nuevas si NO existe una etiqueta o combinación de etiquetas que describan adecuadamente la transacción
    6. La etiqueta debe estar en español
    7. La etiqueta no puede tener más de 20 caracteres
    8. Si la etiqueta es una categoría o es un sinónimo de una categoría, no crear una etiqueta para ella

    Las etiquetas se clasifican en tres tipos:
    1. Tags de Persona (con quién): amigos, mama, pareja, trabajo, etc.
    2. Tags de Evento/Situación (cuándo/contexto): navidad, fin_de_mes, cumpleanos, feriado, finde, etc.
    3. Tags de Proyecto/Propósito (objetivo): viaje, mudanza, nuevo_departamento, bodas, etc.

    Las etiquetas existentes son:
    {formatted_tags}

    Las categorías existentes son:
    {formatted_categories}

    El máximo número de etiquetas permitidas es 30 y actualmente hay {existing_tags_length}.
    Debes considerar este máximo, ya que si eliges nuevas etiquetas, estas serán parte de las existentes y podrían hacer que se supere el límite de 30.

    Devuelve una lista de etiquetas o una sola etiqueta según corresponda.
    La propiedad is_active debe ser True.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": list[LLMTag]
        }
    )
    
    tags_data = response.parsed
    tags: List[BaseSchema] = []

    for llm_tag in tags_data:
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

def get_transaction_from_message(message: str) -> str:
    """
    Get the transaction from the message
    """
    return "transaction"


