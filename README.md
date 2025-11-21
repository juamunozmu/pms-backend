# PMS Backend - Parking & Car Wash Management System

Sistema de gestión integral para negocio de parqueadero y lavado de vehículos.

## 🏗️ Arquitectura

- **Clean Architecture** + **DDD** + **Hexagonal (Ports & Adapters)**
- **Framework**: FastAPI 0.109+
- **Python**: 3.12+
- **Base de Datos**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 (async)
- **Migraciones**: Alembic

## 📁 Estructura del Proyecto

Ver [STRUCTURE.md](./STRUCTURE.md) para detalles completos de la arquitectura de carpetas.

```
app/
├── domain/              # Lógica de negocio pura (entidades, value objects, servicios)
├── application/         # Casos de uso (orquestación)
├── infrastructure/      # Adaptadores (BD, email, export)
├── api/                 # Endpoints FastAPI
└── core/                # Configuración global
```

## 🚀 Inicio Rápido

### 1. Clonar repositorio
```bash
git clone https://github.com/pms-project-rc/pms-backend.git
cd pms-backend
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus valores
```

### 5. Ejecutar con Docker (Recomendado)
```bash
cd ../pms-infra
docker-compose up -d
```

### 6. Ejecutar migraciones
```bash
alembic upgrade head
```

### 7. Acceder a la API
- **Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Health**: http://localhost:8000/health

## 📚 Documentación

- [Estructura del Proyecto](./STRUCTURE.md)
- [Especificaciones del Producto](../pms-docs/01-definicion-proyecto/especificacionesGeneralesProducto.md)
- [Tarifas y Precios](../pms-docs/01-definicion-proyecto/tarifas-y-precios.md)
- [Modelo de Base de Datos](../pms-docs/02-arquitectura/dbdiagram.dbml)

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/unit/domain/
pytest tests/integration/
```

## 🛠️ Comandos Útiles

### Migraciones
```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Linting y Formato
```bash
# Black (formato)
black app/

# Ruff (lint)
ruff check app/

# MyPy (type checking)
mypy app/
```

### Seed Data
```bash
python scripts/seed_data.py
```

## 👥 Equipo y Asignación de Módulos

- **Dev A**: `users/` + `auth/` + seguridad
- **Dev B**: `parking/` + `washing/` + `financial/` (bonos/vales)
- **Dev C**: `pricing/` + `subscriptions/` + `agreements/`
- **Dev D**: `reporting/` + `analytics/` + dashboard + turnos

## 📝 Convenciones

- **Naming**: snake_case (archivos/funciones), PascalCase (clases)
- **Docstrings**: Google style
- **Type hints**: Obligatorios en funciones públicas
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, etc.)

## 🔒 Seguridad

- JWT para autenticación
- Bcrypt para hash de contraseñas
- Validación de permisos por rol
- Auditoría de cambios críticos

## 📊 Bounded Contexts

1. **Users** - Autenticación y gestión de usuarios
2. **Parking** - Gestión de parqueadero
3. **Washing** - Servicios de lavado
4. **Financial** - Gastos, bonos, vales, turnos
5. **Pricing** - Tarifas y configuración comercial
6. **Subscriptions** - Mensualidades
7. **Agreements** - Convenios empresariales
8. **Reporting** - Reportes y analítica

## 🌐 API Endpoints (v1)

- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/logout` - Cerrar sesión
- `POST /api/v1/parking/entry` - Registrar entrada
- `POST /api/v1/parking/exit` - Registrar salida
- `POST /api/v1/washing/services` - Crear servicio de lavado
- `GET /api/v1/dashboard/metrics` - Métricas del dashboard
- ... (ver /api/docs para lista completa)

## 📄 Licencia

MIT

## 🤝 Contribuciones

Ver guía de contribución en el repositorio principal.
API Rest and Business logic in FastAPI
