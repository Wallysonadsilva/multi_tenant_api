"""Add tenants table and link users

Revision ID: f0a78b925d8b
Revises: df9d833abb1d
Create Date: 2025-02-15 22:17:21.934976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# Migration identifiers
revision = 'f0a78b925d8b'
down_revision = 'df9d833abb1d'

def upgrade():
    # Step 1: Create the tenants table first
    op.create_table(
        'tenants',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), unique=True, nullable=False),
        sa.Column('domain', sa.String(), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now())
    )

    # Step 2: Add tenant_id column to users (AFTER tenants exists)
    op.add_column('users', sa.Column('tenant_id', sa.Integer(), nullable=True))

    # Step 3: Assign a default tenant if needed
    op.execute("UPDATE users SET tenant_id = (SELECT id FROM tenants LIMIT 1) WHERE tenant_id IS NULL;")

    # Step 4: Set tenant_id as NOT NULL
    op.alter_column('users', 'tenant_id', nullable=False)

    # Step 5: Add foreign key constraint
    op.create_foreign_key('fk_users_tenant', 'users', 'tenants', ['tenant_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_users_tenant', 'users', type_='foreignkey')
    op.drop_column('users', 'tenant_id')
    op.drop_table('tenants')
