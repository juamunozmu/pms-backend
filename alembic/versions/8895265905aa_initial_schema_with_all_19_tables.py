"""initial schema with all 19 tables

Revision ID: 8895265905aa
Revises: 
Create Date: 2025-11-21 03:56:12.798178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8895265905aa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Aplicar los cambios a la base de datos (migración hacia adelante).
    """
    pass


def downgrade() -> None:
    """
    Revertir los cambios (rollback).
    """
    pass
