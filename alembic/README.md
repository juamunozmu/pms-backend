# 🔄 Alembic - Guía de Migraciones de Base de Datos

## 📚 ¿Qué es Alembic?

Alembic es una herramienta de **migraciones de base de datos** para SQLAlchemy. 

**Piensa en Alembic como "Git para tu base de datos":**
- Cada cambio en la estructura de la BD es un "commit" (migración)
- Puedes ver el historial de cambios
- Puedes hacer rollback si algo sale mal
- Todos los desarrolladores tienen los mismos cambios

---

## 🎯 Conceptos Clave

### 1. **Migración (Migration)**
Un archivo Python que describe cómo cambiar la estructura de la base de datos.

Ejemplo: Agregar una columna `photo_url` a la tabla `washers`

### 2. **Revision**
Un ID único para cada migración (como un commit hash en Git)

Ejemplo: `a1b2c3d4e5f6`

### 3. **upgrade()**
Función que aplica los cambios (ir hacia adelante)

### 4. **downgrade()**
Función que revierte los cambios (rollback)

---

## 🚀 Comandos Principales

### **Ver el estado actual**
```bash
# Ver en qué versión está la base de datos
alembic current

# Ver historial de migraciones
alembic history

# Ver migraciones pendientes
alembic heads
```

### **Crear una migración**

#### **Opción 1: Migración vacía (manual)**
```bash
alembic revision -m "add photo to washers"
```
Esto crea un archivo vacío donde TÚ escribes el código SQL.

#### **Opción 2: Migración automática (detecta cambios)**
```bash
alembic revision --autogenerate -m "add photo to washers"
```
Alembic compara tus modelos de SQLAlchemy con la BD y genera el código automáticamente ✨

### **Aplicar migraciones**
```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar solo la siguiente migración
alembic upgrade +1

# Aplicar hasta una revisión específica
alembic upgrade a1b2c3d4e5f6
```

### **Revertir migraciones (rollback)**
```bash
# Revertir la última migración
alembic downgrade -1

# Revertir hasta una revisión específica
alembic downgrade a1b2c3d4e5f6

# Revertir TODAS las migraciones (⚠️ CUIDADO)
alembic downgrade base
```

---

## 📋 Flujo de Trabajo Típico

### **Escenario: Necesitas agregar una columna `photo_url` a `washers`**

#### **Paso 1: Modificar el modelo SQLAlchemy**
```python
# app/infrastructure/database/models/users.py

class Washer(Base):
    __tablename__ = "washers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    # ... otras columnas ...
    
    # 🆕 Nueva columna
    photo_url = Column(String(255), nullable=True)
```

#### **Paso 2: Generar migración automáticamente**
```bash
alembic revision --autogenerate -m "add photo_url to washers"
```

Alembic detecta el cambio y crea un archivo como:
```
alembic/versions/001_add_photo_url_to_washers.py
```

#### **Paso 3: Revisar la migración generada**
```python
def upgrade() -> None:
    op.add_column('washers', sa.Column('photo_url', sa.String(255), nullable=True))

def downgrade() -> None:
    op.drop_column('washers', 'photo_url')
```

#### **Paso 4: Aplicar la migración**
```bash
alembic upgrade head
```

¡Listo! La columna se agregó a la base de datos sin perder datos.

---

## 🏗️ Estructura de una Migración

```python
"""add photo_url to washers

Revision ID: a1b2c3d4e5f6
Revises: b2c3d4e5f6a7
Create Date: 2024-01-15 10:30:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'a1b2c3d4e5f6'
down_revision = 'b2c3d4e5f6a7'  # Migración anterior
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Aplicar cambios (forward)"""
    # Crear tabla
    op.create_table(
        'washers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
    )
    
    # Agregar columna
    op.add_column('washers', sa.Column('photo_url', sa.String(255)))
    
    # Crear índice
    op.create_index('ix_washers_email', 'washers', ['email'])
    
    # Agregar foreign key
    op.create_foreign_key(
        'fk_washers_admin', 
        'washers', 'admins',
        ['admin_id'], ['id']
    )


def downgrade() -> None:
    """Revertir cambios (backward)"""
    op.drop_constraint('fk_washers_admin', 'washers')
    op.drop_index('ix_washers_email', 'washers')
    op.drop_column('washers', 'photo_url')
    op.drop_table('washers')
```

---

## 🎓 Ejemplo Práctico: Primera Migración

Vamos a crear la migración inicial con las 3 tablas de usuarios:

```bash
# 1. Generar migración automáticamente
alembic revision --autogenerate -m "create initial user tables"

# 2. Aplicar la migración
alembic upgrade head

# 3. Verificar en PostgreSQL
docker compose exec postgres psql -U pms_user -d pms_db -c "\dt"
```

---

## ⚙️ Operaciones Comunes

### **Crear Tabla**
```python
def upgrade():
    op.create_table(
        'washers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(100), unique=True),
    )
```

### **Agregar Columna**
```python
def upgrade():
    op.add_column('washers', sa.Column('phone', sa.String(20)))
```

### **Eliminar Columna**
```python
def upgrade():
    op.drop_column('washers', 'phone')
```

### **Modificar Columna**
```python
def upgrade():
    op.alter_column('washers', 'name', 
        existing_type=sa.String(100),
        type_=sa.String(200),  # Cambiar de 100 a 200
        nullable=False
    )
```

### **Crear Índice**
```python
def upgrade():
    op.create_index('ix_washers_email', 'washers', ['email'])
```

### **Crear Foreign Key**
```python
def upgrade():
    op.create_foreign_key(
        'fk_washers_admin',  # Nombre del constraint
        'washers',           # Tabla fuente
        'admins',            # Tabla destino
        ['admin_id'],        # Columna fuente
        ['id']               # Columna destino
    )
```

---

## 🚨 Buenas Prácticas

### ✅ **HACER**
- Siempre revisar las migraciones autogeneradas antes de aplicarlas
- Escribir mensajes descriptivos (`-m "mensaje claro"`)
- Probar migraciones en desarrollo antes de aplicarlas en producción
- Hacer backup de la BD antes de migraciones importantes
- Hacer commits de las migraciones en Git

### ❌ **NO HACER**
- NO modificar migraciones que ya están en producción
- NO eliminar archivos de migración
- NO hacer `alembic downgrade base` en producción sin backup
- NO saltarse migraciones (siempre `upgrade head`)

---

## 🔧 Troubleshooting

### **Error: "Target database is not up to date"**
```bash
# Aplicar migraciones pendientes
alembic upgrade head
```

### **Error: "Can't locate revision identified by..."**
```bash
# Sincronizar el estado de la BD con Alembic
alembic stamp head
```

### **Error: "FAILED: Can't proceed with --autogenerate"**
- Verificar que todos los modelos estén importados en `models/__init__.py`
- Verificar que la conexión a la BD sea correcta en `alembic.ini`

### **Ver SQL sin aplicar cambios**
```bash
alembic upgrade head --sql
```

---

## 📖 Documentación Oficial

- **Alembic Tutorial**: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- **Auto Generating Migrations**: https://alembic.sqlalchemy.org/en/latest/autogenerate.html
- **Operation Reference**: https://alembic.sqlalchemy.org/en/latest/ops.html

---

## 🎯 Siguientes Pasos

1. ✅ Crear modelos SQLAlchemy para todas las tablas
2. ✅ Generar migración inicial con `alembic revision --autogenerate`
3. ✅ Aplicar migración con `alembic upgrade head`
4. ✅ Verificar que las tablas se crearon correctamente

**¡Alembic te ahorrará muchos dolores de cabeza! 🚀**
