from app.models.mongo.money import Category
from app.schemas.money import Category as CategorySchema
from app.schemas.mongo import PythonObjectId

def populate_categories_for_user(user_id: PythonObjectId):
    """
    | Categoría padre            | ¿Qué incluye? |
    |----------------------------|----------------|
    | **Alimentación**           | Supermercado, restaurantes, delivery, snacks |
    | **Transporte**             | Combustible, transporte público, Uber, mantenciones |
    | **Vivienda**               | Arriendo, hipoteca, servicios básicos (agua, luz, gas), reparaciones |
    | **Salud**                  | Medicamentos, consultas, exámenes, seguros médicos |
    | **Educación**              | Aranceles, libros, cursos, plataformas educativas |
    | **Ocio y entretenimiento** | Cine, vacaciones, hobbies, conciertos, juegos, salidas |
    | **Ropa y cuidado personal**| Ropa, calzado, peluquería, cosméticos, higiene |
    | **Familia y relaciones**   | Regalos, celebraciones, mascotas, gastos relacionados con hijos |
    | **Tecnología y suscripciones** | Celular, internet, apps, gadgets, Netflix, Spotify |
    | **Finanzas y deudas**      | Créditos, pagos de intereses, comisiones bancarias, seguros |
    | **Ahorro e inversión**     | Aportes a cuentas de ahorro, fondos mutuos, compra de acciones |
    | **Ingresos**               | Sueldos, bonos, reembolsos, ventas, ingresos extra |
    | **Otro**                   | Otros gastos |
    """

    categories = [
        CategorySchema(name="Alimentación", description="Supermercado, restaurantes, delivery, snacks", user_id=user_id),
        CategorySchema(name="Transporte", description="Combustible, transporte público, Uber, mantenciones", user_id=user_id),
        CategorySchema(name="Vivienda", description="Arriendo, hipoteca, servicios básicos (agua, luz, gas), reparaciones", user_id=user_id),
        CategorySchema(name="Salud", description="Medicamentos, consultas, exámenes, seguros médicos", user_id=user_id),
        CategorySchema(name="Educación", description="Aranceles, libros, cursos, plataformas educativas", user_id=user_id),
        CategorySchema(name="Ocio y entretenimiento", description="Cine, vacaciones, hobbies, conciertos, juegos, salidas", user_id=user_id),
        CategorySchema(name="Ropa y cuidado personal", description="Ropa, calzado, peluquería, cosméticos, higiene", user_id=user_id),
        CategorySchema(name="Familia y relaciones", description="Regalos, celebraciones, mascotas, gastos relacionados con hijos", user_id=user_id),
        CategorySchema(name="Tecnología y suscripciones", description="Celular, internet, apps, gadgets, Netflix, Spotify", user_id=user_id),
        CategorySchema(name="Finanzas y deudas", description="Créditos, pagos de intereses, comisiones bancarias, seguros", user_id=user_id),
        CategorySchema(name="Ahorro e inversión", description="Aportes a cuentas de ahorro, fondos mutuos, compra de acciones", user_id=user_id),
        CategorySchema(name="Ingresos", description="Sueldos, bonos, reembolsos, ventas, ingresos extra", user_id=user_id),
        CategorySchema(name="Otro", description="Otros gastos", user_id=user_id),
    ]

    for category in categories:
        Category.create(category.model_dump())