from google import genai
from typing import List

from app.schemas.mongo import PythonObjectId

from app.models.mongo.money import Category, Tag, Transaction
from app.schemas.money import LLMCategory, LLMTag, LLMTransaction

from app.schemas.money import BaseSchema

from app.core.constants import GEMINI_TOKEN

client = genai.Client(api_key=GEMINI_TOKEN)

def get_llm_category_from_message(message: str, user_id: PythonObjectId) -> LLMCategory:
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

    return response.parsed

def get_llm_tags_from_message(message: str, user_id: PythonObjectId) -> List[LLMTag]:
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

    return response.parsed

def get_llm_transaction_from_message(message: str) -> str:
    """
    Get the transaction from the message
    """
    prompt = f"""
    Obtén la transacción que describe de mejor manera la transacción del siguiente mensaje: {message}

    Reglas para la transacción:
    1. La transacción debe tener los siguientes campos: amount, currency, type, description, payment_method, timestamp, message_text
    2. El amount debe ser un número positivo o 0 si no se puede determinar.
    3. El currency debe ser CLP por defecto, a no ser que se especifique otra moneda en el mensaje.
    4. El type debe ser income o expense.
    5. El description debe ser una descripción de la transacción, no debe ser el mensaje original, y no debe superar los 100 caracteres.
    6. El payment_method debe ser alguno de los que se muestra en las categorías existentes, si no se puede determinar, usar debit_card. (cash, debit_card, credit_card, transfer, other son los tipos disponibles)
    7. El timestamp debe ser la fecha y hora actual.
    8. El message_text debe ser el mensaje original.

    Los mensajes pueden usar jergas chilenas, estas son las más comunes:
     - luca o lucas: una luca son 1000 pesos chilenos, y tres lucas son 3000 pesos chilenos por ejemplo.
     - cabros o los k: se refiere a un grupo de amigos.
     - si digo 3k o 4k u otro numero que puede ser interpretado como valor monetario, 3k y 4k se refiere a 3000, 4000 pesos chilenos por ejemplo.
    """
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": LLMTransaction
    }
    )

    return response.parsed


