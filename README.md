# 💰 Financial Tracker - Esquemas y Clasificación de Transacciones

Este proyecto permite registrar de forma estructurada **gastos, ingresos y aportes financieros** a partir de mensajes simples (como *"Gasté 2000 en una salida con amigos"*), usando esquemas Pydantic que modelan la información para permitir análisis financieros claros y útiles.

## 📦 Esquemas principales

- **User**: Representa al usuario del sistema (incluye autenticación básica).
- **Transaction**: Representa un evento financiero (gasto o ingreso).
- **Category**: Clasificación obligatoria y jerárquica para cada transacción.
- **Tag**: Etiquetas complementarias y limitadas, inferidas o seleccionadas para enriquecer el contexto de cada transacción.

Estos modelos están diseñados para ser fácilmente inferibles desde texto por una LLM, manteniendo estructura y consistencia en los datos.

---

## 📁 Categorías principales

Cada transacción debe pertenecer a una de las siguientes **12 categorías padre**, pensadas para cubrir los ámbitos más comunes de la vida personal y familiar:

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

---

## 🏷️ Tipología de Tags

Los **tags** funcionan como anotaciones adicionales que capturan el contexto **personal**, **temporal** o **estratégico** de una transacción. Se pueden clasificar en tres tipos funcionales:

---

### 1. 👥 Tags de Persona  
**¿Con quién ocurrió la transacción?**

Estos tags ayudan a entender los vínculos sociales o roles con los que se asocian ciertos gastos o ingresos. Son especialmente útiles para:

- Analizar cuánto gastas en salidas con determinadas personas.
- Identificar patrones de gasto en actividades grupales o familiares.

**Ejemplos:**
- `#amigos`
- `#mamá`
- `#pareja`
- `#trabajo` (como contexto interpersonal, no como propósito)

> *Ejemplo de uso:*  
> "Fui a cenar con mi hermana y mi pareja" → `#hermana`, `#pareja`

---

### 2. 📅 Tags de Evento o Situación  
**¿Cuándo o en qué contexto temporal o situacional ocurrió?**

Este tipo de tag permite detectar gastos que aparecen recurrentemente bajo ciertas condiciones o momentos del calendario.

**Ejemplos:**
- `#navidad`
- `#fin_de_mes`
- `#cumpleaños`
- `#feriado`
- `#finde`

> *Ejemplo de uso:*  
> "Compré regalos de navidad para la familia" → `#navidad`

**Consejo:**  
Considera estandarizar eventos comunes para mantener coherencia. Evita variantes como `#fin_de_semana`, `#finde`, `#fin-de-semana`.

---

### 3. 🎯 Tags de Proyecto o Propósito  
**¿Forma parte de un objetivo o esfuerzo mayor?**

Sirve para agrupar gastos o ingresos que pertenecen a una iniciativa de mediano/largo plazo. Muy útil para:

- Saber cuánto has gastado en un viaje, mudanza, boda, renovación, etc.
- Evaluar inversiones personales o de ocio.

**Ejemplos:**
- `#viaje_a_Perú`
- `#mudanza`
- `#nuevo_departamento`
- `#bodas_2025`

> *Ejemplo de uso:*  
> "Reservé el hotel para nuestro viaje a Perú" → `#viaje_a_Perú`

**Consejo:**  
Mantén consistencia en el nombre de los proyectos. Se recomienda usar formato snake_case (`#viaje_norte`, no `#Viaje Norte`) para facilitar el análisis programático.

---

## 📌 Reglas para implementación

- Máximo **30 tags por usuario** para evitar dispersión.
- Cada tag debe estar asociado internamente a un **tipo** (`persona`, `evento`, `proyecto`), aunque esto no tiene que ser visible para el usuario final.
- La LLM debería:
  - **Priorizar tags existentes.**
  - Si crea uno nuevo, **asignarle automáticamente su tipo funcional**, idealmente mediante una lógica heurística o de aprendizaje.
  - Evitar duplicados semánticos (`#finde` y `#fin_de_semana`).


---

### 🧩 Sobre las Subcategorías

Las **subcategorías** permiten refinar aún más la clasificación dentro de cada categoría padre. A diferencia de las tags, **forman parte de la jerarquía estructurada del modelo de datos** y deben ser **predeterminadas y limitadas por categoría**, para garantizar consistencia.

- Cada categoría puede tener de 3 a 10 subcategorías como máximo.
- Son clave para análisis específicos sin perder orden, por ejemplo:
  - `Alimentación → Supermercado`
  - `Ocio → Cine`
  - `Transporte → Combustible`
- Las subcategorías son gestionadas por el sistema y no por los usuarios, lo cual:
  - Permite mantener un vocabulario controlado.
  - Evita confusiones entre subcategorías y tags.

**Comparación rápida**:

| Aspecto             | Subcategoría                   | Tag                           |
|---------------------|--------------------------------|-------------------------------|
| Obligatoria         | ✅ Sí                          | ❌ No                         |
| Jerárquica          | ✅ Sí (dentro de categoría)    | ❌ No (libre)                 |
| Control de cantidad | ✅ Fijo por sistema            | ✅ Máximo 30 por usuario      |
| Propósito           | Clasificación estructurada     | Contexto adicional flexible  |
