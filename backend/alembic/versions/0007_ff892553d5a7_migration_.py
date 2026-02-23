"""empty message

Revision ID: 0007_ff892553d5a7_migration
Revises: 0006_7b15336a60e3_migration
Create Date: 2026-02-23 04:53:01.766631

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import app
from app.core.security import get_password_hash
from app.enums import RoleEnum, Status, Severity
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0007_ff892553d5a7_migration'
down_revision: Union[str, None] = '0006_7b15336a60e3_migration'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    hashed_password = get_password_hash('inspector123')

    op.bulk_insert(
        sa.Table(
            'users',
            sa.MetaData(),
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('username', sa.String(30), nullable=False),
            sa.Column('full_name', sa.String(255), nullable=True),
            sa.Column('email', sa.String(100), nullable=False),
            sa.Column('role', app.core.decorators.Integer(), nullable=False),
            sa.Column('hashed_password', sa.String(255), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.now),
        ),
        [
            {
                'id': 2,
                'username': 'inspector1',
                'full_name': 'João Silva',
                'email': 'inspector1@example.com',
                'hashed_password': hashed_password,
                'role': RoleEnum.inspector.value,
            },
        ]
    )
    # Atualiza a sequência de users para o próximo ID disponível
    op.execute("SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 0), true)")

    op.bulk_insert(
        sa.Table(
            'establishments',
            sa.MetaData(),
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(255), nullable=False),
            sa.Column('address', sa.String(255), nullable=True),
            sa.Column('cep', sa.String(9), nullable=True),
            sa.Column('city', sa.String(100), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.now),
        ),
        [
            {
                'id': 1,
                'name': 'Restaurante Bom Sabor',
                'address': 'Rua das Flores, 123',
                'cep': '12345-678',
                'city': 'São Paulo',
            },
            {
                'id': 2,
                'name': 'Padaria Doce Manhã',
                'address': 'Avenida Principal, 456',
                'cep': '98765-432',
                'city': 'Rio de Janeiro',
            },
            {
                'id': 3,
                'name': 'Supermercado Central',
                'address': 'Rua Comercial, 789',
                'cep': '54321-987',
                'city': 'Belo Horizonte',
            },
        ]
    )

    op.bulk_insert(
        sa.Table(
            'inspections',
            sa.MetaData(),
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('establishment_id', sa.Integer, nullable=False),
            sa.Column('inspector_id', sa.Integer, nullable=False),
            sa.Column('date_time', sa.DateTime(), nullable=True),
            sa.Column('status', app.core.decorators.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.now),
        ),
        [
            {
                'id': 1,
                'establishment_id': 1,
                'inspector_id': 2,
                'date_time': datetime.now(),
                'status': Status.has_irregularities.value,
            },
        ]
    )

    op.bulk_insert(
        sa.Table(
            'irregularities',
            sa.MetaData(),
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('inspection_id', sa.Integer, nullable=False),
            sa.Column('inspector_id', sa.Integer, nullable=False),
            sa.Column('description', sa.String(255), nullable=False),
            sa.Column('severity', app.core.decorators.Integer(), nullable=False),
            sa.Column('requires_interruption', sa.Boolean(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.now),
        ),
        [
            {
                'id': 1,
                'inspection_id': 1,
                'inspector_id': 2,
                'description': 'Falta de higienização adequada dos equipamentos de cozinha',
                'severity': Severity.major.value,
                'requires_interruption': False,
            },
            {
                'id': 2,
                'inspection_id': 1,
                'inspector_id': 2,
                'description': 'Produtos alimentícios armazenados em temperatura inadequada',
                'severity': Severity.critical.value,
                'requires_interruption': True,
            },
        ]
    )
    
    # Atualiza todas as sequências para o próximo ID disponível
    op.execute("SELECT setval('establishments_id_seq', COALESCE((SELECT MAX(id) FROM establishments), 0), true)")
    op.execute("SELECT setval('inspections_id_seq', COALESCE((SELECT MAX(id) FROM inspections), 0), true)")
    op.execute("SELECT setval('irregularities_id_seq', COALESCE((SELECT MAX(id) FROM irregularities), 0), true)")


def downgrade() -> None:
    op.execute("DELETE FROM irregularities WHERE id IN (1, 2)")
    op.execute("DELETE FROM inspections WHERE id = 1")
    op.execute("DELETE FROM establishments WHERE id IN (1, 2, 3)")
    op.execute("DELETE FROM users WHERE id = 2")
