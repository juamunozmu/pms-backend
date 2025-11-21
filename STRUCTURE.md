# PMS Backend - Estructura del Proyecto

## 📁 Arquitectura de Carpetas

Este proyecto sigue **Clean Architecture + DDD + Hexagonal (Ports & Adapters)** para máxima escalabilidad y mantenibilidad.

```
pms-backend/
├── app/
│   ├── domain/              # 🔵 CAPA DE DOMINIO (Business Logic)
│   │   ├── users/           # Bounded Context: Usuarios y autenticación
│   │   │   ├── entities/    # Entidades del dominio (User, GlobalAdmin, etc.)
│   │   │   ├── value_objects/  # Objetos de valor (Email, Password, etc.)
│   │   │   ├── services/    # Servicios de dominio
│   │   │   ├── events/      # Eventos de dominio
│   │   │   └── repositories/  # Interfaces de repositorios (puertos)
│   │   ├── parking/         # Bounded Context: Parqueadero
│   │   │   ├── entities/    # ParkingRecord, Vehicle
│   │   │   ├── value_objects/  # Plate, VehicleType, Money
│   │   │   ├── services/    # ParkingFeeCalculator, ExemptionService
│   │   │   ├── events/      # VehicleEntered, VehicleExited
│   │   │   └── repositories/
│   │   ├── washing/         # Bounded Context: Lavado
│   │   │   ├── entities/    # WashingService, WashType
│   │   │   ├── value_objects/  # ServiceStatus, Duration
│   │   │   ├── services/    # WashingPriceCalculator
│   │   │   ├── events/      # WashStarted, WashFinished
│   │   │   └── repositories/
│   │   ├── financial/       # Bounded Context: Finanzas
│   │   │   ├── entities/    # Expense, Bonus, Voucher, Shift
│   │   │   ├── value_objects/  # Money, Percentage
│   │   │   ├── services/    # BonusCalculator, VoucherService
│   │   │   ├── events/      # BonusCalculated, ExpenseRecorded
│   │   │   └── repositories/
│   │   ├── pricing/         # Bounded Context: Tarifas y Configuración
│   │   │   ├── entities/    # Rate, BusinessConfig
│   │   │   ├── value_objects/  # RateAdjustment
│   │   │   ├── services/    # PricingService
│   │   │   ├── events/      # RatesUpdated
│   │   │   └── repositories/
│   │   ├── subscriptions/   # Bounded Context: Mensualidades
│   │   │   ├── entities/    # MonthlySubscription
│   │   │   ├── value_objects/  # SubscriptionPeriod
│   │   │   ├── services/    # SubscriptionAlertService
│   │   │   ├── events/      # SubscriptionExpiring
│   │   │   └── repositories/
│   │   ├── agreements/      # Bounded Context: Convenios Empresariales
│   │   │   ├── entities/    # Agreement, Fleet
│   │   │   ├── value_objects/  # Discount
│   │   │   ├── services/    # DiscountCalculator, FleetImporter
│   │   │   ├── events/      # AgreementCreated
│   │   │   └── repositories/
│   │   ├── reporting/       # Bounded Context: Reportes y Analítica
│   │   │   ├── entities/    # Report, Dashboard
│   │   │   ├── value_objects/  # ReportPeriod, Metrics
│   │   │   ├── services/    # ReportGenerator, MetricsCalculator
│   │   │   ├── events/      # ReportGenerated
│   │   │   └── repositories/
│   │   └── shared/          # Elementos compartidos entre contextos
│   │       ├── value_objects/  # Money, DateTime, etc.
│   │       ├── exceptions/  # DomainException, ValidationException
│   │       └── interfaces/  # IRepository, IEventPublisher
│   │
│   ├── application/         # 🟢 CAPA DE APLICACIÓN (Use Cases)
│   │   ├── auth/            # Casos de uso: Login, Logout, Password Recovery
│   │   ├── parking/         # Casos de uso: RegisterEntry, RegisterExit, etc.
│   │   ├── washing/         # Casos de uso: CreateService, AssignWasher, etc.
│   │   ├── shift/           # Casos de uso: OpenShift, CloseShift
│   │   ├── financial/       # Casos de uso: RecordExpense, CalculateBonus
│   │   ├── pricing/         # Casos de uso: UpdateRates, ApplyAdjustment
│   │   ├── reporting/       # Casos de uso: GenerateReport, ExportCSV
│   │   └── analytics/       # Casos de uso: CalculateMetrics, GetDashboard
│   │
│   ├── infrastructure/      # 🟡 CAPA DE INFRAESTRUCTURA (Adaptadores)
│   │   ├── database/
│   │   │   ├── models/      # SQLAlchemy models (mapeo ORM)
│   │   │   └── migrations/  # Migraciones Alembic (si no usas alembic/)
│   │   ├── repositories/    # Implementaciones concretas de repositorios
│   │   │   ├── users/       # SQLAlchemyUserRepository
│   │   │   ├── parking/     # SQLAlchemyParkingRepository
│   │   │   ├── washing/
│   │   │   ├── financial/
│   │   │   ├── pricing/
│   │   │   ├── subscriptions/
│   │   │   ├── agreements/
│   │   │   └── reporting/
│   │   ├── external_services/
│   │   │   ├── email/       # SMTP Email Service
│   │   │   ├── export/      # CSV/PDF Exporters
│   │   │   └── import/      # Excel/CSV Importers
│   │   └── messaging/       # Event Bus, Redis, etc. (futuro)
│   │
│   ├── api/                 # 🔴 CAPA DE PRESENTACIÓN (API REST)
│   │   ├── routes/
│   │   │   └── v1/          # Endpoints versión 1
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── parking.py
│   │   │       ├── washing.py
│   │   │       ├── shifts.py
│   │   │       ├── expenses.py
│   │   │       ├── bonuses.py
│   │   │       ├── rates.py
│   │   │       ├── subscriptions.py
│   │   │       ├── agreements.py
│   │   │       ├── reports.py
│   │   │       ├── analytics.py
│   │   │       └── admin.py
│   │   ├── dependencies/    # Dependency Injection (FastAPI Depends)
│   │   ├── middleware/      # Auth, CORS, Logging middleware
│   │   └── schemas/         # Pydantic schemas (DTOs)
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── parking.py
│   │       └── ...
│   │
│   ├── core/                # Configuración global
│   │   ├── config.py        # Settings (Pydantic BaseSettings)
│   │   ├── security.py      # JWT, hashing, tokens
│   │   └── database.py      # DB session, connection pool
│   │
│   └── main.py              # FastAPI app entry point
│
├── tests/                   # 🧪 PRUEBAS
│   ├── unit/                # Tests unitarios del dominio
│   │   ├── domain/
│   │   └── application/
│   ├── integration/         # Tests de integración (repos, DB)
│   └── e2e/                 # Tests end-to-end (API completa)
│
├── alembic/                 # Migraciones de base de datos
│   ├── versions/
│   └── env.py
│
├── scripts/                 # Scripts útiles
│   ├── seed_data.py         # Datos iniciales
│   ├── create_admin.py      # Crear admin global
│   └── backup_db.sh
│
├── docs/                    # Documentación adicional
│   ├── api/
│   └── architecture/
│
├── .env.example             # Variables de entorno de ejemplo
├── .gitignore
├── requirements.txt         # Dependencias Python
├── pyproject.toml           # Poetry/PDM config (alternativa)
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🎯 Principios de Arquitectura

### 1. **Separación de Capas (Clean Architecture)**
- **Dominio** no depende de nada (núcleo puro)
- **Aplicación** orquesta casos de uso, depende del dominio
- **Infraestructura** implementa puertos, depende de dominio y aplicación
- **API** depende de aplicación e infraestructura (inyección de dependencias)

### 2. **Domain-Driven Design (DDD)**
- Cada **bounded context** tiene su propia carpeta en `domain/`
- **Entidades** con lógica de negocio
- **Value Objects** inmutables
- **Servicios de dominio** para lógica que no pertenece a una entidad
- **Eventos de dominio** para comunicación entre contextos

### 3. **Hexagonal Architecture (Ports & Adapters)**
- **Puertos**: Interfaces en `domain/*/repositories/`
- **Adaptadores**: Implementaciones en `infrastructure/repositories/`
- Fácil cambio de BD (PostgreSQL → MongoDB) sin tocar dominio

---

## 🔧 Configuración Inicial

### 1. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus valores
```

### 4. Ejecutar migraciones
```bash
alembic upgrade head
```

### 5. Iniciar servidor de desarrollo
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📚 Dependencias Principales

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
asyncpg==0.29.0
alembic==1.13.1
pydantic==2.5.3
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
aiosmtplib==3.0.1
openpyxl==3.1.2
reportlab==4.0.9
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
```

---

## 🚀 Próximos Pasos

1. ✅ Estructura de carpetas creada
2. ⏳ Implementar modelos de dominio (entidades, value objects)
3. ⏳ Implementar repositorios (interfaces + SQLAlchemy)
4. ⏳ Crear casos de uso en `application/`
5. ⏳ Implementar endpoints FastAPI
6. ⏳ Añadir autenticación JWT
7. ⏳ Escribir tests unitarios
8. ⏳ Configurar Docker
9. ⏳ Configurar CI/CD

---

## 📖 Convenciones de Código

- **Naming**: snake_case para archivos/funciones, PascalCase para clases
- **Docstrings**: Google style
- **Type hints**: Obligatorios en funciones públicas
- **Tests**: Nombrar `test_*.py`
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, etc.)

---

## 👥 Asignación de Módulos (4 Desarrolladores)

- **Dev A**: `users/` + `auth/` + seguridad
- **Dev B**: `parking/` + `washing/` + `financial/` (bonos/vales)
- **Dev C**: `pricing/` + `subscriptions/` + `agreements/`
- **Dev D**: `reporting/` + `analytics/` + dashboard + turnos

---

**Listo para empezar a codear! 🚀**
