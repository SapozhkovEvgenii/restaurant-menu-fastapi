"""Initial

Revision ID: 6a24191d51c9
Revises: 
Create Date: 2023-07-31 16:03:06.701503

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6a24191d51c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menu_id'), 'menu', ['id'], unique=False)
    op.create_index(op.f('ix_menu_title'), 'menu', ['title'], unique=True)
    op.create_table('submenu',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['menu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_submenu_id'), 'submenu', ['id'], unique=False)
    op.create_index(op.f('ix_submenu_title'), 'submenu', ['title'], unique=True)
    op.create_table('dish',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.String(), nullable=False),
    sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['submenu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dish_id'), 'dish', ['id'], unique=False)
    op.create_index(op.f('ix_dish_title'), 'dish', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dish_title'), table_name='dish')
    op.drop_index(op.f('ix_dish_id'), table_name='dish')
    op.drop_table('dish')
    op.drop_index(op.f('ix_submenu_title'), table_name='submenu')
    op.drop_index(op.f('ix_submenu_id'), table_name='submenu')
    op.drop_table('submenu')
    op.drop_index(op.f('ix_menu_title'), table_name='menu')
    op.drop_index(op.f('ix_menu_id'), table_name='menu')
    op.drop_table('menu')
    # ### end Alembic commands ###